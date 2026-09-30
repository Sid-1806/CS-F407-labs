"""
Part VII: Test the probability model.

For every current word w (or context), a valid conditional distribution must satisfy

    sum_v P(v | w) = 1.
"""

from first_order_lm import FirstOrderLM, DATA
from second_order_lm import SecondOrderLM

for name, model in [("First-order model", FirstOrderLM()), ("Second-order model", SecondOrderLM())]:
    model.train([s.split() for s in DATA])
    probabilities = model.probs

    print(name)
    for word in probabilities:
        total = sum(probabilities[word].values())
        print(" ", word, total)
    print()
