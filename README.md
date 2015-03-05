CSCI 544 Homework 2
=====================
This is an instruction for CSCI544 Homework 2(http://appliednlp.bitbucket.org/hw2/index.html)

The code written for Python 3.4.


Part I
-----------------
The Averaged Perceptron classifier can be used as below:

    python3 perceplearn.py TRAININGFILE MODEL
	python3 percepclassify.py MODEL < TESTINGFILE > OUTPUT

Both TRAININGFILE and TESTINGFILE should have the same format as below:

TRAININGFILE:

LABEL_1 FEATURE_11 FEATURE_12 ... FEATURE_1N 
LABEL_2 FEATURE_21 FEATURE_22 ... FEATURE_2N 
... 
LABEL_M FEATURE_M1 FEATURE_M2 ... FEATURE_MN 

TESTINGFILE

FEATURE_11 FEATURE_12 ... FEATURE_1N 
FEATURE_21 FEATURE_22 ... FEATURE_2N 
... 
FEATURE_M1 FEATURE_M2 ... FEATURE_MN 

Part II
-----------------
Use my averaged perceptron to perform part-of-speech tagging.

The training program, postrain, run as follows:

    python3 postrain.py TRAININGFILE MODEL

where TRAININGFILE is the input file formated with one sentence per line, and each sentence composed of word/tag pairs. For example, a small training file might contain these lines:

This/DT is/VBZ a/DT test/NN ./.

I/PRP saw/VBD a/DT movie/NN ./.

I/PRP like/VBP cookies/NNS ./.


and MODEL is the output file containing the model.

The postag program runs as follows:

    python3 postag.py MODEL < TESTINGFILE > OUTPUT

where MODEL is the model generated by postrain.

postag takes its input from STDIN in the form of one sentence per line,
where each sentence is a sequence of words (without tags). Output will be written to STDOUT, 
and will be a tagged sentence (in the same format as the training data) for each input sentence.

Part III
-----------------
Use my averaged perceptron to perform named entity recogntion.

The method to use it is similar to Part II:

    python3 nelearn.py TRAININGFILE MODEL
	python3 netag.py MODEL < TESTINGFILE > OUTPUT
    
The NER data format is similar to the POS tagging data format, 
but also includes a POS tag between each word and its NER BIO tag: 

WORD/POSTAG/NERTAG WORD/POSTAG/NERTAG ...

Part IV
-----------------
###Source of information
Piazza discussion, TA office hour

### Accuracy of my part-of-speech tagger
After 5 iteration of Averaged Perceptron, my POS tagger accuracy is 93.9%

### Precision, recall and F-score for each named entity types and the overall F-score
After 5 iteration of Averaged Perceptron, I got the following information:

LOC

Precision: 0.607

Recall: 0.678

F-score: 0.641

PER

Precision: 0.587

Recall: 0.734

F-score: 0.653

MISC

Precision: 0.465

Recall: 0.342

F-score: 0.394

ORG

Precision: 0.640

Recall: 0.541

F-score: 0.586


The overall Precision: 0.600

The overall Recall: 0.606

The overall F-score: 0.603

### Use my Naive Bayes classifier instead of my perceptron classifier

Use the Naive Bayes I wrote in HW1 as classifier:

For POS dataset, my POS tagger accuracy is 94.2%

For NER dataset, the performance metrics are as below:

LOC

Precision: 0.590

Recall: 0.670

F-score: 0.627

ORG

Precision: 0.372

Recall: 0.488

F-score: 0.422

PER

Precision: 0.130

Recall: 0.503

F-score: 0.207

MISC

Precision: 0.508

Recall: 0.274

F-score: 0.356


The overall Precision: 0.268

The overall Recall: 0.511

The overall F-score: 0.351

We can see that my Naive Bayes POS tagger has accuracy rate of 94.2%, which is a little higher than my Averaged Perceptron accuracy rate 93.9%. I think one of the reason is may because of my poor Perceptron quality. Also, because POS dataset has as many as 45 classes, which will make finding the class by referring from previous and next words a difficult thing. From my point of view, Perceptron is more sensitive than Naive Bayes for it changes from step by step. If I am unlucky that I meet with many special cases at the end of iteration of Averaged Perceptron, it will affect my model relatively heavily (of course, Averaged Perceptron aims at solve this problem, but need more iteration times), which may also cause a fall in accuracy rate.

When using Naive Bayes to tag NER dataset, we can see a relatively lower Precision, Recall and F-score value than my Averaged Perceptron. I think it is because the major class in NER dataset is "O", which means the classes distribution is not even. As Naive Bayes cares about probability, when P("O") is much bigger than other classes, word has class "O" will tend to be tagged with "O". This may cause tag mistake when a word has low occurrence in all its classes and has class "O". But Perceptron doesn't have this problem because it corrects the weight step by step.