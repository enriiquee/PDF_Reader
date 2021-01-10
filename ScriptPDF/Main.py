from ScriptPDF.Function_script import *

#Start script
if __name__ == '__main__':
    
    #path of folder containing several PDFs
    path = r'/Users/pax-32/Dropbox/Lector_adobe/'     
    #Change directory
    os.chdir(path)
    #Create a list with the pdf files. 
    pdfs = []
    for file in glob.glob("*.pdf"):
        pdfs.append(file)

    #Create a list where we are going to save our dictionaries generated. 
    dicts_fundation_one=[]
    for pdf in pdfs:
        string = convert_pdf_to_txt(pdf)
        print(string)
        #print("NOMBRE DEL PDF: "+ pdf +"\n"+string)
        custData=detectData(string)
        if custData["Test_Type"]=="FoundationOne DX1":
            #print(custData.keys())
            dicts_fundation_one.append(custData)
        else:
            pass




#Detect what type of chip we have: 

fundation_one_generator(dicts_fundation_one)
