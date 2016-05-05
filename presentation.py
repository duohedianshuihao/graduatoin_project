from __future__ import division
from Tkinter import *
import numpy as np
import time

def import_data(filename1, filename2, filename3, filename4):
    global p, Aerfa, Ru, Z
    data1 = open(filename1, 'r')
    n = len(data1.readlines())
    p = np.zeros((n, 3))
    data2 = open(filename2, 'r')
    m = len(data2.readlines())
    Z = np.zeros((m, 2))
    Aerfa = []
    Ru = []

    data1 = open(filename1, 'r')
    i = 0
    for line in data1:
        temp = line.split()
        for j in xrange(0, 3):
            p[i, j] = float(temp[j])
        i += 1

    data2 = open(filename2, 'r')
    i = 0
    for line in data2:
        temp = line.split()
        for j in xrange(0, 2):
            Z[i, j] = float(temp[j])
        i += 1

    data3 = open(filename3, 'r')
    for line in data3:
        temp = line.split()
        def Add(item):
            Aerfa.append(float(item))
        map(Add, [item for item in temp])

    data4 = open(filename4, 'r')
    for line in data4:
        temp = line.split()
        def Add(item):
            Ru.append(float(item))        
        map(Add, [item for item in temp])

def draw_rectangle(Canvas):
    rect_ext = Canvas.create_rectangle(100, 700, 300, 700, fill = 'blue')
    rect_int = Canvas.create_rectangle(400, 700, 600, 700, fill = 'blue')
    rect_soc = Canvas.create_rectangle(700, 700, 900, 700, fill = 'blue')
    text_ext = Canvas.create_text(200, 690, text = 'External')
    text_int = Canvas.create_text(500, 690, text = 'Intrinsic')
    text_soc = Canvas.create_text(800, 690, text = 'Social')
    Canvas.pack()
    return rect_ext, rect_int, rect_soc, text_ext, text_int, text_soc

def input_png(Canvas):
    photo = Image(file = 'dataset/fake_png.jpg')
    pic = Canvas.create_image(0, 0, image = photo)
    Canvas.pack()
    return pic

def Button_P():
    draw_on.delete('all')
    rect_ext, rect_int, rect_soc, text_ext, text_int, text_soc = draw_rectangle(draw_on)
    display_P(rect_ext, rect_int, rect_soc, text_ext, text_int, text_soc, draw_on)

def display_P(rect_ext, rect_int, rect_soc, text_ext, text_int, text_soc, draw_on):
    global p
    list_ext = list(p[:, 0])
    list_int = list(p[:, 1])
    list_soc = list(p[:, 2])
    sum_ext, sum_int, sum_soc = 0, 0, 0
    for i in xrange(0, len(list_ext)):
        sum_ext += list_ext[i]
        sum_int += list_int[i]
        sum_soc += list_soc[i]
        draw_on.coords(rect_ext, 100, 700*(1-sum_ext/12345), 300, 700)
        draw_on.coords(rect_int, 400, 700*(1-sum_int/12345), 600, 700)
        draw_on.coords(rect_soc, 700, 700*(1-sum_soc/12345), 900, 700)
        draw_on.coords(text_ext, 200, 690 - 700*(sum_ext/12345))
        draw_on.coords(text_int, 500, 690 - 700*(sum_int/12345))
        draw_on.coords(text_soc, 800, 690 - 700*(sum_soc/12345))
        draw_on.update()

def Button_Paraset():
    draw_on.delete('all')
    picture = input_png(draw_on)
    display_Paraset(picture)

def display_Paraset(pic):
    pic.update()
    

def Button_Z():
    draw_on.delete('all')
    
    
f1 = str('dataset/fake_p.txt')
f2 = str('dataset/fake_Z.txt')
f3 = str('dataset/fake_Aerfa.txt')
f4 = str('dataset/fake_Ru.txt')
import_data(f1, f2, f3, f4)

root = Tk()
root.title('Epinions数据集结果展示')
frameButton = Frame(root)
frameButton.pack(side = LEFT)
frameDraw = Frame(root)
frameDraw.pack()
button_category = Button(frameButton, text = '事件分类', width = 10, height = 4, command = Button_P).pack(side = TOP)
button_paraset = Button(frameButton, text = '用户信息', width = 10, height = 4, command = Button_Paraset).pack(side = TOP)
button_z = Button(frameButton, text = '事件关联', width = 10, height = 4, command = Button_Z).pack(side = TOP)
button_reserve = Button(frameButton, text = "预留", width = 10, height = 4).pack(side = TOP)
draw_on = Canvas(frameDraw, bg = 'gray', width = 1000, height = 700)
draw_on.pack()
root.mainloop()