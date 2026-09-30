"""
Task 4, Part C: symmetry experiment.

Same 2-2-1 tanh network with every weight and bias set to 0 before training.
The two rows of W1 (one per hidden unit) are printed during training.
"""

import torch
import torch.nn as nn

from xor_net import Y_XOR, make_net, fit, predict

net = make_net("tanh")
with torch.no_grad():
    for param in net.parameters():
        param.zero_()

print("Zero initialisation (tanh, SGD lr 1.0, 3000 steps)")
info = fit(net, Y_XOR, nn.BCEWithLogitsLoss(), record=(0, 1, 2, 10, 100, 1000, 3000))
p, labels = predict(net)
W1 = net[0].weight.data
print(f"  loss: {info['loss_start']:.4f} -> {info['loss_end']:.4f}")
print(f"  ||dL/dW1|| at step 0: {info['grad_norm_start']:.6f}")
print(f"  rows identical at the end: {torch.equal(W1[0], W1[1])}")
print(f"  probabilities: {[round(v, 4) for v in p.tolist()]}, correct: {(labels == Y_XOR.flatten().long()).sum().item()}/4")
