"""
Second-order autoregressive (trigram) language model.

Models P(X_t | X_{t-2}, X_{t-1}) estimated from counts of observed triples:

    P(w_k | w_i, w_j) = C(w_i, w_j, w_k) / sum_m C(w_i, w_j, w_m)

Bayesian-network structure:  X_{t-2} -> X_t <- X_{t-1}

Each sentence is padded with two <START> tokens so that the first words
also have a two-token context: P(X_1 | <START>, <START>), P(X_2 | <START>, X_1).

No ML libraries are used -- only dicts and the `random` module.
"""

import random

START = "<START>"
END = "<END>"


class SecondOrderLM:
    def __init__(self):
        # counts[(prev2, prev1)][next] = number of times `next` followed (prev2, prev1)
        self.counts = {}
        # probs[(prev2, prev1)][next] = P(next | prev2, prev1)
        self.probs = {}

    # Train: count triples of consecutive tokens
    def train(self, sentences):
        """sentences: list of token lists, e.g. [["the", "cat", "sat"], ...]"""
        for tokens in sentences:
            padded = [START, START] + [t.lower() for t in tokens] + [END]
            for prev2, prev1, nxt in zip(padded, padded[1:], padded[2:]):
                context = (prev2, prev1)
                self.counts.setdefault(context, {})
                self.counts[context][nxt] = self.counts[context].get(nxt, 0) + 1
        self._build_distribution()

    # Construct P(X_t | X_{t-2}, X_{t-1}) by normalising each row of triple counts
    def _build_distribution(self):
        self.probs = {}
        for context, row in self.counts.items():
            total = sum(row.values())
            self.probs[context] = {nxt: c / total for nxt, c in row.items()}

    @staticmethod
    def _norm(w):
        return w if w in (START, END) else w.lower()

    def distribution(self, prev2, prev1):
        """Return P(. | prev2, prev1) as a dict, or {} if the context was never seen."""
        return self.probs.get((self._norm(prev2), self._norm(prev1)), {})

    # Display the probabilities for a specified two-token context
    def show_distribution(self, prev2, prev1):
        dist = self.distribution(prev2, prev1)
        print(f"P(next | {prev2!r}, {prev1!r}):")
        if not dist:
            print("  (no observed transitions)")
            return
        for nxt, p in sorted(dist.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {nxt:<8} {p:.3f}")

    # Predict the most probable next token (ties broken alphabetically)
    def predict_next(self, prev2, prev1):
        dist = self.distribution(prev2, prev1)
        if not dist:
            return None
        return min(dist, key=lambda w: (-dist[w], w))

    def sample_next(self, prev2, prev1, rng=random):
        """Sample the next token from P(. | prev2, prev1)."""
        dist = self.distribution(prev2, prev1)
        if not dist:
            return None
        words = list(dist)
        weights = [dist[w] for w in words]
        return rng.choices(words, weights=weights, k=1)[0]

    # Generate by repeatedly sampling until <END> is produced
    def generate(self, mode="sample", max_len=30, rng=random):
        """mode: 'sample' (draw from the distribution) or 'greedy' (argmax)."""
        tokens = []
        prev2, prev1 = START, START
        for _ in range(max_len):
            if mode == "sample":
                nxt = self.sample_next(prev2, prev1, rng)
            else:
                nxt = self.predict_next(prev2, prev1)
            if nxt is None or nxt == END:  # stop at <END> (or an unseen context)
                break
            tokens.append(nxt)
            prev2, prev1 = prev1, nxt  # slide the two-token window
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
    model = SecondOrderLM()
    model.train([s.split() for s in DATA])

    for ctx in [(START, START), (START, "the"), ("the", "cat"), ("the", "dog"),
                ("cat", "sat"), ("sat", "on"), ("on", "the"), ("to", "the")]:
        model.show_distribution(*ctx)
        print(f"  most probable next: {model.predict_next(*ctx)}\n")

    random.seed(0)
    print("Sampled sentences:")
    for _ in range(5):
        print(" ", model.generate())
