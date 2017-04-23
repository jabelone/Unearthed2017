'''
HelloWorld example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf

import csv
import time



def getNetGraph(X, h1size):
    h1_weights = tf.Variable(tf.random_normal([tf.size(X), h1size]), name='h1_weights')
    h1_weights = tf.Print(h1_weights, [h1_weights])
    h1_biases = tf.Variable(tf.zeros([1, h1size], tf.float32), name='h1_biases')
    h1_preactivation = tf.Variable(tf.add(tf.matmul(X, h1_weights), h1_biases), name='h1_preactivation')
    hidden1 = tf.nn.relu(h1_preactivation)

    out_weights = tf.Variable(tf.random_normal([h1size, 1]), name='out_weights')
    out_bias = tf.Variable(0.00, tf.float32, name='out_bias')
    output = tf.matmul(hidden1, out_weights) + out_bias
    
    return output

def loss(X, target):
    #abs loss
    difference = target - X
#    difference = tf.Print(difference, [difference])
    return tf.abs(difference)

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

with open('D:/UnearthedWellData/Well1B3mths.csv',
              newline='') as csvFile:

    csvReader = csv.reader(csvFile)

    allColNames = next(csvReader)
    featuresColIndexes = [allColNames.index(name) for name in featuresColNames]
    targetColIndex = allColNames.index(targetColName)

    print("feature column indexes", featuresColIndexes)
    print("target column index", targetColIndex)

    learning_rate = 0.01
    learning_iterations = 100
    hiddenLayerSize = 8
    
#    trainingSet = [pruneRow(next(csvReader), featuresColIndexes, targetColIndex)
#                   for i in range(100)]
    
    
    trainX = [[1,2,3,4,5,6,7,8]]
    target = [[30]]

#    tf.set_random_seed(time.time())
    
    targetPlaceholder = tf.placeholder(tf.float32, shape=[1,1], name='phTarget')
    inputPlaceholder = tf.placeholder(tf.float32, shape = [1,len(featuresColIndexes)], name='phIn')
    netGraph = getNetGraph(inputPlaceholder, hiddenLayerSize)

    lossVal = loss(netGraph, targetPlaceholder)
    trainOp = tf.train.GradientDescentOptimizer(learning_rate).minimize(lossVal)

    sess = tf.Session()
    init = tf.global_variables_initializer()

    sess.run(init, feed_dict={inputPlaceholder: trainX, targetPlaceholder: target})
    
    testSet = []
    
#    TensorBoard
    writer = tf.summary.FileWriter('./wadoo', sess.graph)

    x = 0
    for line in csvReader:
        x = x + 1
        if x > 10: break
        pruned = pruneRow(line, featuresColIndexes, targetColIndex)
        
        if (x % 2 == 1):
            testSet.append(pruned)
        else:
            sess.run(trainOp, feed_dict={inputPlaceholder: [pruned[0]],
                                         targetPlaceholder: [[pruned[1]]]})
        
#        print("Train row " + str(i) + ":", pruned)
#        for epoch in range(learning_iterations):
#        print(sess.run(lossVal, feed_dict={inputPlaceholder: [pruned[0]],
#                                         targetPlaceholder: [[pruned[1]]]}))

    for i in range(100):
        testRow = testSet[i]
        print ("Test Row " + str(i) + ":", testRow[1])
        print(sess.run(netGraph, feed_dict={inputPlaceholder: [testRow[0]]}))

    sess.close()


