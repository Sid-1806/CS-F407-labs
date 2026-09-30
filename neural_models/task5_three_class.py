"""
Task 5: three-class version of the sensor problem.

    0 = both sensors off (0,0),  1 = sensors disagree (0,1)/(1,0),  2 = both on (1,1)

Only the output layer (3 logits) and the loss (cross-entropy) change.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from xor_net import X, Y_3CLASS, make_net, fit

torch.manual_seed(0)
net = make_net("tanh", outputs=3)
print("final layer weight shape:", tuple(net[2].weight.shape), " logits shape:", tuple(net(X).shape))

info = fit(net, Y_3CLASS, nn.CrossEntropyLoss())
print(f"loss: {info['loss_start']:.4f} -> {info['loss_end']:.4f}   (ln 3 = 1.0986)\n")

with torch.no_grad():
    z = net(X)
    p = torch.softmax(z, dim=1)
for x, y, row in zip(X.tolist(), Y_3CLASS.tolist(), p.tolist()):
    print(f"x={x}  target={y}  p={[round(v, 4) for v in row]}  predicted={row.index(max(row))}")

# Check 1: probabilities sum to 1
print(f"\nx=[0,1]: p = {p[1].tolist()}\n         sum = {p[1].sum().item():.7f}")

# Check 2: adding 100 to every logit does not change softmax
shifted = torch.softmax(z[1] + 100, dim=0)
print(f"softmax(z + 100) max change: {(shifted - p[1]).abs().max().item():.1e}")
print(f"exp(z + 1000) without subtracting the max: {torch.exp(z[1] + 1000).tolist()}")

# Check 3: gradient of the loss w.r.t. the logits equals p - y
z1 = z[1:2].clone().requires_grad_()
F.cross_entropy(z1, Y_3CLASS[1:2]).backward()
print(f"\ndL/dz (autograd): {[round(v, 6) for v in z1.grad[0].tolist()]}")
print(f"p - y:            {[round(v, 6) for v in (p[1] - F.one_hot(Y_3CLASS[1], 3)).tolist()]}")
