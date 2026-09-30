# Task 1: Understand the Problem Before Coding

## 1. Problem specification

Two redundant binary sensors x1 and x2. The device must raise a disagreement warning exactly when
one sensor is on and the other is off.

- Input space: X = {0,1}², the readings (x1, x2).
- Output space: Y = {0,1}, where 1 = "sensors disagree, raise a warning".
- The rule is y = x1 XOR x2.

| x1 | x2 | y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

These four examples are every possible input, so the training set is also the complete test set.

## 2. Sketch of the four points

```
 x2
  1 |   1 (0,1)          0 (1,1)
    |
    |
  0 |   0 (0,0)          1 (1,0)
    +------------------------------ x1
          0                1
```

The class-1 points are on one diagonal and the class-0 points are on the other.

## 3. Why one straight boundary cannot separate the classes

A straight line splits the plane into two sides. If both class-1 points were on one side, the whole
segment joining them would be on that side too. But the segment from (0,1) to (1,0) and the segment
from (0,0) to (1,1) cross at (0.5, 0.5), so that point would have to be on both sides at once, which
is impossible.

## 4. Prediction for a single affine map + sigmoid

It cannot get all four right. Under cross-entropy its best option is to predict p = 0.5 for every
input, which gives a loss of ln 2 ≈ 0.693.

Checked with [task1_linear_model.py](task1_linear_model.py) (`nn.Linear(2, 1)` + BCEWithLogitsLoss,
SGD lr 1.0, 3000 steps):

```
loss: 0.7168 -> 0.6931   (ln 2 = 0.6931)
weights: [0.0, 0.0] bias: -0.0
  x=[0.0, 0.0]  target=0  p=0.5000
  x=[0.0, 1.0]  target=1  p=0.5000
  x=[1.0, 0.0]  target=1  p=0.5000
  x=[1.0, 1.0]  target=0  p=0.5000
```

The prediction holds: the weights shrink to 0, every probability is 0.5, and the loss stays at ln 2.
