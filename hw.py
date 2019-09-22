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
        elif (nodes[i][4]=='1' or nodes[j][4]=='1') and d>alpha_2:
            continue
        elif (nodes[i][4]=='0' or nodes[j][4]=='0') and d> beta_1:
            continue
        dis[i].append((j,d))
        dis[j].append((i,d))
dp_v=defaultdict(lambda :cita)
dp_h=defaultdict(lambda :cita)
result=[]
min_dist=-1
def dfs(err_v,err_h,now,last_v,last_h,path,h,thresh,path_distance):
    p=path[:]
    h1=h[:]
    h1[now[0]]+=1
    #print(err_v,err_h,now[0],dp_h[now[0]])
    p.append(now)
    global min_dist
    if now[4]=='B':
        if min_dist==-1:
            min_dist=path_distance
        else:
            min_dist=min(path_distance,min_dist)
        result.append((path_distance,len(p),p))
       # print(len(result))
        return 1
    res=0
    for d in dis[now[0]]:
        no=nodes[d[0]]
        if h1[no[0]]<=thresh:
            if min_dist!=-1 and path_distance+d[1]>=min_dist:
                    continue
            if no[4]=='1':
                if err_h+d[1]>=dp_h[no[0]]:
                   continue
                elif err_v+d[1]>alpha_1 or err_h+d[1]>alpha_2:
                    continue
                elif last_v==None :
                    res+=dfs(0,err_h+d[1],no,no,last_h,p,h1,thresh,path_distance+d[1])

                elif  dist[(no[0],last_v[0])]<=alpha_1:
                    res+=dfs(0,err_h+d[1],no,no,last_h,p,h1,thresh,path_distance+d[1])
            elif no[4]=='0':
                if err_v+d[1]>=dp_v[no[0]]:
                    continue
                elif err_v+d[1]>beta_1 or err_h+d[1]>beta_2:
                    continue
                
                elif last_h==None:
                    res+=dfs(err_v+d[1],0,no,last_v,no,p,h1,thresh,path_distance+d[1])
                elif  dist[(no[0],last_h[0])]<=beta_2:
                    res+=dfs(err_v+d[1],0,no,last_v,no,p,h1,thresh,path_distance+d[1])
            elif err_v+d[1]<cita and err_h+d[1]<cita:
                res+=dfs(err_v+d[1],err_h+d[1],no,last_v,last_h,p,h1,thresh,path_distance+d[1])
    
    if res==0:
        dp_h[now[0]]=min(err_h,dp_h[now[0]])
        dp_v[now[0]]=min(err_v,dp_v[now[0]])
    return res
def dfs1(err_v,err_h,now,last_v,last_h,path,h,thresh,path_distance):
    p=path[:]
    h1=h[:]
    h1[now[0]]+=1
    #print(err_v,err_h,now[0],dp_h[now[0]])
    p.append(now)
    global min_dist
    if now[4]=='B':
        if min_dist==-1:
            min_dist=path_distance
        else:
            min_dist=min(path_distance,min_dist)
        result.append((path_distance,len(p),p))
        #print(len(result))
        return 1
    res=0
    for d in dis[now[0]]:
        no=nodes[d[0]]
        if h1[no[0]]<=thresh:
            if min_dist!=-1 and path_distance+d[1]>=min_dist:
                    continue
            if no[4]=='1':
                if False:#err_h+d[1]>=dp_h[no[0]]:
                   continue
                elif err_v+d[1]>alpha_1 or err_h+d[1]>alpha_2:
                    continue
                elif last_v==None :
                    res+=dfs(0,err_h+d[1],no,no,last_h,p,h1,thresh,path_distance+d[1])

                elif  dist[(no[0],last_v[0])]<=alpha_1:
                    res+=dfs(0,err_h+d[1],no,no,last_h,p,h1,thresh,path_distance+d[1])
            elif no[4]=='0':
                if False:#err_v+d[1]>=dp_v[no[0]]:
                    continue
                elif err_v+d[1]>beta_1 or err_h+d[1]>beta_2:
                    continue
                
                elif last_h==None:
                    res+=dfs(err_v+d[1],0,no,last_v,no,p,h1,thresh,path_distance+d[1])
                elif  dist[(no[0],last_h[0])]<=beta_2:
                    res+=dfs(err_v+d[1],0,no,last_v,no,p,h1,thresh,path_distance+d[1])
            elif err_v+d[1]<cita and err_h+d[1]<cita:
                res+=dfs(err_v+d[1],err_h+d[1],no,last_v,last_h,p,h1,thresh,path_distance+d[1])
    
    if res==0:
        dp_h[now[0]]=min(err_h,dp_h[now[0]])
        dp_v[now[0]]=min(err_v,dp_v[now[0]])
    return res
for i in range(0,1):
    h=[0]*len(nodes)
    dfs(0,0,nodes[0],None,None,[],h,i,0)
print(len(result))
dfs1(0,0,nodes[0],None,None,[],h,1,0)
print(len(result))
result.sort()
#print(result[0])
for p in result[0][2]:
    print(p[1],p[2],p[3],p[4])







