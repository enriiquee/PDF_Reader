import glob2, os
from Function_script import *



    #path of folder containing several PDFs
    #path=r'C:/Users/enriq/Dropbox/Lector_adobe/PDF/'  
path=r'C:/Users/enriq/Dropbox/Doctorado/PFIS-WB/PDFs Foundation Piloto de prueba/FOUNDATION PILOTAJE DE IMPORTACION'  
#Change directory
os.chdir(path)
#Create a list with the pdf files. 
pdfs = []
for file in glob2.glob("**/*.pdf"):
    pdfs.append(file)
print(len(pdfs))

    # Create a list where we are going to save our dictionaries generated. 
dicts_fundation_one=[]
custData = {}
dictionary={'Pfizer Inc.':0,'Clovis Oncology':0,'Roche Pharma':0, 'No_tiene':0}

for pdf in pdfs:
    string = convert_pdf_to_txt(pdf)
    #print(string)

    if 'Partner Name' in string or 'PARTNER NAME' in string: 
        lines = list(filter(None,string.split('\n')))
        for i in range(len(lines)):
            if 'Partner Name' in lines[i] or 'PARTNER NAME' in lines[i]:
                print(lines[i] + 'Nombre del archivo: '+ pdf )
                if 'Pfizer Inc' in lines[i]:
                    dictionary['Pfizer Inc.']+=1
                elif 'Clovis Oncology' in lines[i] or 'CLOVIS ONCOLOGY' in lines[i]:
                    dictionary['Clovis Oncology']+=1
                elif 'Roche Pharma' in lines[i]:
                    dictionary['Roche Pharma']+=1
                #print(lines[i][13:])
    else:
        dictionary['No_tiene']+=1
        print('No tiene' + 'Nombre del archivo: '+ pdf )


print(dictionary)
    #print("NOMBRE DEL PDF: "+ pdf +"\n"+string)


        