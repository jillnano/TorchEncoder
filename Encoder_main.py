# !usr/bin/python
# coding=utf-8

import sys
import copy
import numpy as np
from pandas.io.json import json_normalize
from sklearn.preprocessing import MinMaxScaler

from TorchPeak import getSampleData
from Encoder_tf import predict_data
from MongoUtils import MongoUtils

Order = ['mid', 'mean_0', 'std_0', 'max_0', 'min_0', 'mean_1', 'std_1', 'max_1', 'min_1', 'mean_2', 'std_2', 'max_2', 'min_2']

if __name__ == '__main__':
	mongo = MongoUtils()
	# playlist_id = sys.argv[1].strip()
	playlist_id = '112545205'
	filename = mongo.findMusicList(playlist_id)
	# filename = [{'filename': '/mnt/d/__odyssey__/TorchEncoder/music/484249937.mp3', 'mid': '484249937'}]
	sampleList = []
	for idx, d in enumerate(filename):
		print('sample:', idx, d['mid'])
		if len(set(Order) - set(d.keys())) > 0:
			sample = getSampleData(d['filename'], d['mid'])
			s = copy.deepcopy(sample)
			del s['mid']
			mongo.updateMusic(d['mid'], s)
		else:
			sample = {}
			for k in Order:
				sample[k] = d[k]
		sampleList.append(sample)
	sample_data = json_normalize(sampleList)[Order]
	filenameList = sample_data.mid
	sample_data = sample_data.drop(['mid'], axis = 1)
	scaler = MinMaxScaler()
	total_X = scaler.fit_transform(np.array(sample_data, dtype = float))
	result = predict_data(total_X)
	# result_data = []
	for idx, fn in enumerate(filename):
		print('encode:', idx, fn['mid'])
		encode_data = {'encode_1': float(result[idx][0]), 'encode_2': float(result[idx][1])}
		mongo.updateMusic(fn['mid'], encode_data)

	# 	result_data.append(fn)
	# print(json.dumps(result_data))
