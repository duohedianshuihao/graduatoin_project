from __future__ import division
from multiprocessing import Pool
import random
import math 
import numpy as np
import copy
import collections
import time


class Initialize(object):

    def __init__(self, file_mc, file_refer, file_exp, file_users):
         self.file_mc = file_mc
         self.file_refer = file_refer
         self.file_exp = file_exp
         self.file_users = file_users

    def init_sim(self):
        print 'initialize sim'
        article = []
        author = []
        category = []
        article_dict = []
        data = open(self.file_mc, 'r')
        for line in data:
            temp = str(line).split()
            article.append(int(temp[0]))
            author.append(int(temp[1]))
            category.append(int(temp[2]))
        data = open(self.file_exp, 'r')
        for line in data:
            temp = str(line).split()
            article_dict.append(int(temp[0]))
        n = len(list(set(article_dict)))
        sim_dict = {}       # use the ID of article to locate the position
        index = 0
        for item in set(article_dict):
            sim_dict[item] = index
            index += 1 
        sim_result = np.zeros((n, n))
        for i in xrange(0, len(author)):
            for j in xrange(0, len(category)):
                if i == j: sim_result[i, j] = 1
                else: 
                    temp_result = 0
                    if author[i] == author[j]:
                        temp_result = temp_result+1
                    if category[i] == category[j] :
                        temp_result = temp_result+1
                    sim_result[i, j] = temp_result/2
        print 'sim DONE'
        return sim_dict, sim_result     


    def init_k0(self):
        global day_dict
        print 'initialize k0'
        article_refer = []
        article_exp = []
        day_refer = []
        day = []
        data_exp = open(self.file_exp)
        for line in data_exp:
            temp = str(line).split()
            article_exp.append(int(temp[0]))
            day.append(int(temp[2]))
        data_refer = open(self.file_refer)
        for line in data_refer:
            temp = str(line).split()
            article_refer.append(int(temp[0]))
            day_refer.append(int(temp[2]))
            day.append(int(temp[2]))
        day_count = collections.Counter(day)
        k0_result = np.zeros((len(set(article_exp)), len(set(day))))
        k0_dict = {}                # use the ID of article and the day to locate the K0
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
            k0_result[k0_dict[article_refer[i]], day_dict[day_refer[i]]] +=  1
        for days in set(day):
            for article in set(article_refer):
                if day_count[days]-k0_result[k0_dict[article], day_dict[days]] == 0:
                    break
                else:
                    k0_result[k0_dict[article], day_dict[days]] = k0_result[k0_dict[article], day_dict[days]]/(day_count[days]-k0_result[k0_dict[article], day_dict[days]])
        print 'k0 DONE'
        return k0_dict, k0_result, day_dict

    # def init_z0(self):
    #     data = open(self.file_exp)
    #     n = len(data.readlines())
    #     z0 = np.zeros((n+1, n+1))   # the index of the event start at 1 rather than 0
    #     event = np.zeros((n, 4))
    #     data = open(self.file_exp)
    #     i = 0
    #     for line in data:
    #         temp = str(line).split()
    #         for j in range(0, len(temp)):
    #             if j < 2:
    #                 event[i, j+1] = temp[j]                
    #             elif j == 3:
    #                 event[i, 3] = temp[j]
    #                 event[i, 0] = i + 1
    #             else:
    #                 continue
    #         i = i + 1
    #     print 'begin!'

    def init_others(self):
        print 'initialize others'
        global Aerfa, Ru, rl, rw
        Aerfa = []
        Ru = []
        rl = 1
        rw = 1
        user_dict = {}
        friends_list = []
        data = open(self.file_exp)
        for line in data:
            temp = line.split()
            friends_list.append(int(temp[1]))
        friends = list(set(friends_list))
        n = len(friends)
        counter = collections.Counter(friends_list)
        def assign(i):
            Aerfa.append(counter[friends[i]]/n)
            Ru.append((counter[friends[i]]+1)/(n+1))
            user_dict[friends[i]] = i
        map(assign, [i for i in xrange(0, n)])
        print 'others DONE'
        return user_dict

    def init_data(self):
        print 'initialize init_data'
        global p, day_dict
        data = open(self.file_exp)
        n = len(data.readlines())
        event = np.zeros((n+1, 3))
        index = 1
        data = open(self.file_exp)
        for line in data:
            temp = line.split()
            event[index, 0] = int(temp[0])
            event[index, 1] = int(temp[1])
            event[index, 2] = int(temp[2])
            index = index + 1
        p = np.zeros((n+1, n+1))
        print 'data DONE'
        return event
        
                            
