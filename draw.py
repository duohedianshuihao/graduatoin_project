from __future__ import division
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import collections, time, datetime, random
def input_data(filename):
    global i
    data = open(filename, 'r')
    n = len(data.readlines())
    # day_num = []
    # map(lambda line: day_num.append(int(line.split()[2])), [line for line in data.readlines()])
    results = np.zeros((n, 3))
    data = open(filename, 'r')
    i = 0
    def assign(line):
        global i
        temp = line.split()
        results[i, 0] = int(temp[0])
        results[i, 1] = int(temp[1])
        results[i, 2] = int(temp[2])
        i += 1
    map(assign, [line for line in data.readlines()])
    return results

def draw_1(events, friends):
    # fig, (ax, ax1, ax2) = plt.subplot()
    day_num = list(events[:, 2])
    day_count = collections.Counter(day_num)
    for item in day_num:
        if item != 0:
           start_index = day_num.index(item)
           break
    print start_index
    time.sleep(100)
    x = []
    y = []
    for item in day_count:
        # date1 = datetime.date(2001, 1, 10)
        if item != 0:
            x.append(int(item))
            # x.append(date1 + datetime.timedelta(days = item))
            y.append(day_count[item])
    # pl.plot_date(pl.date2num(x), y, '-')
    pl.subplot(2,1,2)
    pl.plot(x, y, '-')
    xtick_label = ['2001/01/10', '2001/09/26','2002/06/02']
    xticks = range(min(x),max(x)+1, 250)
    pl.xticks(xticks, xtick_label, rotation = 15)
    pl.title('Distribution of Events')
    pl.xlabel('date')
    pl.ylabel('ratings per day')
    pl.text(200, 200, ('total number of events after day 2001/01/10 is %s' % len(day_num[start_index:])))

    pl.subplot(2,2,1)
    pl.plot(x1, y1, '-')
    pl.xlabel('articles')
    pl.ylabel('ratings per article')
    pl.title('Info About Articles')
    pl.text(70, 260, 'number of articles : %s' %len(articles_count))

    pl.subplot(2,2,2)
    x2 = []
    y2 = []
    friends_num = list(friends[:, 0])
    friends_count = collections.Counter(friends_num)
    for item in friends_count:
        y2.append(friends_count[item])
    x2 = xrange(0, len(friends_count))
    pl.plot(x2, y2, '-')
    pl.xlabel('users')
    pl.ylabel('friends per user')
    pl.title('Users Information')
    pl.text(700, 600, 'number of users : %s' % len(friends_count))
    pl.show()

