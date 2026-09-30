# Task 3: Use an LLM to Generate a First Implementation

LLM used: Claude.

## Prompt used

Generate minimal PyTorch code for the following model and dataset. Do not change the architecture
or task.

- Dataset: the four XOR examples (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0.
- Model: 2 inputs → 2 hidden units → 1 output logit, with a choice of hidden activation (sigmoid,
  tanh or relu).
- Loss: BCEWithLogitsLoss.
- Random weight initialisation with a fixed seed.
- Full-batch SGD for a few thousand steps.

After training, report the initial and final loss, all four probabilities, the thresholded labels,
and the gradient of the first-layer weights after backward(). Also include:
- a check that the batch gradient equals the average of the per-example gradients;
- a version where every weight starts at zero, printing the two rows of W1 during training;
- a comparison of the three activations, including the gradient norm at the first step;
- a three-class version (3 logits, CrossEntropyLoss) for the labels 0, 1, 1, 2.

Explain each test in one sentence.

## Generated program

- [xor_net.py](xor_net.py) — data (`X`, `Y_XOR`, `Y_3CLASS`), `make_net`, `fit`, `predict`
- [task1_linear_model.py](task1_linear_model.py) — the linear-only baseline
- [task4_parts_ab.py](task4_parts_ab.py) — learning check and gradient check
- [task4_part_c_symmetry.py](task4_part_c_symmetry.py) — zero initialisation
- [task4_part_d_activations.py](task4_part_d_activations.py) — sigmoid vs tanh vs ReLU
- [task5_three_class.py](task5_three_class.py) — three-class extension

## Inspection before running

| Step | Where in the code |
|---|---|
| Forward pass | `net(X)` inside `fit()`; `make_net` builds `Linear(2,2)` → activation → `Linear(2,1)` |
| Scalar loss | `loss = loss_fn(net(X), targets)` — the mean over the 4 examples |
| Reverse-mode AD | `loss.backward()` — fills `.grad` for every parameter |
| Parameter update | `opt.step()` with `torch.optim.SGD`; `opt.zero_grad()` is called at the start of every step |

## Changes made

Only one: the seed. With seed 1 the tanh network got stuck at loss 0.347 with 2/4 correct. The code
was right, but that run landed in a poor solution. Following Part A, I changed only the seed, to 0,
and used it for every experiment. With seed 0 it learns XOR with 4/4 correct. Nothing else was
changed.

Results: see [task4_results.md](task4_results.md).
