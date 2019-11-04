# !usr/bin/python
# coding=utf-8

import os
import base64
from glob import glob
from mutagen import File

sonant = u'\u3099'
half_sonant = u'\u309a'

key_sonant =   'かきくけこさしすせそたちつてとはひふへほ' + \
			   'カキクケコサシスセソタチツテトハヒフヘホ'
key_half_sonant =   'はひふへほハヒフヘホ'
value_sonant = 'がぎぐげござじずぜぞだぢづでどばびぶべぼ' + \
			   'ガギグゲゴザジズゼゾダヂヅデドバビブベボ'
value_half_sonant = 'ぱぴぷぺぽパピプペポ'

convert_dict = {}
for k in range(len(key_sonant)):
	convert_dict[key_sonant[k] + sonant] = value_sonant[k]

for k in range(len(key_half_sonant)):
	convert_dict[key_half_sonant[k] + half_sonant] = value_half_sonant[k]


def han2zen(content):
	for k, v in convert_dict.items():
		if k in content:
			content = content.replace(k, v)
	return content

def strQ2B(ustring):
	"""把字符串全角转半角"""
	ss = []
	for s in ustring:
		rstring = ""
		for uchar in s:
			inside_code = ord(uchar)
			if inside_code == 12288:  # 全角空格直接转换
				inside_code = 32
			elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
				inside_code -= 65248
			rstring += chr(inside_code)
		ss.append(rstring)
	return ''.join(ss)

def strB2Q(ustring):
	"""把字符串全角转半角"""
	ss = []
	for s in ustring:
		rstring = ""
		for uchar in s:
			inside_code = ord(uchar)
			if inside_code == 32:  # 全角空格直接转换
				inside_code = 12288
			elif (inside_code >= 33 and inside_code <= 126):  # 全角字符（除空格）根据关系转化
				inside_code += 65248
			rstring += chr(inside_code)
		ss.append(rstring)
	return ''.join(ss)

def symbolFilter(content):
	symbol = '"\'“”，,.'
	result = ''
	for i in content:
		i = i.strip()
		if i and i not in symbol:
			result = result + i
	return result

def formatFilename(content):
	content = han2zen(content)
	content = strQ2B(content)
	return symbolFilter(content)

def getSqlFilename(filename):
	filename = os.path.basename(filename)
	# return os.path.splitext(filename)[0]
	fn = os.path.splitext(filename)[0]
	fn = formatFilename(fn)
	return base64.b64encode(fn.encode()).decode()

def unique_id(filename):
	f = File(filename)
	if 'APIC:' in f: del f['APIC:']
	if 'COMM::XXX' in f: del f['COMM::XXX']
	keys = list(f.keys())
	keys.sort()
	value = ''
	for k in keys:
		v = [str(i) for i in f[k].text]
		v.sort()
		value = value + '%s;'%(','.join(v))
	value = base64.b64encode(value.encode()).decode()
	return value

def unique_file(dirname):
	totalSet = set()
	fileList = glob(dirname + '/*.mp3')
	for i in fileList:
		uid = unique_id(i)
		print(uid)
		if uid in totalSet:
			print(i)
		totalSet.add(uid)

if __name__ == '__main__':
	unique_file('/mnt/d/CloudMusic')