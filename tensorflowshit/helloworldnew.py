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
    with tf.name_scope('hidden'):
        weights = tf.Variable(tf.random_normal([tf.size(X), h1size]), name='weights')
        biases = tf.Variable(tf.zeros([1, h1size], tf.float32), name='biases')
        hidden1 = tf.matmul(X, weights) + biases

    with tf.name_scope('output'):
        weights = tf.Variable(tf.random_normal([h1size, 1]), name='weights')
#        weights = tf.Print(weights, [weights])
        bias = tf.Variable(0.00, tf.float32, name='bias')
        output = tf.matmul(hidden1, weights) + bias
    
    return output

def loss(X, target):
    #abs loss
    return tf.abs(target - X)

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

with open('D:/UnearthedWellData/Well1C3mths.csv',
              newline='') as csvFile:

    csvReader = csv.reader(csvFile)

    allColNames = next(csvReader)
    featuresColIndexes = [allColNames.index(name) for name in featuresColNames]
    targetColIndex = allColNames.index(targetColName)

    print("feature column indexes", featuresColIndexes)
    print("target column index", targetColIndex)

    learning_rate = 0.0001
    learning_iterations = 100
    hiddenLayerSize = 8
    
#    trainingSet = [pruneRow(next(csvReader), featuresColIndexes, targetColIndex)
#                   for i in range(100)]
    
    
    trainX = [[1,2,3,4,5,6,7,8]]
    target = [[30]]

    tf.set_random_seed(time.time())
    
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
        if x > 15000: pass
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

    for i in range(1000):
        testRow = testSet[i]
        print ("Test Row " + str(i) + ":", testRow[1])
        print(sess.run(netGraph, feed_dict={inputPlaceholder: [testRow[0]]}))

    sess.close()


