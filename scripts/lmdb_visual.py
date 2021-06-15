#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Brief:   caffe lmdb visual
# @Author:  qinhj@lsec.cc.ac.cn
# @Usage:   python lmdb_visual.py
# @Reference: http://deepdish.io/2015/04/28/creating-lmdb-in-python/

import lmdb
import caffe
import numpy as np
import cv2
#from matplotlib import pyplot

env = lmdb.open("trainval_lmdb", readonly=True)
txn = env.begin()
cur = txn.cursor()
## caffe data struct
datum = caffe.proto.caffe_pb2.Datum()

for key, value in cur:
    ## deserialize caffe datum object
    datum.ParseFromString(value)
    #print("channel:", datum.channels)
    
    label = datum.label
    data = caffe.io.datum_to_array(datum)
    #print("shape:", data.shape)
    
    ## chw -> hwc for cv2
    image = np.transpose(data, (1,2,0))
    cv2.imshow(str(label), image)
    if (27 == cv2.waitKey(0)): break
    """
    flat_x = np.fromstring(datum.data, dtype=np.uint8)
    x = flat_x.reshape(datum.channels, datum.height, datum.width)
    fig = pyplot.figure()
    pyplot.imshow(x, cmap='gray')
    """

cv2.destoyAllWindows()
env.close()
