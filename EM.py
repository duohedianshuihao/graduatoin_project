from __future__ import division
from multiprocessing import Pool
import random
import math 
import numpy as np
import copy
import collections
import time
import pylab as pl


class Initialize(object):

    def __init__(self, file_mc, file_refer, file_exp, file_users):
         self.file_mc = file_mc
         self.file_refer = file_refer
         self.file_exp = file_exp
         self.file_users = file_users

    def init_sim(self):
        print 'initialize sim'
        author = []
        category = []
        article_dict = []
        data = open(self.file_mc, 'r')
        for line in data:
            temp = str(line).split()
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
        global day_dict, start_index
        print 'initialize k0'
        article_refer = []
        article_exp = []
        day_refer = []
        day = []
        data_exp = open(self.file_exp)
        for line in data_exp.readlines():
            temp = str(line).split()
            article_exp.append(int(temp[0]))
            day.append(int(temp[2]))
        for item in day:
            if item > 0:
                start_index = day.index(item)
                break
            else:
                pass
        data_refer = open(self.file_refer)
        for line in data_refer.readlines():
            temp = str(line).split()
            article_refer.append(int(temp[0]))
            day_refer.append(int(temp[2]))
            day.append(int(temp[2]))
        day_count = collections.Counter(day_refer)
        k0_result = np.zeros((len(set(article_exp)), len(set(day))))
        k0_result_final = np.zeros((len(set(article_exp)), len(set(day))))
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
        for days in set(day_refer):
            for article in set(article_refer):
                k0_result[k0_dict[article], day_dict[days]] = (k0_result[k0_dict[article], day_dict[days]]/day_count[days])
        # for article in set(article_refer):
        #     for days in set(day):
        #         for item in list(set(day))[0:list(set(day)).index(days)]:
        #             k0_result_final[k0_dict[article], day_dict[days]] += k0_result[k0_dict[article], day_dict[item]] * (item+1)/(days+1)       
        print 'k0 DONE'
        # print k0_result_final[k0_dict[1298505860], day_dict[103]]
        # print k0_result_final[k0_dict[1298505860], day_dict[104]]
        return k0_dict, k0_result, day_dict

    def init_others(self):
        print 'initialize others'
        global Aerfa, Ru, rl, rw
        Aerfa = []
        Ru = []
        rl, rw = 1, 1
        user_dict = {}
        friends_list = []
        data = open(self.file_exp)
        for line in data.readlines():
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
        user_dict_key = []   
        for item in user_dict.keys():
            user_dict_key.append(item)
        print 'others DONE'
        return user_dict, user_dict_key

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

    def __init__(self, sim_dict, sim_O, k0_dict, k0, day_dict, user_dict, user_dict_key, event):
        self.sim_dict = sim_dict
        self.sim_O = sim_O
        self.k0_dict = k0_dict
        self.k0 = k0
        self.user_dict = user_dict
        self.day_dict = day_dict
        self.user_dict_key = user_dict_key
        self.event = event
 
    def E_step(self):
        global p, Aerfa, Ru, rl, rw, start_index
        def calculate_j(j):
            def calculate_i(i):
                if i == 0:
                    temp = Ru[self.user_dict[self.event[j, 1]]] * self.k0[self.k0_dict[self.event[j, 0]], self.day_dict[self.event[j, 2]]]
                    p[j, i] = temp * math.exp(-1*temp)
                else:
                    if self.day_dict[self.event[i, 2]] >= self.day_dict[self.event[j, 2]]:
                        p[j, i] = 0
                    else:
                        t = self.day_dict[self.event[j, 2]] - self.day_dict[self.event[i, 2]]
                        temp1 = Aerfa[self.user_dict[self.event[i, 1]]] * Ru[self.user_dict[self.event[j, 1]]] * math.exp(-1*rl*t)
                        temp2 = self.sim_O[self.sim_dict[self.event[j, 0]], self.sim_dict[self.event[i, 0]]] * math.exp(-1*rw*t)
                        temp3 = (Aerfa[self.user_dict[self.event[i, 1]]] * Ru[self.user_dict[self.event[j, 1]]])/rw * (1-math.exp(-1*rw*t))
                        temp4 = self.sim_O[self.sim_dict[self.event[j, 0]], self.sim_dict[self.event[i, 0]]]/rl * (1-math.exp(-1*rl*t))
                        p[j, i] = (float(temp1) + float(temp2))*math.exp(-1*(float(temp3) + float(temp4)))
            map(calculate_i, [i for i in xrange(0, j)])
        map(calculate_j, [j for j in xrange(start_index, len(p))])

    def C_step(self):
        global p, Z, start_index
        Z = {}
        # def Max_index(j):
        #     temp = max(list(p[j,:]))
        #     Z[j] = list(p[j, :]).index(temp)
        # map(Max_index, [j for j in xrange(start_index, len(p))])
        # save_Z = open('dataset/Z.txt', 'w')
        # map(lambda i: save_Z.write(str(int(item))+'\n'), [item for item in Z])
        for j in xrange(1, len(p)):
            temp = max(list(p[j, :]))
            Z[j] = list(p[j, :]).index(temp)
        save_Z = open('dataset/Z.txt', 'w')
        map(lambda i: save_Z.write(str(int(item))+'\n'), [item for item in Z])

    def M_step(self):
        global p, Aerfa, Ru, rl, rw, Z, start_index
        print 'M_step start'
        def optimize_Aerfa(index):
            temp_up, temp_down = 0, 0
            user_ID = self.user_dict_key[index]
            Z_Values = Z.values()
            count_z = collections.Counter(Z_Values)
            for i in xrange(0, len(list(self.event[:, 1]))):
                if user_ID == self.event[i, 1]:         # then i is the ID of the event
                    if count_z[i] == 1:
                        temp_up += count_z[i]
                        index_j = Z_Values.index(i) + start_index       # the index of Z does NOT represent event ID but event ID - start_index
                        temp_down += Ru[self.user_dict[self.event[index_j, 1]]]*(1-math.exp(-1*rw*(self.event[index_j, 2]-self.event[i, 2])))/rw
                    elif count_z[i] > 1:
                        temp_up += count_z[i]
                        for j in xrange(0, len(Z)):
                            if i == Z_Values[j]:
                                temp_down += Ru[self.user_dict[self.event[(j+start_index), 1]]]*(1-math.exp(-1*rw*(self.event[(j+start_index), 2]-self.event[i, 2])))/rw
                    else:
                        pass                            
            if temp_up == 0:
                Aerfa[index] = 0
            else:
                Aerfa[index] = temp_up/temp_down
        map(optimize_Aerfa, [i for i in xrange(0, len(Aerfa))])    
        save_Aerfa = open('dataset/Aerfa1.txt', 'w')
        map(lambda i: save_Aerfa.write(str(float(Aerfa[i]))+'\n'), [i for i in xrange(0, len(Aerfa))])
        print 'update Aerfa over'        

        def optimize_Ru(index):
            temp_up, temp_down1, temp_down2 = 0,0,0
            user_ID = self.user_dict_key[index]     # user ID is the real ID, rather than the index of the event 
            count_event = collections.Counter(list(self.event[start_index:, 1]))
            temp_up = count_event[user_ID]
            if temp_up == 0:
                Ru[index] = 0
            else:
                for j in xrange(start_index, len(list(self.event[:, 1]))):
                    if user_ID == self.event[j, 1]:
                        if Z[j] == 0:
                            temp_down2 += self.k0[self.k0_dict[self.event[j, 0]], self.day_dict[self.event[j, 2]]]*(self.event[j, 2]*(1-0.5*self.event[j, 2]/518))
                        else:
                            temp_down1 += Aerfa[self.user_dict[self.event[Z[j], 1]]]*(1-math.exp(-1*rw*(self.event[j, 2]-self.event[Z[j], 2])))/rw                        
                Ru[index] = temp_up/(temp_down1+temp_down2)                              
        map(optimize_Ru, [i for i in xrange(0, len(Ru))])
        save_Ru = open('dataset/Ru1.txt', 'w')
        map(lambda i: save_Ru.write(str(float(Ru[i]))+'\n'), [i for i in xrange(0, len(Ru))])
        print 'update Ru over'

