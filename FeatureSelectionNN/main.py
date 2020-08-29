import math
import copy


def NNClassifier(data, point, features, num_instances):
	# Compute distance from instance to OneOut

    #returnVal (which instance is the nearest neighbor)
    nearestNeighbor = 0
    
    curr_Min = float('inf')
    #first distance calculated will automatically take this values place
    for i in range(num_instances):
        if point == i: #we want to keep the principle of OneOut so pass the instance if it is same as OneOut
            pass
        else:
            distance = 0
            
            # EUCLID DISTANCE #
            for j in range(len(features)):
                #euclidean distance but not just x,y coordinates can do this for all the features
                distance = distance + pow((data[i][features[j]] - data[point][features[j]]), 2)
                
            distance = math.sqrt(distance)
            # # # # # # # # # #
             
            # CHECK curr_Min
            if distance < curr_Min:
                nearestNeighbor = i 
                curr_Min = distance
    
    return nearestNeighbor


def OneOutNN(data, features, num_instances):
	"""
	Evaluate Nearest Neighbor based on one-out algo
    
    Loop over all instances 
        set each instances as the "One Out"
        
        run nearest neighbor on "One Out" with rest of the data 
        
        check if nearest neighbor was correct
        
        add 0 for incorrect
        add 1 for correct
        
        divide sum / num_instances
    """
	correct = 0.0
	for i in range(num_instances):
		one_out = i

        #returns nearest neighbor
		neighbor = NNClassifier(data, one_out, features, num_instances)
        
        #let nearest neighbor vote on what the one_out label is
		if data[neighbor][0] == data[one_out][0]:
			correct = correct + 1 #if not correct then u add nothing (0)

	accuracy = (correct / num_instances) * 100

	return accuracy


def ForwardSelection(data, num_instances, num_features):
    """
    Start with 0 features and find the best subset of features that has the highest accuracy 
    
    use greedy algorithm to choose best feature to add
    """
	# 0 features => empty subset
    features_subset = []
    return_set = [] #subset of features to return that has the highest accuracy

    #accuracy associated with final subset to return
    max_accuracy = 0.0

    # slides say there are 2^n - 1 subsets of features with n features
    for i in range(num_features):
        feature_add = -1
        loc_feature_add = -1
        loc_acc = 0.0

        for j in range(1, num_features + 1):
            if j not in features_subset:
                #we will ignore j if it is in feature subset otherwise perform algorithm
                temp_set = copy.deepcopy(features_subset)
                #need deep copy of arrays in python
                #j is not in subset (proved by for loop)
                #we shall add j to feature subset and check accuracy
                temp_set.append(j)

                accuracy = OneOutNN(data, temp_set, num_instances)
                print '\tUsing feature(s) ', temp_set, 'accuracy is ', accuracy, '%'

                if accuracy > max_accuracy:
                    max_accuracy = accuracy
                    feature_add = j
                if accuracy > loc_acc:
                    loc_acc = accuracy
                    loc_feature_add = j

        if feature_add >= 0:
            features_subset.append(feature_add)
            return_set.append(feature_add)
            #tempAccCheck = OneOutNN(data, features_subset, num_instances)
            print '\n\nFeature set ', features_subset, ' was best, accuracy is ', max_accuracy, '%\n\n'
        else:
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
            features_subset.append(loc_feature_add)
            #tempAccCheck = OneOutNN(data, features_subset, num_instances)
            print 'Feature set ', features_subset, ' was best, accuracy is ', loc_acc, '%\n\n'

    print 'Finished search!! The best feature subset is ', return_set, ', which has an accuracy of ', max_accuracy, '%'


def BackwardElimination(data, num_instances, num_features, startAcc):
    """
    kind of like the opposite intuition of forward selection
    rather than start with no feature
    
    start with a set containing every feature 
    (we already calculated the accuracy for this set and is the default value for our max_accuracy)
    
    then greedy search and eliminate feature that will result in a more accurate feature set
    
    hopefully will get same set as forward selection
	"""

    # We Start with a feature set containing every feature
    features_subset = [i+1 for i in range(num_features)] #we don't want 0 feature - 1
    return_set = [i+1 for i in range(num_features)] #set of features we will return -> starts as default set

    #could just use one out validator but this is a value already calculated so why not use it
    max_accuracy = startAcc 
    #max_accuracy will ultimately represent the accuracy of our return set we want

    #again from lecture we know there is a 2^n -1 set of possible combination of features
    #   where n is the # of total features

    for i in range(num_features):
        rmv_feature = -1     
        loc_rmv_feature = -1 
        loc_acc = 0.0        

        #same intuition of forward selection

        for j in range(1, num_features + 1):
            if j in features_subset:
                temp_set = copy.deepcopy(features_subset)

                temp_set.remove(j)

                accuracy = OneOutNN(data, temp_set, num_instances)
                print '\tUsing feature(s) ', temp_set, ' accuracy is ', accuracy, '%'

                if accuracy >= max_accuracy:
                    max_accuracy = accuracy
                    rmv_feature = j
                if accuracy >= loc_acc:
                    loc_acc = accuracy
                    loc_rmv_feature = j

        if rmv_feature >= 0:
            features_subset.remove(rmv_feature)
            return_set.remove(rmv_feature)
            print '\n\nFeature set ', features_subset, ' was best, accuracy is ', max_accuracy, '%\n\n'
        else:
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
            features_subset.remove(loc_rmv_feature)
            print 'Feature set ', features_subset, ' was best, accuracy is ',  loc_acc, '%\n\n'

    print 'Finished search!! The best feature subset is ', return_set, ' which has an accuracy of ', max_accuracy, '%' 


