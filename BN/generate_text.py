"""
Part IX: Generate text.

Generation process:
    X_1 ~ P(X_1 | <START>),  X_2 ~ P(X_2 | X_1),  X_3 ~ P(X_3 | X_2), ...
i.e. sample -> append token -> sample again, until <END> is generated.
"""

import random

from first_order_lm import FirstOrderLM, DATA

N_SENTENCES = 20
OUTPUT_FILE = "generated_sentences.txt"

model = FirstOrderLM()
model.train([s.split() for s in DATA])

random.seed(42)  # fixed seed so the results are reproducible
sentences = [model.generate(mode="sample") for _ in range(N_SENTENCES)]

with open(OUTPUT_FILE, "w") as f:
    for i, s in enumerate(sentences, 1):
        line = f"{i:2}. {s}"
        print(line)
        f.write(line + "\n")

print(f"\nSaved {N_SENTENCES} sentences to {OUTPUT_FILE}")
