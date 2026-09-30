"""
Task 1.4: What does a purely linear model (one affine map + sigmoid) do on XOR?
"""

import torch
import torch.nn as nn

from xor_net import X, Y_XOR, fit

torch.manual_seed(0)
linear = nn.Sequential(nn.Linear(2, 1))
info = fit(linear, Y_XOR, nn.BCEWithLogitsLoss(), steps=3000, lr=1.0)

with torch.no_grad():
    p = torch.sigmoid(linear(X)).flatten()

print(f"loss: {info['loss_start']:.4f} -> {info['loss_end']:.4f}   (ln 2 = 0.6931)")
print("weights:", [round(v, 4) for v in linear[0].weight.flatten().tolist()],
      "bias:", round(linear[0].bias.item(), 4))
for x, y, prob in zip(X.tolist(), Y_XOR.flatten().tolist(), p.tolist()):
    print(f"  x={x}  target={int(y)}  p={prob:.4f}")
