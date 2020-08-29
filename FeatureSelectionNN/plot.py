import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

def normalize(data, num_features, num_instances):

    mean = []
    for i in range(1, num_features + 1):
        mean.append((sum(row[i] for row in data)) / num_instances)

    std = []
    for i in range(1, num_features + 1):
        variance = sum(pow((row[i] - mean[i-1]), 2) for row in data) / num_instances
        std.append(math.sqrt(variance))
        
    for i in range(0, num_instances): 
        for j in range(1, num_features + 1):
            data[i][j] = ((data[i][j] - mean[j-1]) / std[j-1])
   
	return data


def main():
    print 'Welcome to Alex Thomas\'s Plotter.'
    file = raw_input('Type in the name of the file to test: ')
    try:
        data = open(file, 'r')
    except:
        raise IOError('The file '+ file +' does not exist. Exiting program.')

    Line_1 = data.readline()
    num_features = len(Line_1.split()) - 1

    data.seek(0)
    num_instances = sum(1 for line in data)

    data.seek(0)
    
    data_matrix = [[] for i in range(num_instances)] #create a row for each instance
    for i in range(num_instances): #in each row read in the feature/label at each correct column
        data_matrix[i] = [float(j) for j in data.readline().split()]
    
    
    print 'This dataset has ', num_features, ' features (not including the class attribute), with ', num_instances, ' instances.'

    print 'Please wait while I normalize the data...'
    
    
    # NORMALIZE DATA
    norm_data = normalize(data_matrix, num_features, num_instances)
    
    print 'Done!'

    # x = feature/index 1 
    # y = feature/index 5
    # label = index 0
    # color = ['red', 'blue']

    label = []
    for i in range(num_instances):
        label.append(norm_data[i][0])
    
    x_index = raw_input('Which feature do you want to be the x_index: ')
    x_index = int(x_index)
    x = []
    for i in range(num_instances):
        x.append(norm_data[i][x_index])
    
    y_index = raw_input('Which feature do you want to be the y_index: ')
    y_index = int(y_index)
    y = []
    for i in range(num_instances):
        y.append(norm_data[i][y_index])

    colors = ['red', 'blue']

    fig = plt.figure(figsize=(8,8))
    plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))

    title = str(file) + ' instances'
    plt.title(title)

    xlabel = 'Feature ' + str(x_index)
    plt.xlabel(xlabel)

    ylabel = 'Feature ' + str(y_index) 
    plt.ylabel(ylabel)

    cb = plt.colorbar()
    loc = np.arange(0,max(label),max(label)/float(len(colors)))
    cb.set_ticks(loc)
    cb.set_ticklabels(colors)

    plt.show()

if __name__ == '__main__':	
    main()