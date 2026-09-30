AI Laboratory: Neural Models - Learning, Depth, Activations, and Output Layers
Answers to Questions 1-10


Question 1: Why is the hidden nonlinearity scientifically necessary here?

Without it the network computes W2(W1 x + b1) + b2 = (W2 W1) x + (W2 b1 + b2), which is again a single affine map. So it can still only draw one straight decision boundary, however many layers are stacked, and XOR cannot be separated by one straight line. A non-linear activation bends the space, so the hidden layer can compute new features such as OR and NAND of the two sensors. XOR is simply "OR and not AND", which is linearly separable in terms of those two features.


Question 2: Why is sigmoid plus binary cross-entropy a sensible engineering pairing for the output?

The target is a single yes/no, so the output should be one probability p = P(warning | x), and sigmoid maps any number to (0, 1). Binary cross-entropy is the negative log-likelihood of a yes/no outcome, so it strongly penalises confident wrong answers. Together they give a simple gradient on the logit, dL/dz = p - y, which stays large when the network is confidently wrong. In PyTorch I used BCEWithLogitsLoss, which combines the sigmoid and the loss in a numerically stable way.


Question 3: What evidence will count as successful learning?

1. The final loss is close to 0, far below ln 2 = 0.693 (the loss of always guessing 0.5).
2. All four thresholded predictions equal 0, 1, 1, 0.
3. The probabilities are confidently near 0 or 1, not just slightly on the right side of 0.5.
4. The first-layer gradient is non-zero at the start (so a learning signal reaches the hidden layer), and the batch gradient equals the average of the four per-example gradients.
5. Repeating the run with different seeds shows how reliably the network learns.


Question 4: What did the XOR experiment demonstrate about the difference between depth and nonlinearity?

That depth alone does nothing without non-linearity. The purely linear model (one affine map plus a sigmoid) got stuck at loss 0.6931 = ln 2, with every probability equal to 0.5, and a stack of linear layers would collapse into the same thing. Adding one tanh hidden layer of only two units was enough to reach a loss of 0.0011 with all four cases correct. What matters is that the hidden layer transforms the inputs into a space where XOR becomes linearly separable, not the number of layers.


Question 5: In your successful run, what evidence showed that backpropagation supplied a useful learning signal rather than merely a nonzero gradient?

The loss fell from 0.7152 to 0.0011, and all four probabilities ended confidently on the correct side (0.0014, 0.9992, 0.9992, 0.0015). By the end the first-layer gradient had shrunk to about 1e-4, because there was almost no error left to correct. In the tanh run with seed 1, by contrast, the gradient was also non-zero but the network got stuck at loss 0.347 with only 2 of 4 correct. So a non-zero gradient alone is not proof of useful learning; the falling loss and the correct predictions are.


Question 6: Why did identical/zero weight initialisation prevent the two hidden units from learning distinct features?

Two hidden units with the same incoming and outgoing weights compute the same output for every input. So backpropagation gives them the same gradient, and gradient descent gives them the same update, and they stay identical forever. The network then behaves as if it had only one hidden unit. With all weights at zero it is even more extreme: tanh(0) = 0 and the output weights are 0, so the gradient reaching the first layer is exactly 0. In my run both rows of W1 stayed exactly [0, 0] for all 3000 steps, the loss stayed at 0.6931 and every probability stayed at 0.5.


Question 7: How did changing the hidden activation affect the gradient you observed? Distinguish the scientific explanation from the engineering observation.

Engineering observation: from the same starting weights (seed 0), the early first-layer gradient norm was 0.0009 for sigmoid, 0.0618 for tanh and 0.0017 for ReLU. Sigmoid learned more slowly (final loss 0.0191) but still got 4/4. Tanh reached 0.0011 with 4/4. ReLU got stuck at 0.4774 with 3/4: its second hidden unit had a negative pre-activation for all four inputs. Over 10 seeds, sigmoid succeeded 7 times, tanh 4 and ReLU once, so a small starting gradient did not mean failure.

Scientific explanation: the gradient reaching W1 is multiplied by the activation's derivative. Sigmoid's derivative is at most 0.25, while tanh's is 1 at 0, so sigmoid passes back a weaker signal and learns more slowly. ReLU's derivative is exactly 1 when the unit is active and exactly 0 when its input is negative. A ReLU unit that is negative for every input gets no gradient at all and never recovers ("dead"), which leaves too few units to represent XOR. A saturated sigmoid is different: its large |pre-activation| gives a small but non-zero derivative.


Question 8: Why must the output layer and loss be selected together according to the task?

The output layer decides what the prediction means, and the loss has to be the right one for that meaning. One sigmoid output is a single yes/no probability, so binary cross-entropy fits. Three softmax outputs are a probability distribution over classes, so multiclass cross-entropy fits. Matched like this, the gradient on the logits is simply p - y. Mismatches break things: squared error on a sigmoid output gives tiny gradients when the answer is confidently wrong, and applying a sigmoid or softmax before a loss that already includes it applies it twice. The code still runs, but it learns the wrong thing.


Question 9: Give one example where the LLM improved your engineering productivity and one example where human verification was essential.

Productivity: the LLM produced the model, the full-batch training loop (zero_grad, forward pass, loss, backward, step), the gradient check and all the experiment scripts in one go, so I could spend my time running and interpreting the experiments.

Verification: the first basic learning check, with seed 1, ended at loss 0.347 with only 2 of 4 correct. The code had no bug; the network had got stuck in a poor solution. Recognising that, and changing only the seed (to 0, which then gave 4/4) rather than changing the task, needed human judgement. Interpreting the zero-initialisation run also needed understanding, not just the printout: the rows stay identical because the gradient into W1 is exactly zero.


Question 10: Which tests in this laboratory would you keep if the model were scaled up, and which would become too expensive?

Keep: the loss curve, accuracy on held-out data, the gradient norm of each layer (to catch vanishing, exploding or dead units), the fraction of dead ReLUs or saturated units, checking that softmax outputs sum to 1 with no nan or inf, and repeating a run with a few seeds.

Too expensive: checking the gradient against finite differences for every parameter (two forward passes per parameter, so billions of passes), printing every probability and every gradient entry, testing every possible input, and running many seeds for every setting. At scale these are replaced by spot-checks on a few random parameters and summary statistics.
