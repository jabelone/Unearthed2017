'''
A Multilayer Perceptron implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
import csv

# Parameters
learning_rate = 0.001
training_epochs = 1
batch_size = 100
display_step = 1

# Network Parameters
n_hidden_1 = 8 # 1st layer number of features
n_input = 8 # MNIST data input (img shape: 28*28)
n_classes = 1


# tf Graph input
x = tf.placeholder("float", [None, n_input], name='x')
y = tf.placeholder("float", [None, 1], name='y')


# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_1, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, 1]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([1]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = tf.pow(tf.subtract(y, pred), 2)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

def pruneRow(row, columnIndexes, targetColIndex):
    prunedRow = [0 if row[index] == 'NULL' else row[index] for index in columnIndexes]
    return (prunedRow, row[targetColIndex])

featuresColNames = ['Casing Pressure',
                    'Gas Flow (Volume)',
                    'Motor Speed',
                    'Motor Torque',
                    'Pump Speed Actual',
                    'Tubing Flow Meter',
                    'Tubing Pressure',
                    'Water Flow Mag from Separator']
targetColName = 'Downhole Gauge Pressure'

csvFile = open('D:/UnearthedWellData/Well1B3mths.csv',
              newline='')

csvReader = csv.reader(csvFile)

allColNames = next(csvReader)
featuresColIndexes = [allColNames.index(name) for name in featuresColNames]
targetColIndex = allColNames.index(targetColName)

csvFile.close()
    
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    testSet = []
    
    # Training cycle
    for epoch in range(training_epochs):
        with open('~/yourdata/UnearthedWellData/Well1B3mths.csv',
              newline='') as csvFile: 
            csvReader = csv.reader(csvFile)
            next(csvReader) #skip header         
            avg_cost = 0.
            rowNum = 0
            for line in csvReader:  
                rowNum += 1
                if rowNum > 10000: break
                    
                pruned = pruneRow(line, featuresColIndexes, targetColIndex)
                if (rowNum % 2) == 0: testSet.append(pruned)
                
                batch_x, batch_y = pruned
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost], feed_dict={x: [batch_x],
                                                              y: [[batch_y]]})
#                # Compute average loss
#                avg_cost += c / (rowNum/2)
#            # Display logs per epoch step
#            if epoch % display_step == 0:
#                print("Epoch:", '%04d' % (epoch+1), "cost=", \
#                    "{:.9f}".format(avg_cost))
    print("Optimization Finished!")

    testLen = len(testSet)
    totalCost = 0.0
    for i in range(testLen):
        testRow = testSet[i]
        batch_x, batch_y = testRow
#        print ("Test Row " + str(i) + ":", batch_y)
        totalCost += sess.run(cost, feed_dict={x: [batch_x], y: [[batch_y]]})[0][0]
    print("Average Cost over {} rows is {}".format(testLen, totalCost/testLen))
    
    # Test model
#    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
#    # Calculate accuracy
#    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
#    print("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
    