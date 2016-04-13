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

					
def process_contents(init_data):
	temp = []
	for x in xrange(0,len(init_data)):
		temp.append(init_data[x, 0])
	contents = set(temp)
	contents = list(contents)
	save_content = []
	counter = collections.Counter(temp)
	n = 0
	for item in contents:
		if counter[item] >= 200:
			save_content.append(item)
			n = n + counter[item]
	data_save1 = np.zeros((n, 6))	
	index = 0
	for i in xrange(0, len(init_data)):
		print "%d : %d" %(i, len(init_data))
		if counter[init_data[i, 0]] >= 200:
			for j in xrange(0, 6):
				data_save1[index, j] = init_data[i, j]
			index = index + 1
	# for item in save_content:
	# 	count = 0
	# 	print format(count/len(save_content), '.2%')
	# 	for i in xrange(0, len(init_data)):
	# 		if init_data[i, 0] == item:
	# 			count = count + 1
	# 			for j in xrange(0, 6):
	# 				data_save1[index, j] = init_data[i, j]
	# 			index = index + 1
	# 			if count == counter[item] : break
	# content_file = open('dataset/temp_rating.txt', 'w')
	# for i in xrange(0, len(init_data1)):
	# 	for j in xrange(0, 6):
	# 		content_file.write(str(int(data_save1[i, j])) + " ")
	# 		if j == 5:
	# 			content_file.write('\n')
	return save_content, data_save1

def process_users(init_data):
	temp = []
	for x in xrange(0,len(init_data)):
		temp.append(init_data[x, 1])
	users = set(temp)
	users = list(users)
	save_users = []
	counter = collections.Counter(temp)
	n = 0
	for item in users:
		if counter[item] >= 10:
			save_users.append(item)
			n = n + counter[item]
	data_save2 = np.zeros((n, 6))	
	index = 0
	for i in xrange(0, len(init_data)):
		print "%d : %d" %(i, len(init_data))
		if counter[init_data[i, 1]] >= 10:
			for j in xrange(0, 6):
				data_save2[index, j] = init_data[i, j]
			index = index + 1
	# for item in save_users:
	# 	count = 0
	# 	for i in xrange(0, len(init_data)):
	# 		if item == init_data[i, 1] :
	# 			count = count + 1
	# 			print item
	# 			for j in xrange(0, 6):
	# 				init_data1[index, j] = init_data[i, j]
	# 			index = index + 1
	# 			if count == counter[item] : break

	# content_file = open('data.txt', 'w')
	# for i in xrange(0, len(data_save2)):
	# 	for j in xrange(0, 3):
	# 		k = ''.join(str(int(data_save2[i, j])))
	# 		content_file.write(k+' ')
	# 		if j == 2:
	# 			content_file.write('\n')
	return save_users, data_save2

def update_user_list(save, name):
	users_len, users_data = input_data(name)
	temp_0 = []
 	for x in xrange(0, users_len):
		temp_0.append(users_data[x, 0])
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

			

		

def data(filename, row):
	data_file = open(filename, 'r')
	n = len(data_file.readlines())
	data = np.zeros((n, row))
	m = -1
	data_file = open(filename, 'r')
	for line in data_file:
		m = m + 1
		temp = str(line).split()
		for j in range(0, row):
			data[m, j] = temp[j]
	return data

def write_data(init_data, n, filename):
	content_file = open(filename, 'w')
	for i in xrange(0, len(init_data)):
		for j in xrange(0, n):
			content_file.write(str(int(init_data[i, j])) + " ")
			if j == n - 1:
				content_file.write('\n')
	

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

def main():
	file1 = str("dataset/user_rating.txt")
	file2 = str("dataset/mc.txt")
	file3 = str("dataset/rating.txt")
	# input_data(file1, 3, 1)
	# input_data(file2, 3, 2)
	# input_data(file3, 6, 3)
	file_init1 = str("dataset/init_user_rating.txt")
	file_init2 = str("dataset/init_mc.txt")
	file_init3 = str("dataset/init_rating.txt")
	file_init4 = str("dataset/temp_rating.txt")
	to_process_contents = data(file_init3, 6)
	contents_list, temp_contents = process_contents(to_process_contents)
	users_list, temp_users = process_users(temp_contents)
	while len(temp_contents) != len(temp_users):
		contents_list, temp_contents = process_contents(temp_users)
		users_list, temp_users = process_users(temp_contents)
	print "process over!"
	save_name1 = str("dataset/final_rating.txt")
	save_name2 = str("dataset/final_contents_list.txt")
	save_name3 = str("dataset/final_users_list.txt")
	write_data(temp_users, 6, save_name1)
	#write_data(contents_list, 1, save_name2)
	#write_data(users_list, 1, save_name3)




if __name__ == '__main__': main()


