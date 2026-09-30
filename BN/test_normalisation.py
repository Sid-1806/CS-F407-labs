"""
Part VII: Test the probability model.

For every current word w, a valid conditional distribution must satisfy

    sum_v P(v | w) = 1.
"""

from first_order_lm import FirstOrderLM, DATA

model = FirstOrderLM()
model.train([s.split() for s in DATA])
probabilities = model.probs

for word in probabilities:
    total = sum(probabilities[word].values())
    print(word, total)
