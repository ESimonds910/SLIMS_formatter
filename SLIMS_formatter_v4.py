# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 11:00:21 2020

@author: esimonds
"""

"""
imports
"""
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo
import csv
import shutil
import os

"""
function allows only integer inputs for entry fields when specified
"""
def callback(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False
    
"""
creates user window to format files paths and move enspire files
needed for SLIMS
"""
main_window = Tk()
main_window.title("Welcome to the SLIMS formatter!")

reg= main_window.register(callback)  

proj_num_lab = Label(main_window, text= "Enter the number of projects read in plate reader:")
proj_num_lab.grid(row=0, column=0, pady=5)

proj_num_ent = Entry(main_window)
proj_num_ent.grid(row=0, column=1, pady=5, padx= 5)
proj_num_ent.config(validate='key', validatecommand= (reg, '%P'))


# test_btn = Button(main_window, text= "Test")
# test_btn.grid(row=1, column=0)
# test_btn.config(state='disabled')


proj_num_btn = Button(main_window, text="Submit", command= lambda: (proj_num_lab.grid_remove(), 
                                                                    proj_num_ent.grid_remove(), 
                                                                    proj_num_btn.grid_remove(),
                                                                    projDetails()))
proj_num_btn.grid(row=0, column=2, pady=5, padx=5)

def projDetails():
    """
    Enter the name for your project, and plate number
    if multiple projects
    
    """
    entries = []
    proj_num = int(proj_num_ent.get())
    
    for num in range(proj_num):
        
        if proj_num == 1:
            
            plate_ent = 0
            proj_lab = Label(main_window, text="Enter project ID: ")
            proj_lab.grid(row=num, column=0, pady= 5)
            
            proj_ent = Entry(main_window)
            proj_ent.grid(row=num, column=1, pady= 5, padx= 5)
            
            entries.append((proj_ent, plate_ent))
                    
        if proj_num > 1:
            
            proj_lab = Label(main_window, text="Enter project ID: ")
            proj_lab.grid(row=num, column=0, pady= 5)
            
            proj_ent = Entry(main_window)
            proj_ent.grid(row=num, column=1, pady= 5, padx= 5)
            
            plate_lab = Label(main_window, text= "Enter plate num: ")
            plate_lab.grid(row=num, column= 2, pady= 5, padx= 5)
            
            plate_ent = Entry(main_window)
            plate_ent.grid(row=num, column=3, pady=5, padx=5)
            plate_ent.config(validate='key', validatecommand= (reg, '%P'))
            
            entries.append((proj_ent, plate_ent))

    enter_btn = Button(main_window, text="Submit", command= lambda: (fileFinder(proj_num, entries),
                                                                     enter_btn.config(state='disabled'),
                                                                     skip_btn.config(state='disabled')))
    enter_btn.grid(row= proj_num + 1, column=0, padx=5, pady=5)
    
    skip_btn = Button(main_window, text="Skip File Copy", command= lambda: getPaths(proj_num, entries))
    skip_btn.grid(row= proj_num + 1, column=1, padx=5, pady=5)
    
    return entries
    
def fileFinder(proj_num, entries):
    """
    For one project: file found, copied, and moved to specified location
    for multiple: file found, split according to entry details, and moved
                to specified location
    """
   
    display = Toplevel(main_window)
    display.title("Copy these file paths and paste into SLIMS")
    
    path_text = Text(display)
    path_text.grid()
    
    if proj_num == 1:
        name = entries[0][0].get()
        file_path_raw = askopenfilename(title='Select file to copy', initialdir="L:/Assay Development/Enspire")
        folder_path_raw = askdirectory(title='Choose Raw folder from Project folder to place file for ' + name, initialdir='L:/Molecular Sciences/Small Scale Runs')
        #Set path for file move location and rename file with proj id
        raw_output = folder_path_raw + '/' + name + '.csv'
        #Move file to new location
        new_location = shutil.copy(file_path_raw, raw_output)

        path_text.insert(END, '/mnt/lab' + raw_output.split(':')[1] + '\n')
        
    
    if proj_num > 1:
        file_path = askopenfilename(title='Open HiPrBind Plate Data', initialdir="L:/Assay Development/Enspire")
        
        start = 0
        end = 0
        
        for entry in entries:
            name = entry[0].get()
            n = entry[1].get()
            folder_path_raw = askdirectory(title="Choose Raw folder from Project folder to place file for " + name, initialdir='L:/Molecular Sciences/Small Scale Runs')

            print('%s and %s' % (name, n))
            with open(file_path) as csvfile:
                reader = csv.reader(csvfile)
                end += int(n)*48
                plateRows= [row for idx, row in enumerate(reader) if idx in range(start,end)]
                start = end
                
                raw_output = folder_path_raw + '/' + name + '.csv'
                with open(raw_output, 'w', newline="") as newFile:
                    csvwriter = csv.writer(newFile)
                    for row in plateRows:
                        csvwriter.writerow(row)
                        
            
            path_text.insert(END, '/mnt/lab' + raw_output.split(':')[1] + '\n')


    # taskComplete = True
    showinfo("Congrats!", "File has been moved! Copy and Paste raw input file for SLIMS!")
    
    add_paths_btn = Button(main_window, text="OD and SLIMS_output file paths", command= lambda: getPaths(proj_num, entries))
    add_paths_btn.grid(pady=5, padx=5)

    
def getPaths(proj_num, entries):
    """
    window created: user options available to find SLIMS inputs
            OD file and SLIMS_output formats
            existing raw file path
            OD file check and dilution values check
    """
    filepath_window = Toplevel(main_window)
    filepath_window.title("More file path options")
    
    chckLabel = Label(filepath_window, text="Choose paths to copy into SLIMS").grid(row=0, column=1, sticky=W + E, padx= 10)
    
    chk1 = IntVar()
    chkBtn1 = Checkbutton(filepath_window, text="OD file path", variable=chk1, onvalue=1, offvalue=0)
    chkBtn1.grid(row=1, column=1, sticky= W + S + N, padx= 10)
    
    chk2 = IntVar()
    chkBtn2 = Checkbutton(filepath_window, text="Output file path", variable=chk2, onvalue=1, offvalue=0)
    chkBtn2.grid(row=2, column=1, sticky= W  + S + N, padx= 10)
    
    exst_raw_btn = Button(filepath_window, text="Find existing raw file", command=lambda: getRawFile())
    exst_raw_btn.grid(row=0, column=0, pady=5, padx=5)
    
    od_file_check_btn = Button(filepath_window, text="Check for OD file", command=lambda: checkOD())
    od_file_check_btn.grid(row=1, column=0, pady=5, padx=5)
    
    get_path_btn = Button(filepath_window, text= "Fetch and Display", command=lambda: displayPaths(entries, chk1, chk2))
    get_path_btn.grid(row=2, column=0, pady=5, padx=5)
    
    get_dilution_btn = Button(filepath_window, text= "Find dilutions", command=lambda: dilutionFolder())
    get_dilution_btn.grid(row=3, column=0, pady=5, padx=5)

def getRawFile():
    """
    If file already exists, user can skip copy/paste option
    and directly obtain file path for SLIMS
    """
    file_path_raw = askopenfilename(title='Select existing raw file', initialdir='L:/Molecular Sciences/Small Scale Runs' )
    display2 = Toplevel(main_window)
    path_text = Text(display2)
    path_text.grid()
    path_text.insert(END, '/mnt/lab' + file_path_raw.split(':')[1] + '\n')

def checkOD():
    """
    Allows user to find OD file to check for issues
    """
    OD_path = askopenfilename(title='Open OD File', initialdir='L:/Molecular Sciences/Small Scale Runs')
    os.startfile(OD_path)

def displayPaths(entries, chk1, chk2):
    """
    Asks user for file and folder paths for OD file and needed
    SLIMS output location
    """
    display3 = Toplevel(main_window)
    display3.title("Copy these file paths and paste into SLIMS")
    path_text = Text(display3)
    path_text.grid()
    
    if chk1.get() == 1:
        for entry in entries:
            name = entry[0].get()
            od_file_path = askopenfilename(title='Choose OD file for ' + name)
            od_output = '/mnt/lab' + od_file_path.split(':')[1]
            path_text.insert(END, od_output + '\n')
    
    if chk2.get() == 1: 
        for entry in entries:
            name = entry[0].get()
            folder_path_proc = askdirectory(title='Choose Processed folder from Project folder of ' + name)
            SLIMS_output = '/mnt/lab' + folder_path_proc.split(':')[1] + "/" + name + '_SLIMS_OUTPUT.xlsx'
            path_text.insert(END, SLIMS_output + '\n')
            
def dilutionFolder():
    """
    Allows user to search and open file containing dilution values 
    needed for SLIMS
    """
    dilution_path = askopenfilename(title='Open protocol with dilutions', initialdir="L:/Assay Development/Jia Liu/Experiments/Antibody/AlphaLISA assay")
    os.startfile(dilution_path)
    
main_window.mainloop()
