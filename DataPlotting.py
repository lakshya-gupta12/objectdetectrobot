import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import math
import seaborn as sns

#Hardcoding Object/Obstacle coordinates
x = [1,2,3,3,4,4]
y = [3,1,3,2,3,1]
sdist=[]
closestp=[0,0]
presentp=[0,0]
goalp=[4,1]
x_data = []
y_data = []

def calculateDistance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist  
#print calculateDistance(x1, y1, x2, y2)  

def search(list,n):   
    for i in range(len(list)): 
        if list[i] == n: 
            return i
        else:
            return False




def closestpoint(x1,y1):
    for i in range(len(x)): #As there are 5 obstacles including goal object.
        sdist.append(calculateDistance(x1,y1,x[i],y[i]))
    print("sdist",sdist)
    if(len(sdist) >0):
        temp=min(sdist)
        print("temp",temp)
        j = sdist.index(temp)
        print("index",sdist.index(temp))
        closestp[0]=(x[j])
        closestp[1]=(y[j])
        print("closestp",closestp)
        if(closestp[0] == goalp[0] and closestp[1] == goalp[1]):
            sdist.clear()
        else:
            x.pop(j)
            y.pop(j)
            sdist.clear()    
    #once the coordinate is visited the element is removed from actaual list
        



def animation_frame(i):
    p = sns.lineplot(x=[presentp[0],closestp[0]], y=[presentp[1],closestp[1]], color="b")
    plt.setp(p.lines,linewidth=3)
    presentp[0]= closestp[0]
    presentp[1]= closestp[1]
    closestpoint(presentp[0],presentp[1])
    print(presentp,closestp)

    



fig,ax = plt.subplots()
ax.set_xlim([-1, 5])
ax.set_ylim([-1, 4])
line, = ax.plot([],[],lw=2)

#placing Goal Object
ax.plot(4, 1, "ro",markersize=10,label='Goal Object')

#placing robo at (0,0) by default
ax.plot(0, 0, "ko",markersize=10,label='Robo')

plt.scatter(x, y,label='Other Objects')




#Driver code
# Robo at (0,0)
closestpoint(0,0)
animation = FuncAnimation(fig, animation_frame,frames=6, interval=1000)
plt.show()

    