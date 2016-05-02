import math
import copy
import numpy as np
import scipy
import collections
import random
import time


def input_data(name, row, type_data):   #type_set=1 -- user_rating.txt  type_set=2 -- mc.txt type_set=3 -- rating.txt
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
        if type_data == 1:                  # judge which file the dataset belongs to 
            if '-1' in temp:            # if user do NOT trust other user, then delete that data
                i = i + 1
                continue
            else:
                for j in xrange(0, len(temp)):                      
                    if j < 2:
                        init_data[m-i, j] = temp[j]
                    elif j == 3:
                        date = str(temp[j]).split('/')
                        for x in xrange(0, len(date)):      #convert date to int_type
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
                if '\n' in temp:                #delete data contain ''
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
    return save_users, data_save2


def update_dataset(init_data, users_list, contents_list, dataset_type):
    final_data = np.zeros((len(init_data), 3))
    index = 0
    for i in xrange(0, len(init_data)):
        print "%d : %d" %(i, len(init_data))
        if dataset_type == 1:               # dataset_type = 1 means the init_user_rating.txt
            if init_data[i, 0] in users_list and init_data[i, 1] in users_list:
                for j in xrange(0, 3):
                    final_data[index, j] = init_data[i, j]
                index = index + 1
        elif dataset_type == 2:             # dataset_type = 2 means the init_mc.txt
            if init_data[i, 0] in contents_list and init_data[i, 1] in users_list:
                for j in xrange(0, 3):
                    final_data[index, j] = init_data[i, j]
                index = index + 1
    return final_data   

def data(filename, row):                # read the data from file
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
            if int(init_data[i, 0]) == 0:           # even there might be some useless options...
                break
            else:
                content_file.write(str(int(init_data[i, j])) + " ")
                if j == n - 1:
                    content_file.write('\n')
    
def split_rating(init_data):
    n = len(init_data)
    temp_article = []
    temp_day = []
    for i in xrange(0, n):
        temp_article.append(init_data[i, 0])
        temp_day.append(init_data[i, 3])
    COUNT = int(n*0.4)
    list_article = []
    list_index = []
    list_day = []
    list_all = range(0, n)
    counter = 0
    time_day = {}
    time_article = {}
    day = list(set(temp_day))
    article = list(set(temp_article))
    for i in xrange(0, len(day)):
        time_day[day[i]] = 0
    for i in xrange(0, len(article)):
        time_article[article[i]] = 0
    counter_day = collections.Counter(temp_day)
    counter_article = collections.Counter(temp_article)
    while counter <= COUNT:
        print counter, COUNT
        tempInt = random.randint(0, n-1)
        if tempInt not in list_index:
            if time_day[init_data[tempInt, 3]]+1 < counter_day[init_data[tempInt, 3]] and time_article[init_data[tempInt, 0]]+1 < counter_article[init_data[tempInt, 0]]:
                time_day[init_data[tempInt, 3]] = time_day[init_data[tempInt, 3]] + 1
                time_article[init_data[tempInt, 0]] = time_article[init_data[tempInt, 0]] + 1
                list_day.append(init_data[tempInt, 3])             
                list_index.append(tempInt)
                list_article.append(init_data[tempInt, 0])
                counter = counter + 1

    if len(article) == len(list(set(list_article))):
        print 'article satisfied'
    else:
        print 'article error'
        split_rating(init_data)
    data_refer = np.zeros((len(list_article), 6))
    data_exp = np.zeros((n - len(list_article), 6))
    index = 0
    for item in list_index:
        for j in xrange(0, 6):
            data_refer[index, j] = init_data[item, j]
        index = index + 1
    index = 0
    for item in list(set(list_all)-set(list_index)):
        for j in xrange(0, 6):
            data_exp[index, j] = init_data[item, j]
        index = index + 1
    print len(data_refer), len(data_exp)
    return data_refer, data_exp
    
def sort_date(init_data):
    n = len(init_data)
    date_list = []
    index_list = []
    new_data = np.zeros((n, 4))
    map(lambda i: date_list.append(init_data[i, 3]), [i for i in xrange(0, n)])
    temp = sorted(enumerate(date_list), key = lambda x : x[1])
    for item in temp:
        index_list.append(item[0])
    index = 0
    for item in index_list:
        new_data[index, :] = init_data[item, 0:4]
        index = index + 1
    return new_data
        
    
                            
            
        

def main():
    # file1 = str("dataset/user_rating.txt")
    # file2 = str("dataset/mc.txt")
    # file3 = str("dataset/rating.txt")
    # input_data(file1, 3, 1)
    # input_data(file2, 3, 2)
    # input_data(file3, 6, 3)
    # file_init1 = str("dataset/init_user_rating.txt")
    # file_init2 = str("dataset/init_mc.txt")
    # file_init3 = str("dataset/init_rating.txt")
    # to_process_contents = data(file_init3, 6)
    # contents_list, temp_contents = process_contents(to_process_contents)
    # users_list, temp_users = process_users(temp_contents)
    # while len(temp_contents) != len(temp_users):
    #     contents_list, temp_contents = process_contents(temp_users)
    #     users_list, temp_users = process_users(temp_contents)
    # print "process over!"
    # save_name1 = str("dataset/final_user_rating.txt")
    # save_name2 = str("dataset/final_mc.txt")
    # save_name3 = str("dataset/final_rating.txt")
    # write_data(temp_users, 6, save_name1)
    # data_set_1 = data(file_init1, 3)            # the user_rating.txt
    # data_set_2 = data(file_init2, 3)            # the mc.txt
    # temp_data_1 = update_dataset(data_set_1, users_list, contents_list, 1)      #update the users lists in dataset user_rating
    # write_data(temp_data_1, 3, save_name1)
    # temp_data_2 = update_dataset(data_set_2, users_list, contents_list, 2)      #update the users and contents lists in dataset mc
    # write_data(temp_data_2, 3, save_name2)
    file_process = str("dataset/final_rating.txt")
    file_result_refer = str("dataset/final_rating_refer.txt")
    file_result_exp = str("dataset/final_rating_exp.txt")
    rating_data = data(file_process, 6)
    data_refer, data_exp = split_rating(rating_data)
    write_data(data_refer, 6, file_result_refer)
    write_data(data_exp, 6, file_result_exp)
    sort_data = data(file_result_exp, 6)
    new_data = sort_date(sort_data)
    write_data(new_data, 4, file_result_exp)

    
    
if __name__ == '__main__': main()


