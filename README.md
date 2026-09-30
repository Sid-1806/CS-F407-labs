# Artificial Intelligence (CS F407) — Lab Solutions

Code implementations, experiments and write-ups for the CS F407 labs: logic and planning, search,
agents, neural models and Bayesian networks.

## Contents

1. [Logic](#1-logic)
2. [Search](#2-search)
3. [Agents](#3-agents)
4. [Neural Models](#4-neural-models)
5. [Bayesian Networks](#5-bayesian-networks)
6. [Repository Structure](#repository-structure)

## 1. Logic

- **Folder:** [`logic/`](logic/)
- **Problem Specification:** [`logic_lab_ex.pdf`](logic/logic_lab_ex.pdf)
- **Code:** [`planner.py`](logic/planner.py), [`robot_delivery.py`](logic/robot_delivery.py), Prolog `*.pl`
- **Write-ups:** `task0`–`task8` `.md`, `reflection_*.md`

**Core concepts:** STRIPS-style actions (preconditions and effects) with a BFS planner to move a
package from A to C, and Prolog to check connections and plans. The planner finds the 4-step plan
and reports "no plan" when the task is impossible.

## 2. Search

- **Folder:** [`search/`](search/)
- **Problem Specification:** [`search_lab_ex.pdf`](search/search_lab_ex.pdf)
- **Code:** [`warehouse.py`](search/warehouse.py)
- **Write-ups:** `task0`–`task6` `.md`, [`answers.md`](search/answers.md)

**Core concepts:** Warehouse navigation as a search problem P = (S, A, T, s0, G, c); A* vs BFS;
Manhattan, zero, Euclidean and 2 × Manhattan heuristics. Both algorithms find the 40-move path,
and the overestimating heuristic searches less but returns a longer path (17 vs 13).

## 3. Agents

- **Folder:** [`agents/`](agents/)
- **Problem Specification:** [`agents_lab.pdf`](agents/agents_lab.pdf)
- **Code:** [`goal_based_agent.py`](agents/goal_based_agent.py)
- **Write-ups:** `task2`–`task3` `.md`, [`answers.md`](agents/answers.md)

**Core concepts:** A goal-based agent, kept separate from its environment, that plans a
collision-free route with BFS before moving. It reaches the goal in the minimum 20 moves.

## 4. Neural Models

- **Folder:** [`neural_models/`](neural_models/)
- **Problem Specification:** [`neur_models_lab_ex.pdf`](neural_models/neur_models_lab_ex.pdf)
- **Code:** [`xor_net.py`](neural_models/xor_net.py) and one script per experiment
- **Write-ups:** `task1`–`task5` `.md`, [`answers.md`](neural_models/answers.md)

**Core concepts:** A 2-2-1 PyTorch network learning XOR: why a non-linear hidden layer is needed,
gradient checks, zero initialisation, sigmoid vs tanh vs ReLU, and a softmax three-class output.
A linear model is stuck at loss 0.6931; one tanh hidden layer solves XOR (loss 0.0011, 4/4).

## 5. Bayesian Networks

- **Folder:** [`BN/`](BN/)
- **Problem Specification:** [`BN_lab (1).pdf`](<BN/BN_lab (1).pdf>)
- **Code:** [`first_order_lm.py`](BN/first_order_lm.py), [`second_order_lm.py`](BN/second_order_lm.py)
- **Write-ups:** [`answers.md`](BN/answers.md)

**Core concepts:** Language models as Bayesian networks: first- and second-order Markov models built
from counts, normalisation tests, and greedy vs sampled generation. More context predicts better but
needs far more data (only 15 of 111 second-order contexts observed).

## Repository Structure

```
lab/
├── logic/
│   ├── planner.py              # STRIPS actions + BFS planner
│   ├── robot_delivery.py       # A → C delivery problem
│   ├── task3_tests.py          # Planner tests
│   └── *.pl                    # Prolog knowledge base and plan checks
├── search/
│   ├── warehouse.py            # Search problem, heuristics, A*, BFS
│   ├── task3_tests.py          # Tests with known answers
│   ├── task5_compare.py        # BFS vs A*
│   └── task6_heuristics.py     # Heuristic comparison
├── agents/
│   └── goal_based_agent.py     # Environment + goal-based agent
├── neural_models/
│   ├── xor_net.py              # Data, network, training loop
│   └── task1/4/5_*.py          # One script per experiment
└── BN/
    ├── first_order_lm.py       # Bigram model
    ├── second_order_lm.py      # Trigram model
    └── *.py                    # One script per lab part
```

Each folder also contains the handout PDF and the `.md` write-ups.
