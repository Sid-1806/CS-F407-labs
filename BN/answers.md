AI Laboratory: Bayesian Networks and Autoregressive Language Models
Answers to Questions 1-14


Question 1: Why is this decomposition useful for generating text?

It breaks the probability of a whole sentence into one word at a time, each conditioned on the words before it. So instead of choosing a whole sentence at once, we just pick the next word given what we have so far, again and again, which matches how text is written from left to right. Since the chain rule is exact, this still gives the correct overall probability, and each small conditional can be learned from data.


Question 2: What independence assumption is being made by this network?

Each word depends only on the previous word: P(X_t | X_1, ..., X_t-1) = P(X_t | X_t-1). In other words, X_t is conditionally independent of X_1, ..., X_t-2 given X_t-1. This is the first-order Markov assumption.


Question 3: Construct P(next word | current word) and identify zero-probability transitions.

the: cat 0.25, dog 0.25, mat 0.167, rug 0.167, park 0.167
cat: sat 0.667, ran 0.333
dog: sat 0.667, ran 0.333
sat: on 1.0
ran: to 1.0

Every other transition is zero, for example "the the", "the <END>", "cat <END>", "sat to" and "ran on". Some zeros are genuine (like "the the"), but others like "sat to" are only zero because the dataset is so small.


Question 4: Where in the program are the transition counts stored?

In the nested dictionary self.counts, filled in the train method. self.counts[prev][next] stores how many times next followed prev, for example self.counts["the"]["cat"] = 3.


Question 5: Where is P(X_t | X_t-1) computed?

In the _build_distribution method, which divides each count by the total of its row and stores the result in self.probs. For example, P(cat | the) = 3/12 = 0.25.


Question 6: How does the program choose the next word?

It supports both. predict_next always picks the most probable word (greedy), while sample_next picks randomly according to the probabilities (the default). Greedy always gives the same sentence and here gets stuck in a loop, while sampling gives varied sentences that reflect the whole distribution.


Question 7: What happens if the program encounters a word for which no transition has been observed?

Its distribution is empty, so predict_next and sample_next return None and generation just stops. It does not crash. The bigger issue is that any unseen transition gets zero probability, so plausible sentences like "the dog ran to the mat" are treated as impossible.


Question 8: If one of the totals is 0.87, what does this tell you about the implementation?

There is a bug, because the probabilities for each previous word must add up to 1. Some probability is missing, probably from dividing by the wrong total or leaving out some next words such as <END> when counting. Sampling would still run, since random.choices rescales the weights, so only a test like this catches it.


Question 9: Are the most probable predictions always the same as the words you would expect?

Mostly, but not always. After "dog" the model prefers "sat" only because it appeared more often, and after "ran" it cannot predict anything except "to". This shows the model only knows word frequencies from its small training data and one previous word, while a person uses meaning, grammar and the whole sentence.


Question 10: Which mode produces more variation, and why?

Sampling. Greedy produced the same looping sentence all five times, because it always picks the single most likely word. Sampling produced four different sentences out of five, because it can pick any word with non-zero probability.


Question 11: How does the second-order model differ from the first-order model?

Graph structure: each word has two parents instead of one.
Probability table: one row per pair of previous words instead of one word, so it grew from 121 to 1221 entries.
Context: it sees two words, so it can tell "on the" apart from "to the", and all of its generated sentences were well-formed.
Data needed: much more. Only 15 of 111 contexts were observed, so it just copied the training sentences.


Question 12: Why does more context improve prediction but make estimation harder?

More context lets the model tell different situations apart, so its predictions become more accurate. But the probability table grows roughly as V to the power n, so with limited data most contexts are never seen and the rest are based on very few examples. Here the table grew from 121 to 1221 entries but 96 of the 111 contexts were never observed, so the model memorised the data instead of generalising.


Question 13: Why is Approach B preferable?

Approach B states exactly what model to build, so the result can be checked against it. Because I understood the representation, I could inspect the code and found a real bug: show_distribution crashed on "The" because it lowercased the word in one lookup but not the other. The specification also gives properties to test, such as each row summing to 1, and keeps the model separate from the code, so I can tell whether a problem comes from a bug or from the model being too simple.


Question 14: What did thinking of the language model as a Bayesian network give you?

It showed the dependencies clearly, and adding one extra arrow turned the first-order model into the second-order one. It factorised the sentence probability into small conditionals that can be estimated by counting. It made generation principled, since generating is just sampling each word given its parents in order. It also gave me a way to test the code, because every row of the table must be a valid probability distribution.