# Newton's method to upgrade the rw and rl
def generate_F_rw(x, event, user_dict, sim_dict, sim_O):
    global Z, Aerfa, Ru, rl
    F, dF = 0, 0
    for j in xrange(start_index, len(event)):
        if Z[j] != 0:
            t = event[j, 2] - event[Z[j], 2]
            exp_rw = math.exp(-1*x*t)
            exp_rl = math.exp(-1*rl*t)
            Aerfa_i = Aerfa[user_dict[int(event[Z[j], 1])]]
            Ru_j = Ru[user_dict[int(event[j, 1])]]
            sim = sim_O[sim_dict[int(event[j, 0])], sim_dict[int(event[Z[j], 0])]]
            big_under = Aerfa_i*Ru_j*exp_rw + sim*exp_rl
            if big_under != 0:
                F += (-1*t*exp_rw)/(big_under) - (x**-2)*(1-exp_rw) + (x**-1)*t*exp_rw
                dF += (t**2*exp_rw)*(big_under+Aerfa_i*Ru_j*exp_rw)/(big_under)**2 + 2*(x**-3)*(1-exp_rw)-(x**-2)*(t*exp_rw) - t*exp_rw*((x**-2)+(x**-1)*t)
    return F, dF

def generate_F_rl(x, event, user_dict, sim_dict, sim_O, rw_old):
    global Z, Aerfa, Ru
    F, dF = 0, 0
    for j in xrange(start_index, len(event)):
        if Z[j] != 0:
            t = event[j, 2] - event[Z[j], 2]
            exp_rw = math.exp(-1*rw_old*t)
            exp_rl = math.exp(-1*x*t)
            Aerfa_i = Aerfa[user_dict[int(event[Z[j], 1])]]
            Ru_j = Ru[user_dict[int(event[j, 1])]]
            sim = sim_O[sim_dict[int(event[j, 0])], sim_dict[int(event[Z[j], 0])]]
            big_under = Aerfa_i*Ru_j*exp_rw + sim*exp_rl
            if big_under != 0:
                F += (-1*t*exp_rl)/(big_under) - (x**-2)*(1-exp_rl) + (x**-1)*t*exp_rl
                dF += (t**2*exp_rl)*(big_under+sim*exp_rl)/(big_under)**2 + 2*(x**-3)*(1-exp_rl)-(x**-2)*(t*exp_rl) - t*exp_rl*((x**-2)+(x**-1)*t)
    return F, dF

