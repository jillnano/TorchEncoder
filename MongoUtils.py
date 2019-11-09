# !usr/bin/python
# coding=utf-8

import pymongo

class MongoUtils(object):
	def __init__(self, *args, **kwargs):
		self.mongoConn = pymongo.MongoClient(host = ['localhost:27017'], connect = False, socketTimeoutMS = 30000)
		self.mongoDb = self.mongoConn['admin']
		self.mongoDb.authenticate('torch', 'torch@mongo')
		self.mongoDb = self.mongoConn['torch']

	def findMusicList(self, playlist_id):
		resultList = []
		midList = self.mongoDb['playlist'].find_one({'playlist_id': playlist_id}, {'_id': 0, 'musicList': 1})['musicList']
		for mid in midList:
			resultList.append(self.findMusic(mid))
		return resultList

	def findMusic(self, mid):
		ret = self.mongoDb['music'].find_one({'mid': mid}, {'_id': 0})
		return ret

	def updateMusic(self, mid, data):
		self.mongoDb['music'].update_one({'mid': mid}, {'$set': data})

if __name__ == '__main__':
	MongoUtils().findMusicList()