import math
import copy
import numpy as np
import scipy
import collections
import time


def input_data():
	data = open("ratings_data.txt", 'r')
	n = len(data.readlines())
	init_data = np.zeros((n, 3))
	m = -1
	data = open("ratings_data.txt", 'r')
	for line in data:
		m = m + 1
		temp = str(line).split()
		for j in range(0, 3):
			init_data[m, j] = temp[j]
	return n, init_data

def process_contents(n, init_data):
	temp = []
	for x in xrange(0,len(init_data)):
		temp.append(init_data[x, 1])
	contents = set(temp)
	contents = list(contents)
	save = []
	counter = collections.Counter(temp)
	n = 0
	for item in contents:
		if counter[item] >= 200:
			save.append(item)
			n = n + counter[item]
	index = 0
	init_data1 = np.zeros((n, 3))	
	for item in save:
		count = 0
		for i in xrange(0, len(init_data)):
			if item == init_data[i, 1] :
				count = count + 1
				print item
				for j in xrange(0, 3):
					init_data1[index, j] = init_data[i, j]
				index = index + 1
				if count == counter[item] : break
	return len(init_data1), init_data1

def process_users(n, init_data):
	temp = []
	for x in xrange(0,len(init_data)):
		temp.append(init_data[x, 0])
	users = set(temp)
	users = list(users)
	save = []
	counter = collections.Counter(temp)
	n = 0
	for item in users:
		if counter[item] >= 10:
			save.append(item)
			n = n + counter[item]
	index = 0
	init_data1 = np.zeros((n, 3))	
	for item in save:
		count = 0
		for i in xrange(0, len(init_data)):
			if item == init_data[i, 0] :
				count = count + 1
				print item
				for j in xrange(0, 3):
					init_data1[index, j] = init_data[i, j]
				index = index + 1
				if count == counter[item] : break

	content_file = open('data.txt', 'w')
	for i in xrange(0, len(init_data1)):
		for j in xrange(0, 3):
			k = ''.join(str(int(init_data1[i, j])))
			content_file.write(k+' ')
			if j == 2:
				content_file.write('\n')


		

def data():
	data_file = open("data.txt", 'r')
	n = len(data_file.readlines())
	data = np.zeros((n, 3))
	m = -1
	data_file = open("data.txt", 'r')
	for line in data_file:
		m = m + 1
		temp = str(line).split()
		for j in range(0, 3):
			data[m, j] = temp[j]
	return n, data

# def Soc_inf(Arfa, Ru, ):
# 	# lamuda

# def Ext_inf():
# 	pass

# def int_inf():
# 	pass

# def E_step():
# 	return #E(x)

# def C_step():
# 	return # Unknown

# def M_step():
# 	return #L'(seita) = 0 

# init_len, init_data = input_data()
# init_len1, init_data1 = process_contents(init_len, init_data)
# process_users(init_len1, init_data1)
n, array = data()
print n
print array