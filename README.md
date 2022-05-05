# VDP_Java
An adaptation of VulDeePecker for detection of vulnerabilities in Java source code  

## VulDeePecker
VulDeePecker is a deep learning based system that uses the idea of code gadgets (semantically related code snippets) to predict vulnerabilities in C/C++ source code.

The original source code for VulDeePecler is not available. As the basis for the present adaptation, a replication from https://github.com/johnb110/VDPython/ was used. 

* The original paper: https://arxiv.org/pdf/1801.01681
* Repository with original data: https://github.com/CGCL-codes/VulDeePecker

The Java adaptation was tested on two datasets:
* Juliet: https://samate.nist.gov/SRD/testsuite.php (mostly clean synthetic data)
* Project KB: https://sap.github.io/project-kb/ (real messy data)

VDP_Java uses the same approach as the original, but is adapted to work on Java source code. The program is set up in a way that facilitates experimantation and testing with different configurations. 


## VDP_Java
The folder includes the Python implementation of the system along with two sample source code files (juliet.txt and kb.txt) ready for training/testing. 

 To run program, use: `python vuldeepecker.py [gadget_file]`, where gadget_file is one of the text files containing a gadget set

* vuldeepecker.py
  * Interface to the project
  * Fetches each gadget, cleans, buffers, trains Word2Vec model, vectorizes, passes to neural network
  * Allows setting of multiple configurations to be tested
* clean_gadget.py
  * For each gadget, replaces all user variables with "VAR#" and user functions with "FUN#"
  * Removes content from string and character literals
* vectorize_gadget.py
  * Converts gadgets into vectors
  * Tokenizes gadgets
  * Uses Word2Vec to convert tokens to embeddings
  * Combines token embeddings in a gadget to create 2D gadget vector
* blstm.py
  * Defines Bidirectional Long Short Term Memory neural network for training/prediction of vulnerabilities
  * Gets gadget vectors as input
  * Implements functions for both training and testing the model


## The Datasets
The folder includes the two datasets used as well as a number of helper scripts used for the preparation of the datasets.


The premade subsets:
* juliet_full - full Juliet dataset
* juliet_100 - Juliet dataset with only vulnerabilities that appear at least 100 times
* juliet_1000 - Juliet dataset with only vulnerabilities that appear at least 1000 times
* KB - the full set of methods in project KB dataset