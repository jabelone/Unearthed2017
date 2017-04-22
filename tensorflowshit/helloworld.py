'''
HelloWorld example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf

import csv




def getNetGraph(X, h1size):
    with tf.name_scope('hidden'):
        weights = tf.random_normal([tf.size(X), h1size], name='weights')
        biases = tf.zeros([h1size], tf.float32)
        hidden1 = tf.nn.relu(tf.matmul(X, weights) + biases)
        
    with tf.name_scope('output'):
        weights = tf.random_normal([h1size, 1], name='weights')
        bias = tf.constant(0, name='bias', dtype=tf.float32)
        output = tf.Variable(tf.matmul(hidden1, weights) + bias)
    
    return output

def loss(X, target):
    #squared loss
    return tf.pow(X - target, 2)

def pruneRow(row, columnIndexes, targetColIndex):
    return ([row[index] for index in columnIndexes], row[targetColIndex])

featuresColNames = ['Casing Pressure',
                    'Gas Flow (Volume)',
                    'Motor Speed',
                    'Motor Torque',
                    'Pump Speed Actual',
                    'Tubing Flow Meter',
                    'Tubing Pressure',
                    'Water Flow Mag from Separator']
targetColName = 'Downhole Gauge Pressure'

with open('D:/unearthed/Bottom Hole Pressure and Fluid Level Challenge/Data/Well1B3mths.csv',
              newline='') as csvfile:

    csvreader = csv.reader(csvfile)

    allColNames = next(csvreader)
    featuresColIndexes = [allColNames.index(name) for name in featuresColNames]
    targetColIndex = allColNames.index(targetColName)

    print("feature column indexes", featuresColIndexes)
    print("target column index", targetColIndex)
    csvfile.close()

    learning_rate = 0.005
    learning_iterations = 1000
    hiddenLayerSize = 5

    trainX = [[1,2,3,4,5]]
    target = [[30]]

    targetPlaceholder = tf.placeholder(tf.float32, shape=[1,1])
    inputPlaceholder = tf.placeholder(tf.float32, shape = [1,len(featuresColIndexes)])
    netGraph = getNetGraph(inputPlaceholder, hiddenLayerSize)

    lossVal = loss(netGraph, targetPlaceholder)
    trainOp = tf.train.GradientDescentOptimizer(learning_rate).minimize(lossVal)

    sess = tf.Session()
    init = tf.global_variables_initializer()

    sess.run(init, feed_dict={inputPlaceholder: trainX, targetPlaceholder: target})

    for epoch in range(learning_iterations):
        sess.run(trainOp, feed_dict={inputPlaceholder: trainX, targetPlaceholder: target})

    print(sess.run(netGraph, feed_dict={inputPlaceholder: trainX, targetPlaceholder: target}))

    sess.close()


