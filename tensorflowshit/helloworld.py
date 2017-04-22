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
        biases = tf.Variable(tf.zeros([h1size]), name='biases')
        hidden1 = tf.nn.relu(tf.matmul(X, weights) + biases)
        
    with tf.name_scope('output'):
        weights = tf.random_normal([h1size], name='weights')
        bias = tf.Variable(0, name='bias', dtype=tf.float32)
        output = tf.Variable((hidden1 * weights) + bias)
    
    return output

def loss(X, target):
    #squared loss
    return tf.pow(X - target, 2)


def main():
    inputVarNum = 5
    learning_rate = 0.05
    trainX = tf.expand_dims(tf.Variable([1.0, 2.0, 3.0, 4.0, 5.0], dtype=tf.float32), 0)
    targetVal = tf.constant(0, dtype=tf.float32)
    
    
    inputPlaceholder = tf.placeholder(tf.float32, shape=[5])
    netGraph = getNetGraph(inputPlaceholder, 5)
    
    lossVal = loss(netGraph, targetVal)
    trainOp = tf.train.GradientDescentOptimizer(learning_rate).minimize(lossVal)
    
    global sess
    sess = tf.Session()
    init = tf.global_variables_initializer()
    
    sess.run(init)
#    
#    for epoch in range(10):
#        sess.run(trainOp, feed_dict={inputPlaceholder : trainX})
#        
        
    print(sess.run(netGraph, {inputPlaceholder: trainX}))
    
    sess.close()
    
main()