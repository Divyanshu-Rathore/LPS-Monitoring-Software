
import math
import numpy as np
import pandas as pd



df1 = pd.read_csv('Location Data - LPS.csv')
df2 = pd.read_csv('Location Data - Storage.csv')
df2['Capacity (tonnes/year)'] = df2['Capacity )(tonnes/year)']
df2 = df2.drop(columns = ['Capacity )(tonnes/year)'], axis = 0)
df1['Latitude']  = pd.to_numeric(df1['Latitude'],errors='coerce')
df1['Longitude']  = pd.to_numeric(df1['Longitude'],errors='coerce')
df2['Latitude']  = pd.to_numeric(df2['Latitude'],errors='coerce')
df2['Longitude']  = pd.to_numeric(df2['Longitude'],errors='coerce')
df1['Amount (tonne/year)'] = pd.to_numeric(df1['Amount (tonne/year)'],errors='coerce')
df2['Capacity (tonnes/year)'] = pd.to_numeric(df2['Capacity (tonnes/year)'],errors='coerce')
A = df2[['Latitude','Longitude']].to_numpy()
B = df1['LPS'].to_numpy()


# Distance
from math import radians, cos, sin, asin, sqrt

def pagal(x,y,nodes,dist1,dist2,C):
    array1= []
    d = []
    index = []
    for i in range(0,len(nodes)):
        
        
        lat1 = radians(x)
        lon1 = radians(y)
        lat2 = radians(nodes[i][0])
        lon2 = radians(nodes[i][1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6400
        d.append(c*r)
        index.append(i)
        
    df3 = pd.DataFrame(d, columns= ['Dist'])
    df3['Index'] = index
    df3.sort_values(by=['Dist'], inplace=True)

    m = 0
    j =0
    for k in range(0,len(df3)):
        if dist2 > int(df3['Dist'][k:k+1]) and dist1 < int(df3['Dist'][k:k+1]):
            if m ==0:
                m = k
            j = j +1
            
           
       
        
       
    if j==0:
        inka = 2000
    else:
        array1 = df3['Index'][m:m+j].to_numpy()
        inka =0
        i=0
        for i in range(0,j):
            if C <= df2['Capacity (tonnes/year)'][array1[i]]:
                inka = array1[i]
                break
    return inka, array1
 

# GUI
from tkinter import Entry, IntVar, Tk
from tkinter import *
import tkinter as tk 
from tkinter import ttk 
win =tk.Tk()
from tkinter.ttk import Combobox
from PIL import Image, ImageTk


load = Image.open("PP.jpg")
load = load.resize((390, 800), Image.ANTIALIAS)
render = ImageTk.PhotoImage(load)

 



def Plant():
    lat=0
    lon=0
    Cap =0
    d1=0
    d2=0
    for i in range(len(df1)):
        if(lps.get() == df1['LPS'][i]):
            lat = df1['Latitude'][i]
            lon = df1['Longitude'][i]
            Cap = df1['Amount (tonne/year)'][i]
            break
    if dist.get() == '< 80 km':
        d1 = 5
        d2 = 80
    if dist.get() == '80 - 200 km':
        d1 = 80
        d2 = 200
    if dist.get() == '200 - 400 km':
        d1 = 200
        d2 = 400
    if dist.get() == '400 - 600 km':
        d1 = 400
        d2 = 600
    if dist.get() == '600 - 800 km':
        d1 = 600
        d2 = 800
    if dist.get() == '800 - 1200 km':
        d1 = 800
        d2 = 1200
    if dist.get() == '1200 - 1500 km':
        d1 = 1200
        d2  = 1500
    if dist.get() == '> 1500 km':
        d1 = 1500
        d2 = 45000
        
    opt ,a = pagal(lat,lon,A,d1,d2,Cap)
    
    
    i = 0
    element1 = ''
    element2 = ''
    element3 = ''
    if opt == 2000:
        element1 =  'None'
        element2 =  'None'
        element3 = 'None'
        
    else:
        r = len(a)
        if r > 11:
            r = 11
        else:
            r = r
            for i in range(0,r):
                element1 = element1 + df2['Storage Facility'][a[i]] +'\n'
                element2 = element2 + str(df2['Capacity (tonnes/year)'][a[i]]) +'\n'
            
            element3 = df2['Storage Facility'][(opt)] + '   -  With Storing Capacity  of ' + str(df2['Capacity (tonnes/year)'][opt]) + ' Million Tonnes/Year'
            
    led10.configure(text = element1,font=("Bold", 12))
    led14.configure(text = element2,font=("Bold", 12))
    led15.configure(text = element3 ,font=("Bold", 12))
    
    
            
win.title('Indian Institute of Technology Ropar')

panel = ttk.Label(win, image = render)
panel.pack(side= "right")

frame = ttk.LabelFrame(win, text = 'Development Engineering Project')
frame.pack(side = "left", fill = "both", expand = "yes")

def Click():
    Capacity =0
    
    for i in range(len(df1)):
        if(lps.get() == df1['LPS'][i]):
            Capacity = np.round(df1['Amount (tonne/year)'][i],2)
            break
   
    led7.configure(text = lps.get(),font=("Bold", 12))
    led13.configure(text = Capacity,font=("Bold", 12))
    
    


led = ttk.Label(frame,text= 'Integration of Carbon Emitting Sources and Storage Locations', font=("Bold", 20))
#led.grid(row = 0,column = 2.5, sticky =tk.W,padx =10)
led.place(x= 155, y=4)
led.configure(foreground = 'Black' , background = 'light blue')


led1 = ttk.Label(frame,text= 'Select Carbon Emitting Source',font=("Bold", 12))
led1.place(x= 130, y= 100)
led1.configure(foreground = 'black',background = 'light blue')



lps = ttk.Combobox(frame, width = 27)
  
B_LPS = B.tolist()

# Adding combobox drop down list
lps['values'] = B_LPS

lps.place(x= 150, y= 150)
lps.current()

on = ttk.Button(frame, text = 'Check', command = Click)
on.place(x= 360, y= 150)


led2 = ttk.Label(frame, text = 'Selected Carbon Emitting Source',font=("Bold", 12))
led2.place(x= 500, y= 100)
led2.configure(foreground = 'black', background = 'light blue')

led12 = ttk.Label(frame, text = 'Capacity to Emit Carbon (Million Tonnes/Year)',font=("Bold", 12))
led12.place(x= 800, y= 100)
led12.configure(foreground = 'black', background = 'light blue')

led7 = ttk.Label(frame,text= '' ,font=("Bold", 8))
led7.place(x= 500, y= 150)
led7.configure(foreground = 'black')

led13 = ttk.Label(frame,text= '' ,font=("Bold", 8))
led13.place(x= 1000, y= 150)
led13.configure(foreground = 'black')

led3 = ttk.Label(frame,text= 'Select Distance',font=("Bold", 12))
led3.place(x= 130, y= 210)
led3.configure(foreground = 'black',background = 'light blue')


led4 = ttk.Label(frame, text = 'Storage Location within Selected Range',font=("Bold", 12))
led4.place(x= 500, y= 210)
led4.configure(foreground = 'black', background = 'light blue')

led12 = ttk.Label(frame, text = 'Capacity to Store Carbon (Million Tonnes/Year)',font=("Bold", 12))
led12.place(x= 800, y= 210)
led12.configure(foreground = 'black',background = 'light blue')

dist = ttk.Combobox(frame, width = 27)
  

dist['values'] = ('< 80 km', '80 - 200 km','200 - 400 km','400 - 600 km', '600 - 800 km', '800 - 1200 km', '1200 - 1500 km', '> 1500 km')

dist.place(x= 150, y= 240)

led5 = ttk.Button(frame, text = 'Check', command = Plant)
led5.place(x= 360, y= 240)

led10 = ttk.Label(frame,text= '' ,font=("Bold", 8))
led10.place(x= 600, y= 250)
led10.configure(foreground = 'black')

led14 = ttk.Label(frame,text= '' ,font=("Bold", 8))
led14.place(x= 900, y= 250)
led14.configure(foreground = 'black')

led6 = ttk.Label(frame,text= "Nearest Storage location (For Storing Captured Carbon Dioxide)",font=("Bold", 12))
led6.place(x= 130, y= 500)
led6.configure(foreground = 'black', background = 'light blue')

led15 = ttk.Label(frame,text= '' ,font=("Bold", 12))
led15.place(x= 600, y= 500)
led15.configure(foreground = 'black')





win.mainloop()

