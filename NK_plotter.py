"""
Script to plot nk data from fmf files stored in the material database for the AFMD group.
@author: Irfan Habib
last modifed: 2023/05/08
"""
#import statements
import numpy as np
from pylab import *
import tkinter as tk
from tkinter import filedialog
import pandas as pd

#function definitions
def load_data(file_path): # the fmf file has a lot of metadata that we want to skip trhough and extract what's needed 
    with open(file_path) as f: #open file
        lines = f.readlines() #load file into string array
        data_columns_fmt = [] # will be used to save the format info from teh fmf file
        data_columns_names = [] # will be sued to save the column names from the fmf file
        for i,line in enumerate(lines): #iterate throught data file
            if '[*data definitions]' in line: # find the heading info
                for line_a in lines[i+1:]: #skip the header line and iterate through column names
                    # print(line_a)
                    if line_a != '\n': #make sure you ahven't reached the end of the column names
                        data_columns_fmt.append(line_a[line_a.index(':')+1:].strip()) # store format info each col name
                        data_columns_names.append(line_a[:line_a.index(':')].strip())# store each column name
                    else: break # if end of the column names (data definition section) then end the loop
            if '[*data]' in line: # find the beginning of the actual data
                    # print(lines[i+1:])
                    df = pd.read_csv(file_path,skiprows=i+1,delim_whitespace=True, dtype = 'float', names = data_columns_names) #load data into dataframe, use delim_whitespace option to get rid of tab and line spaces
    
    # print(data_columns)                
    return df, data_columns_fmt #return the df and the format info

        # print(data_columns)

def plot_nk(data,fmt_label): # prep figure for nice aesthetics
    fig1 = figure(figsize = (8,6), dpi = 150)
    axN = fig1.add_subplot(211)
    axK = fig1.add_subplot(212)
    axK.set_xlabel(r'Wavelength [nm]', fontsize = 16)
    # axN.set_title('Optical Constants')
    axN.set_ylabel(r'n', fontsize = 16)
    axK.set_ylabel(r'k', fontsize = 16)
    axN.tick_params(axis = 'y', labelsize = 14)
    axK.tick_params(axis = 'y', labelsize = 14)
    axK.tick_params(axis = 'x', labelsize = 14)
    axN.tick_params(axis = 'x', labelsize = 14)
    axN.set_xticklabels('')
    axN.grid()
    axK.grid()
    
    
    if len(fmt_label)>3: # check if we are dealing with anisotropic data or not. >3 -> aniso components (4 plots), else just iso components (2 plots)

        axN.plot(data['wavelength'],data['n_ordinary'], color = 'blue', label = r'$'+fmt_label[1]+'$')
        axK.plot(data['wavelength'],data['k_ordinary'], color = 'red', label = r'$'+fmt_label[2]+'$')
        axN.plot(data['wavelength'],data['n_extraordinary'],color = 'purple',linestyle = '--', label = r'$'+fmt_label[3]+'$')
        axK.plot(data['wavelength'],data['k_extraordinary'], color = 'orange', linestyle = '--', label = r'$'+fmt_label[4]+'$')
    else:
        axN.plot(data['wavelength'],data['n_ordinary'], color = 'blue', label = r'$'+fmt_label[1]+'$')
        axK.plot(data['wavelength'],data['k_ordinary'], color = 'red', label = r'$'+fmt_label[2]+'$')
   
    axN.legend()
    axK.legend()
    
    

#main
def main():
    print('Please select nk data to plot (file must be .fmt,, compatible with AFMD .fmt nk files):')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename() #open file dlg to select fmf nk file to plot
    data, fmt = load_data(file_path) #load in data and do some prelim processing
    # print(data.head())
    plot_nk(data,fmt) #plot n and k data
    show() # display plot, save from the matplotlib window and rescale as needed


#execute
if __name__ == '__main__':
    main()