def normalize(data, num_features, num_instances):
    """
    to normalize we willl take z-normalize equation from lecture slides

    z-normalize => X = (X - mean(X)) / std(X)
    returns normalized instances

    so for this data 
    returned normalized matrix will look like:
    normalized[i][j] = (instances[i][j] - mean[j-1]) / std[j-1] 

    mean[j-1]/std[j-1] => because first column goes to the label

    range(x to y) => starts from x and goes till y - 1
    but we want to go from 1 to num_features
    therefore => range(1, num_features+1)

    create mean array and std array (for each feature)
    """

    # MEAN ARRAY
    mean = []
    for i in range(1, num_features + 1):
        mean.append((sum(row[i] for row in data)) / num_instances)

    # STD ARRAY
    std = []
    for i in range(1, num_features + 1):
        variance = sum(pow((row[i] - mean[i-1]), 2) for row in data) / num_instances
        std.append(math.sqrt(variance))
        
    # Z NORMALIZE
    for i in range(0, num_instances): 
        for j in range(1, num_features + 1):
            data[i][j] = ((data[i][j] - mean[j-1]) / std[j-1])
   
	return data


def main():
    #start of simple menu
    print 'Welcome to Alex Thomas\'s Feature Selection Algorithm.'
    
    #prompt user for file and then open file of that type and store data
    file = raw_input('Type in the name of the file to test: ')
    
    """
    #FILE PROMPT CHECK
    print file
    """

    """
    We need to now read in the data 
    
    first column is class (either 1 or 2)
    following columns are the features
    
    instances # = # of lines
    feature # = # of items in one line - 1 (for class label)

    appears to be for the small data file: 10 features  
                      the large data file: 40 features

    but from the instructions:
        max # of features is 64
        max # of instances is 2048
    # 1 x x x x x x x x x x ... 
	# 2 x x x x x x x x x x ... 
    
	# Store data from file
	# Open file, error exception

    """
    try:
        data = open(file, 'r')
        #open the file and we are only reading hence the 'r'
    except:
        #if we can't find user inputted file then ->
        raise IOError('The file '+ file +' does not exist. Exiting program.')

	#find the # of features in this file
    #(Don't hardcode based on file)
    Line_1 = data.readline()
    num_features = len(Line_1.split()) - 1

    #we have read the first line so let's take the reader cursor back to the beginning 
    data.seek(0)

	# Read in all lines on file to get # instances 
    num_instances = sum(1 for line in data)



    #we now have # of features and instances in our file
    """
    TEST # READ
    
    print 'This data file has ', num_instances, ' with ', num_features, ' features.'
    """
    #return cursor to beginning again
    data.seek(0)

	# let's store data into array of arrays (matrix)
    data_matrix = [[] for i in range(num_instances)] #create a row for each instance
    for i in range(num_instances): #in each row read in the feature/label at each correct column
        data_matrix[i] = [float(j) for j in data.readline().split()]
    
    # data_matrix[x][0]=> classification label
    # data_matrix[x][1...num_features] => features 

    """
    TEST DATA READ
    
    for instance in data_matrix:
        print instance
    """
    
    print 'This dataset has ', num_features, ' features (not including the class attribute), with ', num_instances, ' instances.'

    print 'Please wait while I normalize the data...'
    
    
    # NORMALIZE DATA
    norm_data = normalize(data_matrix, num_features, num_instances)
    
    print 'Done!'

    """
    TEST NORM DATA READ

    for instance in data_matrix:
        print instance
    """

    # Algorithm selection
    print 'Type the number of the algorithm you want to run.'
    print '1. Forward Selection'
    print '2. Backward Elimination'
    #print '3. Alex\'s Special Algorithm #NOT IMPLEMENTED#'
    
    choice = int(raw_input())
    while (choice < 1 or choice > 2):
        print ('ERROR: algorithm selected not available, please pick a different algorithm.')
        choice = int(raw_input())

    """
    #ALGO PROMPT CHECK         
    if choice == 1:
        print 'option 1 chosen'
    else:
        print 'option 2 chosen'
    """

    #before picking algorithm first use nearest neighbor with the leaving one out evaluation

    all_features = []
    for i in range(1, num_features + 1):
        all_features.append(i)

    
    acc_perc = OneOutNN(norm_data, all_features, num_instances)

    print 'Running nearest neighbor with all ', num_features, ' features, using "leaving-one-out" evaluation, I get an accuracy of ', acc_perc, '%'

    print 'Beginning search.\n\n'

    if choice == 1:
        ForwardSelection(norm_data, num_instances, num_features)
    else: #(our for loop will ensure it is either 1 or 2)
        BackwardElimination(norm_data, num_instances, num_features, acc_perc)

if __name__ == '__main__':	
    main()