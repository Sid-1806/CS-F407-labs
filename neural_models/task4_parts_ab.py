"""
Task 4, Parts A and B: does the network learn XOR, and is the gradient right?

Part A: loss before/after, the four probabilities and labels.
Part B: W1.grad = dL/dW1. The loss is a mean over the 4 examples, so this
        should equal the average of the 4 single-example gradients.
"""

import torch
import torch.nn as nn

from xor_net import X, Y_XOR, make_net, fit, predict

loss_fn = nn.BCEWithLogitsLoss()
torch.manual_seed(0)
net = make_net("tanh")

# Part B at the starting weights
net.zero_grad()
loss_fn(net(X), Y_XOR).backward()
batch_grad = net[0].weight.grad.clone()

single = []
for i in range(4):
    net.zero_grad()
    loss_fn(net(X[i:i + 1]), Y_XOR[i:i + 1]).backward()
    single.append(net[0].weight.grad.clone())
average = torch.stack(single).mean(0)

print("Part B: gradient check at the initial weights")
print("  dL/dW1 (full batch):          ", [[round(v, 6) for v in row] for row in batch_grad.tolist()])
print("  mean of 4 per-example grads:  ", [[round(v, 6) for v in row] for row in average.tolist()])
print("  same:", torch.allclose(batch_grad, average, atol=1e-7))

# Part A
print("\nPart A: training (tanh, SGD lr 1.0, 3000 steps, seed 0)")
info = fit(net, Y_XOR, loss_fn)
p, labels = predict(net)
print(f"  loss: {info['loss_start']:.4f} -> {info['loss_end']:.4f}")
for x, y, prob, lab in zip(X.tolist(), Y_XOR.flatten().tolist(), p.tolist(), labels.tolist()):
    print(f"  x={x}  target={int(y)}  p={prob:.4f}  label={lab}")
print(f"  correct: {(labels == Y_XOR.flatten().long()).sum().item()}/4")
print("  dL/dW1 after training:", [[f"{v:.2e}" for v in row] for row in net[0].weight.grad.tolist()])
