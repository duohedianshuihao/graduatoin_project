import math
import copy
import numpy as np
import scipy
import collections
import time


def input_data(name, row, type_data):	#type_set=1 -- user_rating.txt	type_set=2 -- mc.txt type_set=3 -- rating.txt
	data = open(name, 'r')
	n = len(data.readlines())		 
	init_data = np.zeros((n, row))
	m = -1
	i = 0
	data = open(name, 'r')
	for line in data:
		m = m + 1
		if type_data == 2:
			temp = str(line).split('|')
		else:
			temp = str(line).split()
		if type_data == 1:					# judge which file the dataset belongs to 
			if '-1' in temp:			# if user do NOT trust other user, then delete that data
				i = i + 1
				continue
			else:
				for j in xrange(0, len(temp)):						
					if j < 2:
						init_data[m-i, j] = temp[j]
					elif j == 3:
						date = str(temp[j]).split('/')
						for x in xrange(0, len(date)):		#convert date to int_type
							date[x] = int(date[x])
						if date[1] == 1 or date[1]==3 or date[1]== 5 or date[1]== 7 or date[1]== 8 or date[1]== 10 or date[1]== 12:
							if date[0] == 2001 and date[1] == 1 and date[2] == 10:
								init_data[m-i, j-1] = (date[0]-2001)*365 + (date[1]-1)*31 + date[2]-10
							else: 
								init_data[m-i, j-1] = (date[0]-2001)*365 + (date[1]-1)*31 + date[2]-1
						elif date[1] == 2:
							init_data[m-i, j-1] = (date[0]-2001)*365 + (date[1]-1)*28 + date[2]-1 
						else:
							init_data[m-i, j-1] = (date[0]-2001)*365 +(date[1]-1)*30 + date[2]-1
					else:
						continue
		if type_data == 2:
			for j in range(0, len(temp)):	
				if '\n' in temp:				#delete data contain ''
					i = i + 1
					print m
					break
				init_data[m-i, j] = temp[j]
		if type_data == 3:
			for j in range(0, len(temp)):	
				if j < 3:
					init_data[m, j] = temp[j]
				elif j == 3 or j == 5:
					continue
				elif j == 4:
					date = str(temp[j]).split('/')
					for x in xrange(0, len(date)):
						date[x] = int(date[x])
					if date[1] == 1 or 3 or 5 or 7 or 8 or 10 or 12:
						if date[0] == 2001 and date[1] == 1 and date[2] == 10:
							init_data[m, j-1] = (date[0]-2001)*365 + (date[1]-1)*31 + date[2]-10
						else: 
							init_data[m, j-1] = (date[0]-2001)*365 + (date[1]-1)*31 + date[2]-1
					elif date[1] == 2:
						init_data[m, j-1] = (date[0]-2001)*365 + (date[1]-1)*28 + date[2]-1
					else:
						init_data[m, j-1] = (date[0]-2001)*365 +(date[1]-1)*30 + date[2]-1
				else: 
					init_data[m, j-2] = temp[j]
	if type_data == 1:
		file_str = "dataset/init_user_rating.txt"
	if type_data == 2:
		file_str = "dataset/init_mc.txt"
	if type_data == 3:
		file_str = "dataset/init_rating.txt"

	content_file = open(file_str, 'w')
	for i in xrange(0, len(init_data)):
		for j in xrange(0, row):
			content_file.write(str(int(init_data[i, j]))+' ')
			if j == row - 1:
				content_file.write('\n')

	

					
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
	return save

def update_user_list(save, name):
	users_len, users_data = input_data(name)
	temp_0 = []
 	for x in xrange(0, users_len):
		temp_0.append(users_data[x, 0])
	#users_list = set(temp_0)
	counter_users = collections.Counter(temp_0)
	n = 0 
	for item in save:
		if counter_users[item] > 0:
			n = n + counter_users[item]
	index = 0
	init_list1 = np.zeros((n, 3))
	for item in save:
		count = 0
		for i in xrange(0, users_len):
			if item == users_data[i, 0]:
				count = count + 1
				for j in xrange(0, 3):
					init_list1[index, j] = users_data[i, j]
				index = index + 1
				if count == counter_users[item]: break

	temp_1 = []
	for x in xrange(0, len(init_list1)):
		temp_1.append(init_list1[x, 1])
	#friends_list = set(temp_1)
	counter_friends = collections.Counter(temp_1)
	m = 0
	for item in save:
		if counter_friends[item] > 0:
			m = m + counter_friends[item]
	index = 0
	final_list = np.zeros((m, 3))
	for item in save:
		count = 0
		for i in xrange(0, len(init_list1)):
			if item == init_list1[i, 1]:
				count = count + 1
				for j in xrange(0, 3):
					final_list[index, j] = init_list1[i, j]
				index = index + 1
				if count == counter_friends[item]: break			

	content_file = open('users.txt', 'w')
	for i in xrange(0, len(final_list)):
		for j in xrange(0, 3):
			k = ''.join(str(int(final_list[i, j])))
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
file1 = str("dataset/user_rating.txt")
file2 = str("dataset/mc.txt")
file3 = str("dataset/rating.txt")
#input_data(file2, 3, 2)
#input_data(file1, 3, 1)
input_data(file3, 6, 3)
# init_len1, init_data1 = process_contents(init_len, init_data)
# save = process_users(init_len1, init_data1)
# update_user_list(save, file2)
