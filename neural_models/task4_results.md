# Task 4: Execute, Test, and Diagnose the Generated Code

## Part A: Basic learning check

Code: [task4_parts_ab.py](task4_parts_ab.py) — tanh hidden layer, seed 0, SGD lr 1.0, 3000 steps.

```
Part A: training (tanh, SGD lr 1.0, 3000 steps, seed 0)
  loss: 0.7152 -> 0.0011
  x=[0.0, 0.0]  target=0  p=0.0014  label=0
  x=[0.0, 1.0]  target=1  p=0.9992  label=1
  x=[1.0, 0.0]  target=1  p=0.9992  label=1
  x=[1.0, 1.0]  target=0  p=0.0015  label=0
  correct: 4/4
  dL/dW1 after training: [['-8.74e-05', '-8.73e-05'], ['7.74e-05', '7.73e-05']]
```

| Input | Target | Probability | Label |
|---|---|---|---|
| (0,0) | 0 | 0.0014 | 0 |
| (0,1) | 1 | 0.9992 | 1 |
| (1,0) | 1 | 0.9992 | 1 |
| (1,1) | 0 | 0.0015 | 0 |

- Initial loss 0.7152, final loss 0.0011.
- All four labels are correct.
- The only setting changed was the seed: seed 1 got stuck at loss 0.347 with 2/4 correct, so seed 0
  is used instead.

## Part B: Backpropagation check

At the initial weights:

```
Part B: gradient check at the initial weights
  dL/dW1 (full batch):           [[0.000505, 0.000607], [-0.042569, -0.044773]]
  mean of 4 per-example grads:   [[0.000505, 0.000607], [-0.042569, -0.044773]]
  same: True
```

- `net[0].weight.grad` holds ∂L/∂W⁽¹⁾. Entry [i, j] is how much the loss changes when the weight from
  input j to hidden unit i changes a little.
- The loss is the mean over the four examples, L = ¼ Σᵢ Lᵢ, and differentiation is linear, so
  ∂L/∂W⁽¹⁾ = ¼ Σᵢ ∂Lᵢ/∂W⁽¹⁾. Running backward() on each example separately and averaging gives exactly
  the batch gradient.
- After training, the gradient entries are about 1e-4, because there is almost no error left.

## Part C: Symmetry experiment

Code: [task4_part_c_symmetry.py](task4_part_c_symmetry.py) — every weight and bias set to 0, tanh,
SGD lr 1.0, 3000 steps.

```
Zero initialisation (tanh, SGD lr 1.0, 3000 steps)
  step     0: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  step     1: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  step     2: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  step    10: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  step   100: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  step  1000: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  step  3000: W1 row 0 = [0.0, 0.0], W1 row 1 = [0.0, 0.0]
  loss: 0.6931 -> 0.6931
  ||dL/dW1|| at step 0: 0.000000
  rows identical at the end: True
  probabilities: [0.5, 0.5, 0.5, 0.5], correct: 2/4
```

- The two rows of W1 stay identical, in fact exactly [0, 0], for the whole run. The loss never
  moves from ln 2, and every probability stays at 0.5.
- Why: identical hidden units compute the same output for every input and have the same outgoing
  weight, so they get the same gradient and the same update, and can never become different. Here it
  is even more extreme: tanh(0) = 0 and W2 = 0, so the gradient reaching W1 is exactly zero and the
  weights never move at all.

## Part D: Activation experiment

Code: [task4_part_d_activations.py](task4_part_d_activations.py) — same seed (0), so the same initial
weights, SGD lr 1.0, 3000 steps. Only the hidden activation changes. The early gradient is
‖∂L/∂W⁽¹⁾‖₂ at step 0.

| Hidden activation | Final loss | 4/4 correct? | Early ‖∇W⁽¹⁾L‖₂ |
|---|---|---|---|
| Sigmoid | 0.0191 | yes | 0.0009 |
| Tanh | 0.0011 | yes | 0.0618 |
| ReLU | 0.4774 | no (3/4) | 0.0017 |

Hidden pre-activations a = W1x + b1 after training:

| Input | Sigmoid (unit 1, unit 2) | Tanh (unit 1, unit 2) | ReLU (unit 1, unit 2) |
|---|---|---|---|
| (0,0) | -3.00, 9.24 | -1.91, 5.11 | -2.87, -0.01 |
| (0,1) | 3.67, 3.08 | 2.06, 1.65 | -0.17, -0.53 |
| (1,0) | 3.67, 3.08 | 2.06, 1.65 | -0.17, -0.60 |
| (1,1) | 10.34, -3.08 | 6.04, -1.82 | 2.53, -1.12 |

One seed says little, so each activation was also trained with seeds 0-9:

| Hidden activation | Runs with 4/4 | Mean early ‖∇W⁽¹⁾L‖₂ |
|---|---|---|
| Sigmoid | 7/10 | 0.0062 |
| Tanh | 4/10 | 0.0360 |
| ReLU | 1/10 | 0.0252 |

### Interpretation

Sigmoid started with the smallest gradient (0.0009, and about 6 times smaller than tanh on average
over 10 seeds). That fits sigmoid′ ≤ 0.25 against tanh′(0) = 1, and sigmoid did learn more slowly
(final loss 0.0191 against 0.0011). But the small gradient did not stop it: it solved XOR most often
(7/10). Tanh learned fastest when it worked, but with only two hidden units it got stuck in a poor
solution on 6 of 10 seeds.

ReLU did worst (1/10). In the seed-0 run, unit 2's pre-activation is negative for all four inputs
(-0.01, -0.53, -0.60, -1.12), so it outputs 0 everywhere and gets exactly zero gradient. It is a dead
unit, and the one remaining unit cannot represent XOR, hence 3/4. The sigmoid units have large
pre-activations (9.24, 10.34): they are saturated, but because they have already learned, not
because they failed.

These results are for this setup only: 2 hidden units, plain SGD at lr 1.0, and four examples. They
do not show that one activation is better in general.
