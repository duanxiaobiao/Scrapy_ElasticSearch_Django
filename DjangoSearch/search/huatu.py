

# encoding=utf-8
import matplotlib.pyplot as plt
from pylab import *                                 #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

def  funs(x,y):

    for index,value in enumerate(y) :
        if value == None:
            del x[index]
            del y[index]

    return x,y


x1 = [152,213,800,3000]
x2 = [152,213,800,3000]
x3 = [152,213,800,3000]
x4 = [152,213,800,3000]

y1 = [None, 100, 100, None]
y2 = [100,None,79.5,63.5]
y3= [100,None,84.5,58.9]
y4= [100,None,81.1,71.9]

x1,y1 = funs(x1,y1)
x2,y2 = funs(x2,y2)
x3,y3 = funs(x3,y3)
x4,y4 = funs(x4,y4)

print(x1)
print(y1)
print("==============================")
print(x2)
print(y2)
print("==============================")
print(x3)
print(y3)
print("==============================")

print(x4)
print(y4)
print("==============================")

#plt.plot(x, y, 'ro-')
#plt.plot(x, y1, 'bo-')
# plt.xlim(-1, 11)  # 限定横轴的范围
#pl.ylim(-1, 110)  # 限定纵轴的范围


plt.plot(x1, y1, marker='o', mec='r', mfc='w',label=u'y1')
for x,y in zip(x1,y1):
    plt.text(x, y, (x, y), color='r')
plt.plot(x2, y2, marker='*', ms=10,label=u'y2')
for xx,yx in zip(x2,y2):
    plt.text(xx, yx, (xx, yx), color='b')
plt.plot(x3, y3, marker='o', ms=10,label=u'y3')
for xx,yx in zip(x3,y3):
    plt.text(xx, yx, (xx, yx), color='y')
plt.plot(x4, y4, marker='*', ms=10,label=u'y4')
for xx,yx in zip(x4,y4):
    plt.text(xx, yx, (xx, yx), color='green')
plt.legend()  # 让图例生效
plt.savefig('xxxxx')  # 让图例生效
# plt.xticks(x, names, rotation=45)
# plt.margins(0)
# plt.subplots_adjust(bottom=0.15)
# plt.xlabel(u"time(s)邻居") #X轴标签
# plt.ylabel("RMSE") #Y轴标签
# plt.title("A simple plot") #标题

plt.show()