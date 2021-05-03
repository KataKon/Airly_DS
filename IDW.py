#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

location = pd.read_csv("Downloads/sensor_locations.csv", usecols=[1,2])
loc_arr = location.to_numpy()
#print(loc_arr)


# In[2]:


cols=[]
for i in range(1,57):
    cols.append(i*6)
all_m = pd.read_csv("Downloads/march-2017.csv", usecols=cols)
#print(all_m)


# In[3]:


pm10 = all_m.to_numpy()


# In[4]:


#odległość liczona przy założeniu, że Ziemia jest kulą
def distance(x1, x2, y1, y2):
    return np.sqrt((x2-x1)**2+(np.cos(x1*np.pi/180)*(y2-y1)**2))*40075.704/360 #km
#funkcja wagowa 
def weight(x, xk, y, yk, p):
    return 1/distance(xk, x, yk, y)**p
#interpolacja IDW
def IDW(x, y, loc_arr, pm10, date, p):
    sum_wz = 0
    sum_w = 0
    for i in range(56):
        if(math.isnan(pm10[date,i])!=True and x!=loc_arr[i,0] and y!=loc_arr[i,1]):
            sum_wz += weight(x, loc_arr[i,0], y, loc_arr[i,1], p)*pm10[date, i]
            sum_w += weight(x, loc_arr[i,0], y, loc_arr[i,1], p)
        else:
            sum_wz+=0
            sum_w+=0
    z = sum_wz/sum_w
    return z #zwraca wartość w punkcie (x,y)
# parametry określające jakośc interpolacji (MPE i RMSE)
def quality(z,pm10):
    s=0
    mpe=0
    mse=0
    rmse = 0
    n=0
    for i in range(744):
        for j in range(56):
            if(math.isnan(pm10[i,j])!=True):
                mpe+=z[i,j]-pm10[i,j]
                mse+=(z[i,j]-pm10[i,j])**2
                n+=1
    mpe=mpe/n
    rmse=np.sqrt(mse/n)
    tab = [mpe,rmse]
    return tab
k = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]
tab = []
for p in k:
    z = np.zeros((744,56))
    for i in range(744):    
        for j in range(56):
            z[i,j] = IDW(loc_arr[j,0],loc_arr[j,1],loc_arr,pm10,i,p)
    tab.append(quality(z,pm10))
print(tab)


# In[6]:


mpe = []
rmse = []
for i in range(len(k)):
    a,b = tab[i]
    mpe.append(a)
    rmse.append(b)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(k,mpe,'o')
axes[0].set_xlabel("parametr p")
axes[0].set_ylabel("MPE")
axes[0].grid(True)
axes[0].set_title("Średni błąd estymacji")
axes[1].plot(k,rmse,'o')
axes[1].set_xlabel("parametr p ")
axes[1].set_ylabel("RMSE")
axes[1].grid(True)
axes[1].set_title("Pierwiastek średniego błędu kwadratowego")






