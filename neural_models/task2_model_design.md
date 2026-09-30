# Task 2: Design the Intelligent Agent

## Model specification

| Part | Choice |
|---|---|
| Architecture | 2 inputs → 2 hidden units → 1 output |
| Hidden layer | a = W1 x + b1 (W1: 2x2, b1: 2), h = f(a) |
| Hidden activation f | tanh (baseline); sigmoid and ReLU compared in Task 4 Part D |
| Output | one logit z = W2 h + b2 (W2: 1x2, b2: 1), p = sigmoid(z) |
| Loss | binary cross-entropy, averaged over the 4 examples (`BCEWithLogitsLoss` on the logit) |
| Optimiser | full-batch gradient descent (SGD), learning rate 1.0, 3000 steps |
| Initialisation | PyTorch's default random initialisation, with a fixed seed |

## Validation criteria

1. Final loss close to 0, far below ln 2 = 0.693 (the loss of always guessing 0.5).
2. All four thresholded predictions (p > 0.5) equal 0, 1, 1, 0.
3. Probabilities confidently near 0 or 1.
4. A non-zero first-layer gradient at the start, and a batch gradient equal to the average of the four
   per-example gradients.
5. Repeated runs with different seeds, to see how reliably the network learns.

## Questions 1-3

See [answers.md](answers.md), Questions 1-3.
