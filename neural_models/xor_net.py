"""
Redundant safety sensors: learning XOR with a tiny neural network.

    hidden:  a = W1 x + b1,  h = f(a)       (2 hidden units)
    output:  z = W2 h + b2                  (logits)

Binary task:  1 logit,  p = sigmoid(z), binary cross-entropy (BCEWithLogitsLoss)
3-class task: 3 logits, p = softmax(z), cross-entropy (CrossEntropyLoss)

Shared by every experiment script in this folder.
"""

import torch
import torch.nn as nn

torch.set_num_threads(1)   # tiny tensors: one thread is faster

X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
Y_XOR = torch.tensor([[0.], [1.], [1.], [0.]])      # warning when the sensors disagree
Y_3CLASS = torch.tensor([0, 1, 1, 2])               # 0 both off, 1 disagree, 2 both on

ACTIVATIONS = {"sigmoid": nn.Sigmoid, "tanh": nn.Tanh, "relu": nn.ReLU}


def make_net(activation="tanh", outputs=1):
    """2 -> 2 -> outputs network; returns logits."""
    return nn.Sequential(
        nn.Linear(2, 2),
        ACTIVATIONS[activation](),
        nn.Linear(2, outputs),
    )


def fit(net, targets, loss_fn, steps=3000, lr=1.0, record=()):
    """Full-batch gradient descent.

    Returns a dict with the loss before and after training, and the
    first-layer gradient norm ||dL/dW1|| at step 0.
    `record` is a list of steps at which W1 is printed.
    """
    opt = torch.optim.SGD(net.parameters(), lr=lr)
    W1 = net[0].weight
    info = {}
    for step in range(steps + 1):
        opt.zero_grad()
        loss = loss_fn(net(X), targets)      # forward pass + scalar loss
        loss.backward()                      # backpropagation fills .grad
        if step == 0:
            info["loss_start"] = loss.item()
            info["grad_norm_start"] = W1.grad.norm().item()
        if step in record:
            print(f"  step {step:5}: W1 row 0 = {W1.data[0].tolist()}, W1 row 1 = {W1.data[1].tolist()}")
        if step < steps:
            opt.step()                       # parameter update
    info["loss_end"] = loss.item()
    return info


def predict(net):
    with torch.no_grad():
        p = torch.sigmoid(net(X)).flatten()
    return p, (p > 0.5).long()
