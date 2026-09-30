"""
Part XIII: Comparing the first-order and second-order models.

Measures:
  1. number of distinct parameters
  2. number of zero-probability contexts
  3. diversity of generated sentences
  4. qualitative coherence of generated sentences (with examples)
"""

import random
import re

from first_order_lm import FirstOrderLM, DATA, START, END
from second_order_lm import SecondOrderLM

N_SAMPLES = 100
N_EXAMPLES = 10

training = [s.split() for s in DATA]
training_set = set(DATA)

first = FirstOrderLM()
first.train(training)
second = SecondOrderLM()
second.train(training)

vocab = sorted({w for s in training for w in s})  # 10 words
outputs = vocab + [END]                           # possible next tokens

# All contexts the model could in principle be asked about
first_contexts = [START] + vocab
second_contexts = [(START, START)] + [(START, w) for w in vocab] + \
                  [(a, b) for a in vocab for b in vocab]

# A sentence is "well-formed" if it has the structure of the training data:
#   the <animal> <verb> <preposition> the <place>
WELL_FORMED = re.compile(r"^the (cat|dog) (sat on|ran to) the (mat|rug|park)$")


def report(name, model, contexts):
    observed = model.probs
    nonzero = sum(len(row) for row in observed.values())
    full_size = len(contexts) * len(outputs)
    unseen_contexts = [c for c in contexts if c not in observed]

    random.seed(42)
    samples = [model.generate(mode="sample") for _ in range(N_SAMPLES)]
    distinct = set(samples)
    novel = distinct - training_set
    well_formed = [s for s in samples if WELL_FORMED.match(s)]
    avg_len = sum(len(s.split()) for s in samples) / N_SAMPLES

    print(f"=== {name} ===")
    print("1. Parameters")
    print(f"   full CPT size (contexts x next tokens): {len(contexts)} x {len(outputs)} = {full_size}")
    print(f"   non-zero parameters actually estimated:  {nonzero}")
    print(f"   zero entries in the full CPT:            {full_size - nonzero}")
    print("2. Zero-probability contexts")
    print(f"   observed contexts:   {len(observed)} / {len(contexts)}")
    print(f"   unseen contexts:     {len(unseen_contexts)}  (P(. | context) undefined)")
    print(f"3. Diversity ({N_SAMPLES} sampled sentences)")
    print(f"   distinct sentences:  {len(distinct)}")
    print(f"   novel (not in training data): {len(novel)}")
    print(f"   average length:      {avg_len:.1f} words")
    print("4. Coherence")
    print(f"   well-formed ('the X sat on/ran to the Y'): {len(well_formed)}/{N_SAMPLES}")
    print(f"   first {N_EXAMPLES} samples:")
    for s in samples[:N_EXAMPLES]:
        tag = "training" if s in training_set else ("well-formed" if WELL_FORMED.match(s) else "ill-formed")
        print(f"     [{tag:<11}] {s}")
    print(f"   novel sentences generated:")
    for s in sorted(novel, key=len)[:N_EXAMPLES]:
        print(f"     {s}")
    if not novel:
        print("     (none - every generated sentence is a copy of a training sentence)")
    print()


report("First-order model  P(X_t | X_{t-1})", first, first_contexts)
report("Second-order model P(X_t | X_{t-2}, X_{t-1})", second, second_contexts)
