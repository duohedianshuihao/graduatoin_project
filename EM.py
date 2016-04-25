from __future__ import division
import math 
import numpy as np
import copy
import collections
import time

class Initialize(object):

    def __init__(self, file_mc, file_refer, file_exp):
         self.file_mc = file_mc
         self.file_refer = file_refer
         self.file_exp = file_exp

    def init_sim(self):
        article = []
        author = []
        category = []
        data = open(self.file_mc, 'r')
        for line in data:
            temp = str(line).split()
            article.append(temp[0])
            author.append(temp[1])
            category.append(temp[2])
        n = len(article)
        sim_dict = {}
        for i in xrange(0, n):
            sim_dict[article[i]] = i
        sim_result = np.zeros((n, n))
        for i in xrange(0, n):
            for j in xrange(0, n):
                if i == j: sim_result[i, j] = 1
                else: 
                    temp_result = 0
                    if author[i] == author[j]:
                        temp_result = temp_result+1
                    if category[i] == category[j] :
                        temp_result = temp_result+1
                    sim_result[i, j] = temp_result/2
        return sim_dict, sim_result     


    def init_k0(self):
        article_refer = []
        article_exp = []
        day_refer = []
        day = []
        data_refer = open(self.file_refer)
        for line in data_refer:
            temp = str(line).split()
            article_refer.append(temp[0])
            day_refer.append(temp[3])
            day.append(temp[3])
        data_exp = open(self.file_exp)
        for line in data_exp:
            temp = str(line).split()
            article_exp.append(temp[0])
            day.append(temp[3])
        day_count = collections.Counter(day)
        k0_result = np.zeros((len(set(article_exp)), len(set(day))))
        k0_dict = {}
        global day_dict 
        day_dict = {}
        index = 0
        for item in set(article_exp):       # generate the dict
            k0_dict[item] = index
            index = index + 1
        index = 0
        for item in set(day):
            day_dict[item] = index
            index = index + 1
        for i in xrange(0, len(article_refer)):         # counter article in day
            k0_result[k0_dict[article_refer[i]], day_dict[day_refer[i]]] = k0_result[k0_dict[article_refer[i]], day_dict[day_refer[i]]] + 1
        for days in set(day):
            for article in set(article_refer):
                k0_result[k0_dict[article], day_dict[days]] = k0_result[k0_dict[article], day_dict[days]]/day_count[days]  
                print k0_result[k0_dict[article], day_dict[days]], day_count[days], days   
                if k0_result[k0_dict[article], day_dict[days]] != 0:
                    time.sleep(0.1)     
        return k0_dict, k0_result

            
            

                                              







# def E_step():


# def C_step():


# def M_step():


# def write_result():

    
def main():
    initialize = Initialize('dataset/final_mc.txt', 'dataset/final_rating_refer.txt', 'dataset/final_rating_exp.txt')
    # sim_Dict, sim_O = initialize.init_sim()
    k0_Dict, k0 = initialize.init_k0()

if __name__ == '__main__':
    main()