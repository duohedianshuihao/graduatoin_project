from __future__ import division
from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import time

# def import_data(filename1, filename2, filename3, filename4):
#     global p, Aerfa, Ru, Z
#     data1 = open(filename1, 'r')
#     n = len(data1.readlines())
#     p = np.zeros((n, 3))
#     data2 = open(filename2, 'r')
#     m = len(data2.readlines())
#     Z = np.zeros((m, 2))
#     Aerfa = []
#     Ru = []

#     data1 = open(filename1, 'r')
#     i = 0
#     for line in data1:
#         temp = line.split()
#         for j in xrange(0, 3):
#             p[i, j] = float(temp[j])
#         i += 1

#     data2 = open(filename2, 'r')
#     i = 0
#     for line in data2:
#         temp = line.split()
#         for j in xrange(0, 2):
#             Z[i, j] = float(temp[j])
#         i += 1

#     data3 = open(filename3, 'r')
#     for line in data3:
#         temp = line.split()
#         def Add(item):
#             Aerfa.append(float(item))
#         map(Add, [item for item in temp])

#     data4 = open(filename4, 'r')
#     for line in data4:
#         temp = line.split()
#         def Add(item):
#             Ru.append(float(item))        
#         map(Add, [item for item in temp])

# def draw_rectangle(Canvas):
#     global p
#     list_ext = list(p[:, 0])
#     list_int = list(p[:, 1])
#     list_soc = list(p[:, 2])
#     sum_ext = sum(list_ext)
#     sum_int = sum(list_int)
#     sum_soc = sum(list_soc)
#     Canvas.create_rectangle(100, 600*(1-sum_ext/12345), 250, 600, fill = 'blue')
#     Canvas.create_rectangle(300, 600*(1-sum_int/12345), 450, 600, fill = 'blue')
#     Canvas.create_rectangle(500, 600*(1-sum_soc/12345), 650, 600, fill = 'blue')
#     Canvas.create_text(175, 590 - 600*(sum_ext/12345), text = 'External : ' + str("%.2f" % ((sum_ext/12345)*100)) +' %')
#     Canvas.create_text(375, 590 - 600*(sum_int/12345), text = 'Intrinsic : ' + str("%.2f" % ((sum_int/12345)*100)) +' %')
#     Canvas.create_text(575, 590 - 600*(sum_soc/12345), text = 'Social :' + str("%.2f" % ((sum_soc/12345)*100)) +' %')
#     Canvas.pack()
    #return rect_ext, rect_int, rect_soc, text_ext, text_int, text_soc

def input_png(Canvas, number):
    if number == 1:
        photo_file = Image.open('figure/button_1.png')
        im = ImageTk.PhotoImage(photo_file)
        label = Label(Canvas, image = im, bg = 'gray')
        label.image = im
        label.pack()
        Canvas.pack()
    elif number == 2:
        photo_file = Image.open('figure/button_2.png')
        im = ImageTk.PhotoImage(photo_file)
        label = Label(Canvas, image = im, bg = 'gray')
        label.image = im
        label.pack()
        Canvas.pack()
    elif number == 3:
        photo_file = Image.open('figure/button_3.png')
        im = ImageTk.PhotoImage(photo_file)
        label = Label(Canvas, image = im, bg = 'gray')
        label.image = im
        label.pack()
        Canvas.pack()
    elif number == 4:
        photo_file = Image.open('figure/button_4.png')
        im = ImageTk.PhotoImage(photo_file)
        label = Label(Canvas, image = im, bg = 'gray')
        label.image = im
        label.pack()
        Canvas.pack()

def Button_dataset():
    #AframeDraw.delete('all')
    input_png(frameDraw, 1)


def Button_result():
    #frameDraw.delete('all')
    input_png(frameDraw, 2)    
    

def Button_user():
    #frameDraw.delete('all')
    input_png(frameDraw, 3)

def Button_compare():
    #frameDraw.delete('all')
    input_png(frameDraw, 4)
    
# f1 = str('dataset/fake_p.txt')
# f2 = str('dataset/fake_Z.txt')
# f3 = str('dataset/fake_Aerfa.txt')
# f4 = str('dataset/fake_Ru.txt')
# import_data(f1, f2, f3, f4)
root = Tk()
root.title('Epinions数据集结果展示')
frameButton = Frame(root, width = 200, height = 800)
frameButton.pack(side = LEFT)
frameDraw = Frame(root, width = 1000, height = 800)
frameDraw.pack()
button_dataset = Button(frameButton, text = '数据集', width = 15, height = 4, command = Button_dataset).pack(side = TOP)
button_result = Button(frameButton, text = '实验结果', width = 15, height = 4, command = Button_result).pack(side = TOP)
button_user = Button(frameButton, text = '用户特性', width = 15, height = 4, command = Button_user).pack(side = TOP)
button_compare = Button(frameButton, text = "外部内部影响对比", width = 15, height = 4, command = Button_compare).pack(side = TOP)
root.mainloop()
