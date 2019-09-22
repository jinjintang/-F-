import sys
from collections import defaultdict
import numpy as np
from math import *
import heapq
alpha_1=25000
alpha_2=15000
beta_1=20000
beta_2=25000
cita=30000
delta=1

w1=0.5
w2=0.5

nodes=[]

dis=defaultdict(list)
dist=defaultdict(lambda :-1)
def cal_dist(i,j):
    x=(nodes[i][1]-nodes[j][1])**2
    y=(nodes[i][2]-nodes[j][2])**2
    z=(nodes[i][3]-nodes[j][3])**2
    return sqrt(x+y+z)

def cal_radius(a,b,c):
    return a*b*c/sqrt((a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c))
def cal_mo(x):
    return sqrt((x**2).sum())
def yuanxin(a,b,c,r):
    a,b,c=np.array(a),np.array(b),np.array(c)
    z=np.cross(a-b,b-c)
    bo=np.cross(a-b,z)
    bo=bo/np.linalg.norm(bo,ord=2)
    return b+bo*r,b-bo*r
def cal_bc(o,r,b,c):
    co=cal_mo(c-o)
    cd=sqrt(co**2-r**2)
    theta=acos(r/cd)
    theta_0=np.dot((a-b),(c-b))/(cal_mo(a-b)*cal_mo(c-b))
    return (theta_0-theta)*r+co          

f = open('data1.csv', "r")
for line in f:
    line=line.strip().split(',')
    nodes.append((len(nodes),float(line[1]),float(line[2]),float(line[3]),line[4]))

for i in range(len(nodes)):
    for j in range(i+1,len(nodes)):
        d=int(cal_dist(i,j))
        dist[(i,j)]=dist[(j,i)]=d
        if nodes[j][4]=='B':
            if d>cita:
                continue
        elif d>alpha_1:
            continue
        elif (nodes[i][4]=='1' or nodes[j][4]=='1' )and d>alpha_2:
            continue
        elif (nodes[i][4]=='0' or nodes[j][4]=='0' )and d> beta_1:
            continue
        dis[i].append((j,d))
        dis[j].append((i,d))
r=200
for i in range(len(nodes)):
    for j in dis[i]:
        for k in dis[j[0]]:
            if i!=k[0] :
                a=np.array(nodes[i][1:4])
                b=np.array(nodes[j[0]][1:4])
                c=np.array(nodes[k[0]][1:4])
                if cal_radius(cal_mo(a-b),cal_mo(a-c),cal_mo(b-c))<r:
                    continue
                o1,o2=yuanxin(a,b,c,r)
                res=cal_bc(o1,r,b,c)
                res=min(res,cal_bc(o2,r,b,c))
                print(cal_mo(a-b)+res)
                
