"""
First-order autoregressive (bigram) language model.

Models P(X_t | X_{t-1}) estimated from transition counts:

    P(w_j | w_i) = C(w_i, w_j) / sum_k C(w_i, w_k)

No ML libraries are used -- only dicts and the `random` module.
"""

import random

START = "<START>"
END = "<END>"


class FirstOrderLM:
    def __init__(self):
        # counts[prev][next] = number of times `next` followed `prev`
        self.counts = {}
        # probs[prev][next] = P(next | prev)
        self.probs = {}

    # 1-2. Train: count transitions between consecutive tokens
    def train(self, sentences):
        """sentences: list of token lists, e.g. [["the", "cat", "sat"], ...]"""
        for tokens in sentences:
            padded = [START] + [t.lower() for t in tokens] + [END]
            for prev, nxt in zip(padded, padded[1:]):
                self.counts.setdefault(prev, {})
                self.counts[prev][nxt] = self.counts[prev].get(nxt, 0) + 1
        self._build_distribution()

    # 3. Construct P(X_t | X_{t-1}) by normalising each row of counts
    def _build_distribution(self):
        self.probs = {}
        for prev, row in self.counts.items():
            total = sum(row.values())
            self.probs[prev] = {nxt: c / total for nxt, c in row.items()}

    def distribution(self, prev):
        """Return P(. | prev) as a dict, or {} if prev was never seen."""
        return self.probs.get(prev.lower() if prev not in (START, END) else prev, {})

    # 4. Display the probabilities for a specified previous token
    def show_distribution(self, prev):
        dist = self.distribution(prev)
        print(f"P(next | {prev!r}):")
        if not dist:
            print("  (no observed transitions)")
            return
        for nxt, p in sorted(dist.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {nxt:<8} {p:.3f}")

    # 5. Predict the most probable next token (ties broken alphabetically)
    def predict_next(self, prev):
        dist = self.distribution(prev)
        if not dist:
            return None
        return min(dist, key=lambda w: (-dist[w], w))

    def sample_next(self, prev, rng=random):
        """Sample the next token from P(. | prev)."""
        dist = self.distribution(prev)
        if not dist:
            return None
        words = list(dist)
        weights = [dist[w] for w in words]
        return rng.choices(words, weights=weights, k=1)[0]

    # 6-7. Generate by repeatedly sampling until <END> is produced
    def generate(self, mode="sample", max_len=30, rng=random):
        """mode: 'sample' (draw from the distribution) or 'greedy' (argmax)."""
        tokens = []
        prev = START
        for _ in range(max_len):
            nxt = self.sample_next(prev, rng) if mode == "sample" else self.predict_next(prev)
            if nxt is None or nxt == END:  # stop at <END> (or an unseen context)
                break
            tokens.append(nxt)
            prev = nxt
        return " ".join(tokens)


DATA = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


if __name__ == "__main__":
    model = FirstOrderLM()
    model.train([s.split() for s in DATA])

    for w in [START, "the", "cat", "dog", "sat", "ran", "on", "to"]:
        model.show_distribution(w)
        print(f"  most probable next: {model.predict_next(w)}\n")

    random.seed(0)
    print("Sampled sentences:")
    for _ in range(5):
        print(" ", model.generate())
