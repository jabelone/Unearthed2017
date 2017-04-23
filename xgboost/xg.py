#!/usr/bin/python
import numpy as np
import xgboost as xgb

### load data in do training
dtrain = xgb.DMatrix('svmTrain.txt')
dtest = xgb.DMatrix('svmTest.txt')
print(dtrain)
param = {'max_depth':200, 'eta':0.5, 'silent':1, 'objective':'reg:linear', 'eval_metric':'mae'}
watchlist  = [(dtest,'eval'), (dtrain,'train')]
num_round = 10
bst = xgb.train(param, dtrain, num_round, watchlist)

print ('start testing prediction from first n trees')

### predict using first 1 tree
label = dtest.get_label()
ypred1 = bst.predict(dtest, ntree_limit=1)

# by default, we predict using all the trees
ypred2 = bst.predict(dtest)

print ('error of ypred1=%f' % (np.sum((ypred1>0.5)!=label) /float(len(label))))
print ('error of ypred2=%f' % (np.sum((ypred2>0.5)!=label) /float(len(label))))