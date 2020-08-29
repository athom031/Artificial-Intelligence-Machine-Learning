## Artifical Intelligence - Machine Learning

### Feature selection using Nearest Neighbor Classifier

<div align="center">
<img src="https://github.com/athom031/Artificial_Intelligence/blob/master/FeatureSelectionNN/feature_selection_example/80_features_3_5.png" width = "50%"/> 
</div><br/>


## Abstract

Given a feature set with N classified instances and M features, we want to find the feature subset that will best represent the dataset for future unclassified instances. This uses the Nearest Neighbor Classifier and One Out algorithm to measure each potential feature subset.
##### One Out Algorithm: 
Take one data point out and build a Nearest Neighbor classifier from the current feature subset. Then use this classifier to guess the one out point. We do this for every point to determine the accuracy of our current feature subset.
##### Feature Selection:
We select features one of two ways, either we start with no features (forward selection) or all features (backward selection). Then we simply greedily narrow it down to the most accurate subset of features (remember we evaluate accuracy with the one out algorithm.

## Getting Started

This is a python project that makes use of math and matplot libraries.<br/>
First install python on to your system. <br/>
[Mac Python 3 Download](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)


### Prerequisites

All modules used are default libraries of python.

### Compile

To select the features of a dataset:
```
python main.py
```	
It will ask for a txt file that holds the dataset in the current directory. <br/>

This data file should follow the following constraints: <br/>
``` 
each row is a data instance
each column is a feature
EXCEPT -> first column holds the class of each instance
``` 
In forward selection you will most likely get two features which you can plot with plot.py:
```
python plot.py
```

## Reflection

### Warnings

Though foward selection and backward selection will result in similar accurate feature subset, these subsets will not always be the same. <br/>
Forward selection will replicate the accuracy of backward selection with less features. <br/>
This makes the features picked by Backwards Selection harder to pick. <br/>
Backwards Selection also takes more time on larger datasets. 

[Example]("https://github.com/athom031/Artificial_Intelligence/tree/master/FeatureSelectionNN/feature_accuracy_example/")