class ECM(object):

    def __init__(self, sim_dict, sim_O, k0_dict, k0, day_dict, user_dict, event):
        self.sim_dict = sim_dict
        self.sim_O = sim_O
        self.k0_dict = k0_dict
        self.k0 = k0
        self.user_dict = user_dict
        self.day_dict = day_dict
        self.event = event
 
    def E_step(self):
        global p, Aerfa, Ru, rl, rw
        def calculate_j(j):
            print j, len(p)
            def calculate_i(i):
                if i == 0:
                    temp = Ru[self.user_dict[self.event[j, 1]]] * self.k0[self.k0_dict[self.event[j, 0]], self.day_dict[self.event[j, 2]]]
                    p[j, i] = temp * math.exp(-1*temp)
                else:
                    if self.day_dict[self.event[i, 2]] <= self.day_dict[self.event[j, 2]]:
                        p[j, i] = 0
                    else:
                        t = self.day_dict[self.event[i, 2]] - self.day_dict[self.event[j, 2]]
                        temp1 = Aerfa[self.user_dict[self.event[i, 1]]] * Ru[self.user_dict[self.event[j, 1]]] * math.exp(-1*rl*t)
                        temp2 = self.sim_O[self.sim_dict[self.event[j, 0]], self.sim_dict[self.event[i, 0]]] * math.exp(-1*rw*t)
                        temp3 = (Aerfa[self.user_dict[self.event[i, 1]]] * Ru[self.user_dict[self.event[j, 1]]])/rw * (1-math.exp(-1*rw*t))
                        temp4 = self.sim_O[self.sim_dict[self.event[j, 0]], self.sim_dict[self.event[i, 0]]]/rl * (1-math.exp(-1*rl*t))
                        p[j, i] = (temp1 + temp2)*math.exp(-1*(temp3 + temp4))
            map(calculate_i, [i for i in xrange(0, len(p))])
        map(calculate_j, [j for j in xrange(1, len(p))])

    def C_step(self):
        global p, Z
        Z = {}
        def Max_index(j):
            temp = max(list(p[j,:]))
            Z[j] = list(p[j, :]).index(temp)
        map(Max_index, [j for j in xrange(1, len(p))])


    def M_step(self):
        global p, Aerfa, Ru, rl, rw, Z
        for item in self.user_dict:
            counter = 0
            for i in self.event[:, 1]:
                event_id = list(event[:, 1]).index(i)
        def calculate_z(item):
            list_ID = []
            counter = 0
            def get_Id(item):
                sum_up = 0
                sum_down = 0
                for i in xrange(1, len(p)):
                    if item == self.event[i, 1]:
                        for sth in Z.values():
                            if sth == i:
                                sum_up += 1
                                index = Z.keys().index(sth) + 1
                                sum_down += Ru[self.event[index, 1]]*(1-math.exp(-1*rw*(self.event[i, 1]-self.event[index, 1])))/rw
                if sum_up == 0:
                    Aerfa[item] = 0
                else:
                    Aerfa[item] = sum_up/sum_down
            map(get_Id, [item in self.user_dict])



                    
                    
            
            
        

    
def main():
    initialize = Initialize('dataset/final_mc.txt', 'dataset/final_rating_refer.txt', 'dataset/final_rating_exp.txt', 'dataset/final_user_rating.txt')
    sim_Dict, sim_O = initialize.init_sim()
    k0_Dict, k0, day_Dict = initialize.init_k0()
    user_Dict = initialize.init_others()
    Event = initialize.init_data()
    ecm = ECM(sim_Dict, sim_O, k0_Dict, k0, day_Dict, user_Dict, Event)
    ecm.E_step()
    ecm.C_step()
    ecm.M_step()

if __name__ == '__main__': main()