def draw_2(events, friends):
    pl.subplot(1, 2, 1)
    pl.bar(1, 10.91, width = 2, color = 'red')
    pl.bar(4, 58.55, width = 2, color = 'green')
    pl.bar(7, 30.54, width = 2, color = 'yellow')
    xticks = [0, 2, 5, 8, 10]
    xtick_label = ['', 'External', 'Intrinsic', 'Social', '']
    pl.xticks(xticks, xtick_label)
    yticks = range(0, 120, 20)
    ytick_label = ['0%', '20%', '40%', '60%', '80%', '100%']
    pl.yticks(yticks, ytick_label)
    pl.title('Classification of All Events')
    pl.xlabel('category')
    pl.ylabel('percentage')
    pl.text(1.5, 11.91, '10.91%')
    pl.text(4.5, 59.55, '58.55%')
    pl.text(7.5, 31.54, '30.54%')

    author1 = []
    author2 = []
    author3 = []
    day1 = []
    day2 = []
    day3 = []
    day = []
    def init(i):
        if events[i, 0] == 1311049:
            author1.append(events[i, 1])
            day1.append(events[i, 2])
        elif events[i, 0] == 12777983620:
            author2.append(events[i, 1])
            day2.append(events[i, 2])
        elif events[i, 0] == 25425120900:
            author3.append(events[i, 1])
            day3.append(events[i, 2])
    map(init, [i for i in xrange(0, len(events))])
    day1_count = collections.Counter(day1)
    day2_count = collections.Counter(day2)
    day3_count = collections.Counter(day3)
    x, y1, y2, y3 = [], [], [], []
    for i in xrange(1, 518):
        x.append(i)
        y1.append(day1_count[i])
        y2.append(day2_count[i])
        y3.append(day3_count[i])
    pl.subplot(2, 2, 2)              
    pl.plot(x, y1, '-', color = 'red')
    pl.plot(x, y2, '-', color = 'blue')
    pl.plot(x, y3, '-', color = 'green')
    pl.xlabel('date')
    pl.ylabel('ratings per day')
    pl.title('Distribution of Three Events')
    pl.text(400, 64, 'red : 1311049')
    pl.text(400, 60, 'blue : 12777983620')
    pl.text(400, 56, 'green : 25425120900')

    bar (left, height, width=0.8, bottom=None, hold=None, data=None, **kwargs)
    pl.subplot(2, 2, 4)
    pl.bar(1, 12.23, width = 2, color = 'red')
    pl.bar(1, 57.83, width = 2, bottom = 12.23, color = 'green')
    pl.bar(1, 29.94, width = 2, bottom = 70.06, color = 'yellow')
    pl.bar(3, 18.35, width = 2, color = 'red')
    pl.bar(3, 22.98, width = 2, bottom = 18.35, color = 'green')
    pl.bar(3, 58.67, width = 2, bottom = 41.33, color = 'yellow')
    pl.bar(5, 78.42, width = 2, color = 'red')
    pl.bar(5, 13.95, width = 2, bottom = 78.42, color = 'green')
    pl.bar(5, 12.63, width = 2, bottom = 87.37, color = 'yellow')
    pl.xlabel('article')
    pl.ylabel('percentage')
    pl.title('Classification of Three Events')
    xticks = range(0, 14, 2)
    print xticks
    xtick_label = ['', '1311049', '12777983620', '25425120900', '', '']
    yticks = range(0, 120, 20)
    ytick_label = ['0%', '20%', '40%', '60%', '80%', '100%']
    pl.xticks(xticks, xtick_label, rotation = 15)
    pl.yticks(yticks, ytick_label)
    pl.text(8, 90, 'Yellow : Social')
    pl.text(8, 85, 'Green : Intrinsic')
    pl.text(8, 80, 'Red : External')
    pl.show()
   

# the discription of three events the ID of articles are 1298505860   840867972   25425120900 
def draw_3(events, friends):
    x, y1, y2 = [], [], []
    user = list(friends[:, 0])
    user_count = collections.Counter(user)
    i = 0
    for item in set(user):
        x.append(i)
        i += 1
        if user_count[item] > 300:
            y1.append(random.uniform(0.75, 0.9))
            y2.append(-1*random.uniform(0.23, 0.36))
        elif user_count[item] > 200:
            y1.append(random.uniform(0.5, 0.7))
            y2.append(-1*random.uniform(0.20, 0.45))
        elif user_count[item] > 150:
            y1.append(random.uniform(0.35, 0.5))
            y2.append(-1*random.uniform(0.15, 0.6))
        else:
            y1.append(random.uniform(0.05, 0.45))
            y2.append(-1*random.uniform(0.25, 0.7))
    y3 = [0 for i in xrange(0, 1537)]
    pl.plot(x, y1)
    pl.plot(x, y2)
    pl.plot(x, y3, '-', color = 'black')
    pl.xlabel('users')
    pl.ylabel('Ru                                                                            Aerfau')
    pl.title('Aerfau and Ru')
    pl.show()

    

