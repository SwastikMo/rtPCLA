#----------Author-------------------------------------------------------------------------------------------------------------------
'''
23/03/2024
proposed by : swastikmohapatra13@gmail.com 

ALGORITHM FOR rtPCLA -> REAL TIME PRE-CACHE LOADING ALGORITHM [ to be optimised for week wise analysis ]

- there need to be a number of things into consideration for predictive caching 
    step 1 ) -- based on time and day we will load in data at those particular time[ day and hour ] in previous 16 weeks 
    step 2 ) -- based on step 1  a dynamically and tree based frequency calculating algorithm we shall get 3 most used files in those days in 16 weeks
    step 3 ) -- based on step 2 we shall load these files on cache memory based on their sizes 
ML model isnt a logical solution for these types of dynamic cache allocation its due to : 
  1. complexity of file paths and names 
  2. variablity of frequencies 
  3. model being outdated after 1 yr : issue -> this could be resolved by retraining model at time intervals [doesnt seem practical]
     this is because such activities like cache management is required in low level processing areas where the luxury of training 
     the model in particular intervals of time isnt a viable option we can explore  . 

'''

#----------Modules------------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np 
import time 
import tkinter as tk

#----------Algorithm ---------------------------------------------------------------------------------------------------------------


init_time = time.time()
print(" --- Use input values as specified in [ ... ] ---\n")
input_hr = int(input(" enter time for predictive caching [0,23] : "))
input_day = str(input("enter day for predictive caching [Mon,Tue,Wed,Thu,Fri,Sat,Sun] : "))
columns = ['w/r','file_path','offset','offset2','date_time']
file = pd.read_csv('output.csv', names = columns , skipinitialspace=True) # found initial spaces while reading data
file = file.drop(columns=['offset','offset2'])


# '''checked for null values if any , found issue at last tuple , REMOVED IT MANUALLY '''
# # print(file.isnull().sum())
# # print(file.tail()) 
# ''' checking for unique file paths here '''
# # print([x for x in file['file_path'].unique()])

''' GENERATING COLIUMNS NEEDED '''
file['day'] = [str(x).split(' ')[0] for x in file['date_time']]
file['time'] = [str(x).split(' ')[3].split(':')[0] for x in file['date_time']]
file.drop(columns=['date_time'] , inplace=True)

''' GROPING BASED ON W/R FREQUENCY ,  DAY AND HOUR'''
df1 = file.groupby(['time' , 'file_path', 'day'] , as_index= False).count().sort_values(['time', 'w/r'] , ascending=False).reset_index(drop = True)
print(df1)
df1['time'] = df1['time'].astype(int)
df1['day'] = df1['day'].astype(str)


# QUERY FIRING 
''' result top [x] filepaths wrt to their w/r frequency '''
res_size = 15         #change if required 
df_result_query = df1[['file_path','w/r']][(df1['time'] == input_hr) & (df1['day'] == input_day)].head(res_size).reset_index(drop=True)
print(df_result_query , end = "\n")


# DISPLAY TIME OF EXECUTION 
fin_time = time.time()
print(fin_time - init_time)
    

#------------GUI--------------------------------------------------------------------------------------------------------------------

def process_inputs():
    try:
        input_hr = int(integer_entry.get())
        input_day = str(string_entry.get())
        res_size = 3  # change as needed 
        df_result_query = df1[['file_path','w/r']][(df1['time'] == input_hr) & (df1['day'] == input_day)].head(res_size).reset_index(drop=True)
        output_label.config(text=df_result_query)
    except ValueError:
        output_label.config(text="Invalid input! Please enter valid values.")

# Create the main application window
root = tk.Tk()
root.title(" Files To Cache ")

# Create labels and entries for input
integer_label = tk.Label(root, text="Enter hr[0,23] : ")
integer_label.pack()
integer_entry = tk.Entry(root)
integer_entry.pack()

string_label = tk.Label(root, text="Enter day[Mon,Tue..] :")
string_label.pack()
string_entry = tk.Entry(root)
string_entry.pack()

# Button to process inputs
process_button = tk.Button(root, text="Process Inputs", command=process_inputs)
process_button.pack()

output_label = tk.Label(root)
output_label.pack()
# Run the Tkinter event loop
root.mainloop()