'''
HelloWorld example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf

import csv

inputVarNum = 10


def getNetGraph(X, h1size):
    with tf.name_scope('hidden'):
        weights = tf.random_normal([tf.size(X), h1size], name='weights')
        biases = tf.zeros([h1size], tf.float32)
        hidden1 = tf.nn.relu(tf.matmul(X, weights) + biases)
        print("hidden1", hidden1)
        
    with tf.name_scope('output'):
        weights = tf.random_normal([h1size, 1], name='weights')
        print("weightmatrix", weights)
        bias = tf.constant(0, name='bias', dtype=tf.float32)
        output = tf.Variable(tf.matmul(hidden1, weights) + bias)
    
    return output

def loss(X, target):
    #squared loss
    return tf.pow(X - target, 2)


def main():
    inputVarNum = 5
    learning_rate = 0.05
    trainX = tf.Variable([[1,1,1,1,1]], dtype=tf.float32)
    targetVal = tf.constant(30, dtype=tf.float32)
    
    
    inputPlaceholder = tf.constant([[1,2,3,4,5]], dtype=tf.float32, name='input')
    netGraph = getNetGraph(inputPlaceholder, 5)
    
    lossVal = loss(netGraph, targetVal)
    trainOp = tf.train.GradientDescentOptimizer(learning_rate).minimize(lossVal)
    
    global sess
    sess = tf.Session()
    init = tf.global_variables_initializer()
    
    sess.run(init)
    
    for epoch in range(1000):
        sess.run(trainOp)
        
        
    print(sess.run(netGraph))
    
    sess.close()
    
main()