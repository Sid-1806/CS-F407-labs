"""
Part VIII: Predicting the next word.

For several contexts w, display P(X_{t+1} | X_t = w) and the most probable
next word argmax_v P(v | w), then compare it with the word a human would
expect (Question 9).
"""

from first_order_lm import FirstOrderLM, DATA

model = FirstOrderLM()
model.train([s.split() for s in DATA])

# The next word I would personally expect after each context.
# Edit these to your own expectations.
HUMAN_EXPECTATION = {
    "the": "dog",
    "cat": "sat",
    "dog": "ran",
    "sat": "on",
    "ran": "away",
    "on": "the",
    "to": "the",
}

matches = 0
for word, expected in HUMAN_EXPECTATION.items():
    dist = model.distribution(word)
    predicted = model.predict_next(word)
    tied = [v for v, p in dist.items() if p == dist[predicted]]

    model.show_distribution(word)
    print(f"  argmax (model): {predicted}" + (f"   (tie between {tied})" if len(tied) > 1 else ""))
    print(f"  human expects:  {expected}   P = {dist.get(expected, 0.0):.3f}")
    if expected in tied:
        matches += 1
        print("  -> MATCH")
    else:
        print("  -> DIFFERENT" + ("  (never seen in training)" if expected not in dist else ""))
    print()

print(f"Model argmax agreed with human expectation in {matches}/{len(HUMAN_EXPECTATION)} contexts.")
