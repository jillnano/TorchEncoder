# !usr/bin/python
# coding=utf-8

import os
import sys
import json
import numpy as np
from pandas.io.json import json_normalize
from sklearn.preprocessing import MinMaxScaler

from TorchPeak import getSampleData
from Encoder_tf import predict_data

Order = ['filename', 'mean_0', 'std_0', 'max_0', 'min_0', 'mean_1', 'std_1', 'max_1', 'min_1', 'mean_2', 'std_2', 'max_2', 'min_2']

if __name__ == '__main__':
	filename = open(sys.argv[1].strip(), 'r').readlines()
	filename = [i.strip() for i in filename]
	filename = filter(lambda x: x, filename)
	filename = [os.path.abspath(i) for i in filename]
	sampleList = []
	for fn in filename:
		sample = getSampleData(fn, os.path.basename(fn))
		sampleList.append(sample)
	sample_data = json_normalize(sampleList)[Order]
	filenameList = sample_data.filename
	sample_data = sample_data.drop(['filename'], axis = 1)
	scaler = MinMaxScaler()
	total_X = scaler.fit_transform(np.array(sample_data, dtype = float))
	result = predict_data(total_X)
	result_data = []
	for idx, fn in enumerate(filename):
		result_data.append({'filename': fn, 'encode_1': float(result[idx][0]), 'encode_2': float(result[idx][1])})
	print(json.dumps(result_data))
