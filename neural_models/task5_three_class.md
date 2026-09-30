# Task 5: Extend the Task

| Class | Meaning | Inputs |
|---|---|---|
| 0 | both sensors inactive | (0,0) |
| 1 | sensors disagree | (0,1), (1,0) |
| 2 | both sensors active | (1,1) |

## Modified output design

Only the output layer and the loss change. The hidden layer (2 tanh units) is the same.

| | Binary XOR | Three-class |
|---|---|---|
| Output layer | `nn.Linear(2, 1)` | `nn.Linear(2, 3)` — `make_net("tanh", outputs=3)` |
| Output | 1 logit → sigmoid | 3 logits → softmax |
| Loss | `BCEWithLogitsLoss` | `CrossEntropyLoss` |
| Targets | `Y_XOR = [[0],[1],[1],[0]]` | `Y_3CLASS = [0, 1, 1, 2]` |

## Predictions before running

1. **Shape of the final weight matrix:** 3 x 2 (3 logits from 2 hidden units), plus a bias of 3.
2. **Logits per example:** 3, so the output for the batch of four is 4 x 3.
3. **Why softmax probabilities sum to one:** pₖ = exp(zₖ) / Σⱼ exp(zⱼ). Every term is positive, and
   they all share a denominator equal to the sum of the numerators, so Σₖ pₖ = 1.
4. **Why the logit gradient is p − y:** with a one-hot target y and true class c, the loss is
   L = −log p_c = −z_c + log Σⱼ exp(zⱼ). Differentiating with respect to zₖ gives
   ∂L/∂zₖ = −[k = c] + exp(zₖ)/Σⱼ exp(zⱼ) = pₖ − yₖ.

## Results

Code: [task5_three_class.py](task5_three_class.py) — seed 0, SGD lr 1.0, 3000 steps.

```
final layer weight shape: (3, 2)  logits shape: (4, 3)
loss: 1.0591 -> 0.0004   (ln 3 = 1.0986)

x=[0.0, 0.0]  target=0  p=[0.9995, 0.0005, 0.0]  predicted=0
x=[0.0, 1.0]  target=1  p=[0.0001, 0.9996, 0.0002]  predicted=1
x=[1.0, 0.0]  target=1  p=[0.0001, 0.9996, 0.0002]  predicted=1
x=[1.0, 1.0]  target=2  p=[0.0, 0.0005, 0.9995]  predicted=2
```

- Both shape predictions are confirmed.
- All four inputs are classified correctly.
- The starting loss 1.0591 is close to ln 3 = 1.0986, the loss of guessing each class with
  probability ⅓.

| Input | Target | p(class 0) | p(class 1) | p(class 2) | Predicted |
|---|---|---|---|---|---|
| (0,0) | 0 | 0.9995 | 0.0005 | 0.0000 | 0 |
| (0,1) | 1 | 0.0001 | 0.9996 | 0.0002 | 1 |
| (1,0) | 1 | 0.0001 | 0.9996 | 0.0002 | 1 |
| (1,1) | 2 | 0.0000 | 0.0005 | 0.9995 | 2 |

## Checks

**Softmax sums to 1**, for the input (0,1):
```
x=[0,1]: p = [0.0001280092546949163, 0.9996238946914673, 0.00024805398425087333]
         sum = 1.0000000
```

**The logit gradient equals p − y**, for the input (0,1):
```
dL/dz (autograd): [0.000128, -0.000376, 0.000248]
p - y:            [0.000128, -0.000376, 0.000248]
```

**Optional diagnostic: shifting every logit by the same amount.**
```
softmax(z + 100) max change: 7.0e-10
exp(z + 1000) without subtracting the max: [inf, inf, inf]
```
Adding a constant c to every logit multiplies both the top and the bottom of the softmax by exp(c),
so the probabilities do not change; the 7e-10 difference is only rounding. But exponentiating large
logits directly overflows to infinity, and inf / inf gives nan. Subtracting the largest logit first
makes the biggest exponent exp(0) = 1 and every other one at most 1, so nothing can overflow and the
probabilities are exactly the same. That is why stable implementations subtract the maximum logit.
