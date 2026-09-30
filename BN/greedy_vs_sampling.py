"""
Part X: Deterministic vs probabilistic generation.

Mode A (greedy):   always choose argmax_w P(w | w_previous)
Mode B (sampling): draw w ~ P(w | w_previous)

Generates five sentences with each mode and compares their variation.
"""

import random

from first_order_lm import FirstOrderLM, DATA

N = 5

model = FirstOrderLM()
model.train([s.split() for s in DATA])
random.seed(42)

for mode, label in [("greedy", "Mode A: Greedy"), ("sample", "Mode B: Sampling")]:
    sentences = [model.generate(mode=mode) for _ in range(N)]
    print(f"{label}")
    for i, s in enumerate(sentences, 1):
        print(f"  {i}. {s}")
    print(f"  distinct sentences: {len(set(sentences))}/{N}\n")
