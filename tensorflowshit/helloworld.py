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



learning_rate = 0.005
hiddenLayerSize = 5

trainX = tf.constant([[1,1,1,1,1]], dtype=tf.float32, shape=[1,5], name='input')
targetVal = tf.constant(30, dtype=tf.float32)


inputPlaceholder = tf.placeholder(tf.float32, shape = [1,5])
netGraph = getNetGraph(inputPlaceholder, hiddenLayerSize)

lossVal = loss(netGraph, targetVal)
trainOp = tf.train.GradientDescentOptimizer(learning_rate).minimize(lossVal)

global sess
sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init, feed_dict={inputPlaceholder: [[1,2,3,4,5]]})
#
#for epoch in range(1000):
#    sess.run(trainOp, feed_dict={inputPlaceholder: trainX})


print(sess.run(netGraph, feed_dict={inputPlaceholder: [[1,2,3,4,5]]}))

sess.close()
    

