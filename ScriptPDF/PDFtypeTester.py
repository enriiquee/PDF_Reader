import glob2, os
from Function_script import *

"""
This script allow us to detect what type of data we have. This is only a tester, so doesn't run in the main script. 
"""

#path of folder containing several PDFs
#path=r'C:/Users/enriq/Dropbox/Lector_adobe/PDF/'   
path=r'C:/Users/eperez2/OneDrive - UNIVERSIDAD DE MURCIA/PDF_Reader/Archivos/New files'  
#Change directory
os.chdir(path)
#Create a list with the pdf files. 
pdfs = []
for file in glob2.glob("**/*.pdf"):
    pdfs.append(file)
#print(len(pdfs))

    # Create a list where we are going to save our dictionaries generated. 
dicts_fundation_one=[]
custData = {}
dictionary={'Pfizer Inc.':0,'Clovis Oncology':0,'Roche Pharma':0, 'No_tiene':0}

counter_yes=0
counter_no=0
typeof=""
for pdf in pdfs:
    string = convert_pdf_to_txt(pdf)
    #print(string)

    if 'Partner Name' in string or 'PARTNER NAME' in string: 
        lines = list(filter(None,string.split('\n')))
        for i in range(len(lines)):
            if 'Partner Name' in lines[i] or 'PARTNER NAME' in lines[i]:
                #print(lines[i] + 'Nombre del archivo: '+ pdf )
                if 'Pfizer Inc' in lines[i]:
                    dictionary['Pfizer Inc.']+=1
                    typeof='Pfizer Inc'
                elif 'Clovis Oncology' in lines[i] or 'CLOVIS ONCOLOGY' in lines[i]:
                    dictionary['Clovis Oncology']+=1
                    typeof="Clovis Oncology"
                elif 'Roche Pharma' in lines[i]:
                    dictionary['Roche Pharma']+=1
                    typeof='Roche'
                #print(lines[i][13:])
            elif 'Test Type' in lines[i]:
                pass
                #print(lines[i]+";"+ pdf)
    else:
        dictionary['No_tiene']+=1
        print('No tiene' + 'Nombre del archivo: '+ pdf )

    if 'Test Type FoundationOne DX1' in lines or 'Test Type FoundationOne Liquid AB1'  in lines or 'Test Type FoundationOne DX1 (SOLID)'  in lines or 'Test Type FoundationOne Liquid'  in lines or 'Test Type FoundationOne'  in lines: 
        counter_yes+=1
        print(typeof+";"+pdf)
    else:
        counter_no+=1
        
    
#print(counter_no, counter_yes)






    





    

    
#print(dictionary)
    #print("NOMBRE DEL PDF: "+ pdf +"\n"+string)


        