def newtons_method(x0, e, event, user_dict, sim_dict, sim_O):
    print 'start Newtons method'
    global Z, rw, rl
    x0_copy = x0
    rw_old = rw
    # update rw
    F_rw, dF_rw = generate_F_rw(x0, event, user_dict, sim_dict, sim_O)
    while abs(F_rw - 0) > e:
        x0 = x0 - F_rw/dF_rw
        F_rw, dF_rw = generate_F_rw(x0, event, user_dict, sim_dict, sim_O)
        print F_rw, x0
    rw = x0
    # update rl
    F_rl, dF_rl = generate_F_rl(x0_copy, event, user_dict, sim_dict, sim_O, rw_old)
    while abs(F_rl - 0) > e:
        x0_copy = x0_copy - F_rl/dF_rl
        F_rl, dF_rl = generate_F_rl(x0_copy, event, user_dict, sim_dict, sim_O, rw_old)
        print F_rl, x0_copy
    rl = x0_copy
    print rw, rl
        


            

    
def main():
    global Aerfa, Ru, Z, p, rw, rl
    initialize = Initialize('dataset/final_mc.txt', 'dataset/final_rating_refer.txt', 'dataset/final_rating_exp.txt', 'dataset/final_user_rating.txt')
    sim_Dict, sim_O = initialize.init_sim()
    k0_Dict, k0, day_Dict = initialize.init_k0()
    user_Dict, user_Dict_key= initialize.init_others()
    Event = initialize.init_data()
    Aerfa_old = copy.deepcopy(Aerfa)
    Ru_old = copy.deepcopy(Ru)
    ecm = ECM(sim_Dict, sim_O, k0_Dict, k0, day_Dict, user_Dict, user_Dict_key, Event)
    ecm.E_step()
    ecm.C_step()
    ecm.M_step()
    newtons_method(5, 0.01, Event, user_Dict, sim_Dict, sim_O)
    while sum(abs(Aerfa_old-Aerfa)) > 1 or sum(abs(Ru_old-Ru)) > 1:
        Aerfa_old = copy.deepcopy(Aerfa)
        Ru_old = copy.deepcopy(Ru)
        ecm.E_step()        
        ecm.C_step()
        ecm.M_step()
        newtons_method(rl, 0.01, Event, user_Dict, sim_Dict, sim_O)
    print 'ALL OVER !'


if __name__ == '__main__': main()