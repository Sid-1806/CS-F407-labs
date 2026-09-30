"""
Task 4, Part D: sigmoid vs tanh vs ReLU hidden units.

Only the activation changes; the seed (so the initial weights), learning rate
and number of steps are the same. The early gradient is ||dL/dW1|| at step 0.
Because a single run can be lucky or unlucky, each activation is also
trained with 10 different seeds.
"""

import torch
import torch.nn as nn

from xor_net import X, Y_XOR, make_net, fit, predict

loss_fn = nn.BCEWithLogitsLoss()
target = Y_XOR.flatten().long()

print("Seed 0, SGD lr 1.0, 3000 steps")
print(f"  {'activation':<11}{'final loss':>11}{'4/4 correct?':>14}{'early ||dL/dW1||':>18}")
for act in ["sigmoid", "tanh", "relu"]:
    torch.manual_seed(0)
    net = make_net(act)
    info = fit(net, Y_XOR, loss_fn)
    p, labels = predict(net)
    correct = (labels == target).sum().item()
    print(f"  {act:<11}{info['loss_end']:>11.4f}{'yes' if correct == 4 else f'no ({correct}/4)':>14}"
          f"{info['grad_norm_start']:>18.4f}")
    with torch.no_grad():
        a = net[0](X)
    print(f"    hidden pre-activations a = W1 x + b1: {[[round(v, 2) for v in row] for row in a.tolist()]}")

print("\nSeeds 0-9")
print(f"  {'activation':<11}{'runs with 4/4':>14}{'mean early ||dL/dW1||':>24}")
for act in ["sigmoid", "tanh", "relu"]:
    wins, norms = 0, []
    for seed in range(10):
        torch.manual_seed(seed)
        net = make_net(act)
        info = fit(net, Y_XOR, loss_fn)
        _, labels = predict(net)
        wins += int((labels == target).all())
        norms.append(info["grad_norm_start"])
    print(f"  {act:<11}{f'{wins}/10':>14}{sum(norms) / len(norms):>24.4f}")