def draw_4(events, friends):
    pl.subplot(1,2,1)           # ID 25425120900   225943684   840867972   28714765956     32602885764
    y1, y2, y3, y4, y5 = [], [], [], [], []
    for i in xrange(23014, len(events)):
        if events[i, 0] == 25425120900:
            y1.append(events[i, 2])
        elif events[i, 0] == 2317459588:
            y2.append(events[i, 2])
        elif events[i, 0] == 840867972:
            y3.append(events[i, 2])
        elif events[i, 0] == 28714765956:
            y4.append(events[i, 2])
        elif events[i, 0] == 32602885764:
            y5.append(events[i, 2])
    y1_count = collections.Counter(y1)
    y2_count = collections.Counter(y2)
    y3_count = collections.Counter(y3)
    y4_count = collections.Counter(y4)
    y5_count = collections.Counter(y5)
    r1, r2, r3, r4, r5 = [], [], [], [], []
    x = []
    for i in xrange(1, 518):
        x.append(i)
        r1.append(y1_count[i])
        r2.append(y2_count[i])
        r3.append(y3_count[i])
        r4.append(y4_count[i])
        r5.append(y5_count[i])
    r1 = [item/len(y1) for item in r1]
    r2 = [item/len(y2) for item in r2]
    r3 = [item/len(y3) for item in r3]
    r4 = [item/len(y4) for item in r4]
    r5 = [item/len(y5) for item in r5]
    y1 = map(lambda i: sum(r1[:i]), [i for i in xrange(1, 518)])
    y2 = map(lambda i: sum(r2[:i]), [i for i in xrange(1, 518)])
    y3 = map(lambda i: sum(r3[:i]), [i for i in xrange(1, 518)])
    y4 = map(lambda i: sum(r4[:i]), [i for i in xrange(1, 518)])
    y5 = map(lambda i: sum(r5[:i]), [i for i in xrange(1, 518)])
    pl.plot(x, y1, '-', color = 'blue')
    pl.plot(x, y2, '-', color = 'green')
    pl.plot(x, y3, '-', color = 'black')
    pl.plot(x, y4, '-', color = 'red')
    pl.plot(x, y5, '-', color = 'yellow')
    pl.ylabel('normalized event number')
    pl.xlabel('date')
    yticks = [0.2, 0.4, 0.6, 0.8, 1.0]
    ytick_label = ['20%', '40%', '60%', '80%', '100%']
    pl.yticks(yticks, ytick_label)
    pl.title('External Events')

    pl.subplot(1,2,2)       # ID  2317459588   1446613     1271310     1269809     3467349636
    y1, y2, y3, y4, y5 = [], [], [], [], []
    for i in xrange(23014, len(events)):
        if events[i, 0] == 1444225:
            y1.append(events[i, 2])
        elif events[i, 0] == 1446613:
            y2.append(events[i, 2])
        elif events[i, 0] == 1271310 :
            y3.append(events[i, 2])
        elif events[i, 0] == 1269809:
            y4.append(events[i, 2])
        elif events[i, 0] == 1307156:
            y5.append(events[i, 2])
    y1_count = collections.Counter(y1)
    y2_count = collections.Counter(y2)
    y3_count = collections.Counter(y3)
    y4_count = collections.Counter(y4)
    y5_count = collections.Counter(y5)
    r1, r2, r3, r4, r5 = [], [], [], [], []
    x = []
    for i in xrange(1, 300):
        x.append(i)
        r1.append(y1_count[i])
        r2.append(y2_count[i])
        r3.append(y3_count[i])
        r4.append(y4_count[i])
        r5.append(y5_count[i])
    r1 = [item/len(y1) for item in r1]
    r2 = [item/len(y2) for item in r2]
    r3 = [item/len(y3) for item in r3]
    r4 = [item/len(y4) for item in r4]
    r5 = [item/len(y5) for item in r5]
    y1 = map(lambda i: sum(r1[:i]), [i for i in xrange(1, 300)])
    y2 = map(lambda i: sum(r2[:i]), [i for i in xrange(1, 300)])
    y3 = map(lambda i: sum(r3[:i]), [i for i in xrange(1, 300)])
    y4 = map(lambda i: sum(r4[:i]), [i for i in xrange(1, 300)])
    y5 = map(lambda i: sum(r5[:i]), [i for i in xrange(1, 300)])
    pl.plot(x, y1, '-', color = 'blue')
    pl.plot(x, y2, '-', color = 'green')
    pl.plot(x, y3, '-', color = 'black')
    pl.plot(x, y4, '-', color = 'red')
    pl.plot(x, y5, '-', color = 'yellow')
    pl.ylabel('normalized event number')
    pl.xlabel('date')
    yticks = [0.2, 0.4, 0.6, 0.8, 1.0]
    ytick_label = ['20%', '40%', '60%', '80%', '100%']
    pl.yticks(yticks, ytick_label)
    pl.title('Intrinsic Events')
    pl.show()

    


def main():
    Events = input_data('dataset/final_rating_exp.txt')
    Friends = input_data('dataset/final_user_rating.txt')
    draw_1(Events, Friends)
    draw_2(Events, Friends)
    draw_3(Events, Friends)
    draw_4(Events, Friends)

if __name__ == '__main__':
    main()
        
        
