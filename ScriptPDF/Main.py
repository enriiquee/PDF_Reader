
from Function_script import *
import glob2

"""
This script allows us to execute the functions without starting the virtual environment. It is mostly used for testing. 
Remember to change the path in order to run. 

"""


#Start script
if __name__ == '__main__':
    
    #path of folder containing several PDFs
    
    path = r'/Users/enriq/Dropbox/Lector_adobe/PDF/' 
    # path= r'/Users/pax-32/Dropbox/Lector_adobe/PDF/'
    #path = r'/home/eperez/Documents/PDF_Reader/PDF'
    #Change directory
    os.chdir(path)
    #Create a list with the pdf files. 
    pdfs = []
    for file in glob2.glob("**/*.pdf"):
        pdfs.append(file)
    


    #Create a list where we are going to save our dictionaries generated. 
    dicts_fundation_one=[]
    dicts_clovis=[]
    dicts_Unknown=[]
    for pdf in pdfs:
        string = convert_pdf_to_txt(pdf)
        type_of_Partner=detect_type_of_file(string, pdf)

        Type_of_pdf=detect_Type_of_pdf(string, pdf)
        custData=detectData(string,type_of_Partner,pdf,Type_of_pdf)
        dicts_fundation_one.append(custData)
        # print("NOMBRE DEL PDF: "+ pdf +"\n"+string)
        # custData=detectData(string,type_of_Partner,pdf)
        
        # dicts_fundation_one.append(custData)
        
        # if custData["Test_Type"]=="FoundationOne DX1":
        #     #print(custData.keys())
        #     dicts_fundation_one.append(custData)
        # else:
        #     pass
    # print(custData)



# Detect what type of chip we have: 

    fundation_one_generator(dicts_fundation_one)
