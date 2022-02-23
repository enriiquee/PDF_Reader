"""
@author: Enrique Pérez
@email: enrique.perez@ucm.es
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, glob2, logging
from tkinter import messagebox
from ScriptPDF.Function_script import *


import logging, sys

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

"""
This launcher allows the execution of the virtual environment to run the script. 

"""

#Start tkinter gui function
def tkinter_GUI():
    
    try:
        logger.info('Starting execution')
        
        root = Tk()
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)
        root.title("Script to read PDFs")
        #root.geometry("500x200")
        #root.configure(bg='Grey')

        #Functions: 
        def getFolderPath():
            folder_selected = filedialog.askdirectory() 
            folderPath.set(folder_selected)

        def doStuff():
            folder = folderPath.get()
            #Change directory
            os.chdir(folder)
            #Create a list with the pdf files. 
            pdfs = []
            for file in glob2.glob("**/*.pdf"):
                if file.endswith('.pdf'):
                    pdfs.append(file)
            
            #Create a list where we are going to save our dictionaries generated. 
            dicts_fundation_one=[]
            value_progress_increasse=(len(pdfs)/2)*100
            logger.info('Reading files...')
            for pdf in pdfs:
                string = convert_pdf_to_txt(pdf)
                #print(string)
                #print("NOMBRE DEL PDF: "+ pdf +"\n"+string)
                my_progressbar['value']+=value_progress_increasse
                root.update_idletasks
                type_of_Partner=detect_type_of_file(string, pdf)
                
                Type_of_pdf=detect_Type_of_pdf(string, pdf)
                # print(Type_of_pdf)
                
                custData=detectData(string,type_of_Partner,pdf,Type_of_pdf)
                dicts_fundation_one.append(custData)

                # if custData["Test_Type"]=="FoundationOne DX1":
                #     #print(custData.keys())
                #     dicts_fundation_one.append(custData)
                # else:
                #     pass
            
            logger.info('Saving results...')
            fundation_one_generator(dicts_fundation_one, pdfs)
            logger.info('Done. Exiting program.')
            #Message info:
            messagebox.showinfo('Info', 'Process completed!')
            quit()
            #print("Doing stuff with folder", folder)

        folderPath = StringVar()
        Label(root, text="Path:").grid(row=0, column=0)
        #Label(root, text="Apellido:").grid(row=1, column=0)

        Entry(root,textvariable=folderPath).grid(row=0, column=1, sticky=E+W)
        #Entry(root).grid(row=1, column=1, sticky=E+W)

        

        ttk.Button(root, text="Browse Folder",command=getFolderPath).grid(row=0,column=2)
        #print(btnFind)
        #c = ttk.Button(root ,text="Acept", command=doStuff).grid(row=4,column=0)

        Button(root, text="Run program", command=doStuff).grid(pady=10,
                                        padx=10,
                                        row=2,
                                        column=0,
                                        columnspan=2,
                                        sticky=S+N+E+W)
        

        my_progressbar=ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate', length=400)
        my_progressbar.grid(row=4,column=0,columnspan=3,sticky=S+N+E+W)

        root.mainloop()
    
    except Exception as error:
        logger.error('\nERROR: ' + repr(error))
        logger.error('Aborting execution')
        exit(1)

if __name__ == '__main__':

    tkinter_GUI()
