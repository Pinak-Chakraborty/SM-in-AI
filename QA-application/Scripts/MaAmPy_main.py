######################################################################
# Question Answering Application - MaAmPy
# This is main module for MaAmPy application that takes input question
# It needs the following scripts
# (1) Search_Chunk from QuesChunk.py
# (2) check_WordNet and Tell_Me_Alfred from ALFRED.2.py
######################################################################

import os 
os.system("cls") #clear the screen

print ("INFO - warming up - importing packages....")

# package imports
import nltk, codecs, sys, re
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import classification_report

#MaAmPy module import written for this project
from QuesChunk import Search_Chunk # this is our module to determine search chunk 
from ALFRED_3 import check_WordNet # this is our module to check word net
from ALFRED_3 import Tell_Me_Alfred # this is our module to search web

# define global data structures for feature extraction, featureset and class label
features  = {}
cls_set = []
featuresets = []
searchChunk = ""
q_dict = {"LOC": "Location", "NUM":"Number", "HUM":"Human", "DESC":"Description", \
          "ENTY":"Entity", "ABBR":"Abbreviation"}

def TokenizePosChunk(line):
# This function uses NLTK routines to tokenize, pos tag and it then creates chunks
# based on the grammer defined as chgrammar.
# It then extracts features and appends these to featureset to be used by the
# classifier

    tokenizedSentTemp = nltk.word_tokenize(line) # tokenize the question (contains class labels)

    tokenizedSent = tokenizedSentTemp[3:] #take out the class marker
    mainClass = tokenizedSentTemp[0] #separate out the main class
    subClass = tokenizedSentTemp[2] #separate out the sub class
   
    tokenizedSent = tokenizedSentTemp
            
    tokenizedSentwithPos = nltk.pos_tag(tokenizedSent) # determine POS for every token

    # now extract features - tokens, POS and chunks (tbd)
    global features
    features = {}
    for tokenTuple in tokenizedSentwithPos:
        for token in tokenTuple:
            features['contains(%s)' % token.lower()] = True

    # add to class label list if not already added
    global cls_set
    if mainClass not in cls_set:
        cls_set.append(mainClass)

    # featuresets - list of tuples of the form (features, class index)
    global featuresets 
    featuresets.append((features,cls_set.index(mainClass)))

def TokenizePosChunkTest(line):
# Same as as the routine TokenizePosChunk above but without a class label for test
# question and it determines the search chunk for the question

    # global searchChunk
    global searchChunk
    searchChunk = ""
    
    tokenizedSent = nltk.word_tokenize(line) # tokenize the question (contains class labels)
    tokenizedSentwithPos = nltk.pos_tag(tokenizedSent) # determine POS for every token

    searchChunk = Search_Chunk(tokenizedSentwithPos) # determine the search chunk
    #print ("search chunk in call ", searchChunk)
    
    # now extract features - tokens and their POS 
    global features
    features = {}
    for tokenTuple in tokenizedSentwithPos:
        for token in tokenTuple:
            features['contains(%s)' % token.lower()] = True

def classify_train_test ():
# This function reads train data sets and calls TokenizePosChunk function to create
# featureset and then uses the SVM classifier to train the model
# It then reads test data set and calls TokenizePosChunk function to create
# features for test data set and uses SVM classifier to predict class labels

#    trainDataFileList = ["train_1000.label", "train_2000.label", \
#                      "train_3000.label", "train_4000.label", \
#                      "train_5500.label"]
    trainDataFileList = ["train_1000.label"]
#                      
    
    global features, cls_set, featuresets, searchChunk
    features  = {}
    cls_set = []
    featuresets = []
    searchChunk = ""

    # process all train data sets and build featureset
    for trainDataFile in trainDataFileList:
        for line in open(trainDataFile, encoding="ISO-8859-1"):
            TokenizePosChunk(line)
    train = featuresets #store featureset as train
    
    # SVM with a Linear Kernel and default parameters
    classif = SklearnClassifier(LinearSVC())
    classif.train(train)

    quest = " "
    quest = input ("enter question (q! to quit)==> ")

    while (quest != "q!"):
        # initialize global variables for test dataset processing
        features  = {}
        #cls_set = [] # no need to initialize class set for test
        featuresets = []
        testques = []
        searchChunk = ""
        
        testques.append(quest)
        TokenizePosChunkTest(quest)
        test = features #store features as test now
        #print ("search chunk aft call ", searchChunk)

        p = classif.classify_many(test)

        chunkVar = searchChunk
        classVar = q_dict[cls_set[p[0]]]
        
        print ("Searching for  => ", chunkVar, "\nQuestion Class => ", classVar)
        Tell_Me_Alfred (chunkVar, classVar)
        
        #print (cls_set)
        #print("\n")
        #print(p)
        print("\n")

        quest = input ("enter question (q! to quit)==> ")

# now run the clasify function
classify_train_test()

