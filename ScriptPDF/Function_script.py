import xlsxwriter, glob, os
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from six import StringIO


#Definimos la función para convertir los pdfs en lineas. 
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()

    return str.replace("\\n","\n")

#Debido a que existen distintos tipos de archivo, vamos a crear una función que detecte qué tipo de archivo es: 

def detect_type_of_file(string):
    #Comprobamos que los archivos contengan el Partner Name, ya que existen de Clovis, de Pfizer y de Roche
    type_of_file=""
    if 'Partner Name' in string or 'PARTNER NAME' in string: 
        lines = list(filter(None,string.split('\n'))) 
        for i in range(len(lines)): #Comprobamos de que tipo de Partner es. 
            if 'Partner Name' in lines[i] or 'PARTNER NAME' in lines[i]:
                #print(lines[i] + 'Nombre del archivo: '+ pdf )
                if 'Pfizer Inc' in lines[i]:
                    type_of_file='Pfizer Inc'
                    return type_of_file
                elif 'Clovis Oncology' in lines[i] or 'CLOVIS ONCOLOGY' in lines[i]:
                    type_of_file='Clovis Oncology'
                    return type_of_file
                elif 'Roche Pharma' in lines[i]:
                    type_of_file='Roche Pharma'
                    return type_of_file
                else:
                    print("Hay un archivo que no cumple este formato "+ pdf)
    
    else:
         print('No tiene' + 'Nombre del archivo: '+ pdf )

    #Eliminamos las tabulaciones. 
    #lines = list(filter(None,string.split('\n')))

    # if 'Test Type' in string: #Comprobamos si existe el test type en el archivo.
    #     lines = list(filter(None,string.split('\n')))
    #     for i in range(len(lines)):
    #         if 'Test Type' in lines[i]:
    #             if 'Liquid' in lines[i]:
    #                 test_type='Liquid'
    #                 return test_type
    #             elif 'FoundationOne DX1' in lines[i]:
    #                 test_type='FoundationOne DX1'
    #                 return test_type
    #             elif '(SOLID)' in lines[i]:
    #                 test_type='Solid'
    #                 return test_type
    # else:
    #     test_type="No_Type"
    #     return test_type
    #     print("No tiene tipo de muestra")
        

#Definimos la función para detectar los datos de interés. 
def detectData(string, type_of_partner):
    if type_of_partner=='Pfizer Inc':
        print("Detecto Pfizer")
        return detectData_Pfizer(string)
    elif type_of_partner=='Clovis Oncology':
        print("Detecto Clovis")
        return detectData_Clovis(string)
    elif type_of_partner=='Roche Pharma':
        print("Detecto Roche")
        return detectData_Roche(string)


def detectData_Clovis(string):
    """
    Allow to extract info from Clovis Oncology 
    :Param: string
    :return : Dictionary with all the elements extracted.
    """
    #Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []

    #We do the classification between the two types of files that we have with foundationOne Liquid

    if 'Test Type FoundationOne Liquid' in lines:
        if 'GENOMIC FINDINGS' in lines:
            print("Naranja")
            for i in range(len(lines)):
                print(lines[i])
                if 'FMI Test Order #' in lines[i]:
                    custData['FMI_Test'] = lines[i+1]
                elif 'Subject ID' in lines[i]:
                    custData['Subjet'] = lines[i+1]
                elif 'Test Type' in lines[i]:
                    custData['Test_Type'] = lines[i][10:]
                elif 'Partner Name' in lines[i]:
                    custData['Partner_Name']= lines[i][13:]        
                elif 'Partner Study ID' in lines[i]:
                    custData['Partner_Study'] = lines[i][17:]
                elif 'FMI Study ID' in lines[i]:
                    custData['FMI_Study_ID'] = lines[i][13:]  
                elif 'Report Date' in lines[i]:
                    custData['Date'] = lines[i+1]
                elif 'Site ID' in lines[i]:
                    custData['Site_ID'] = lines[i][8:]
                elif 'Date of Birth' in lines[i]:
                    custData['Date_of_Birth'] = lines[i][14:]   
                elif 'Diagnosis' in lines[i]:
                    custData['Diagnosis'] = lines[i][10:]
                elif 'Specimen ID' in lines[i]:
                    custData['Specimen_ID'] = lines[i][12:]
                elif 'Sample Type' in lines[i]:
                    custData['Sample_type'] = lines[i][12:]
                elif 'Site' in lines[i]:
                    custData['Site'] = lines[i][5:]
                elif 'Collection Date' in lines[i]:
                    custData['Collection_Date'] = lines[i][16:]
                elif 'Received Date' in lines[i]:
                    custData['Received_Date'] = lines[i][14:]
                elif 'Visit Type' in lines[i]:
                    custData['Visit_Type'] = lines[i][11:]

                #GENOMIC FINDINGS
                elif "GENOMIC FINDINGS" in lines[i]:
                    #print(lines[i])
                    while lines[i]!='GENE':
                        #print(lines[i])
                        i+=1
                    try:
                        i+=1
                        while "ALTERATION" not in lines[i]: 
                            genenomic_findings.append(lines[i])
                            i+=1

                        if "ALTERATION" in lines[i]:
                            i+=1
                            #print(lines[i])
                            while "GENOMIC SIGNATURES" not in lines[i]:
                                alts_findings.append(lines[i])
                                i+=1
                    except:
                        print("Error in Genomic Findings")

               #Biomarker
                elif 'GENOMIC SIGNATURES' in lines[i]:
                    try:
                        while lines[i]!='Biomarker':
                            i+=1

                        i+=1
                        while 'Result' not in lines[i]:
                            a=lines[i]
                            if 'Not Evaluable' in lines[i]:
                                genomic_signatures.append(lines[i][:-14])
                                alts_signatures.append(lines[i][-13:])
                                i+=1
                                a=lines[i]
                            else:
                                genomic_signatures.append(lines[i])
                                alts_signatures.append(lines[i+1])
                                i+=1
                    except:
                        print("Error in genomic signatures")
                        
                #Variants of unkwnon significance
                elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
                    while lines[i]!='GENE':
                        #print(lines[i])
                        i+=1
                    try:
                        i+=1
                        while "ALTERATION" not in lines[i]: 
                            #print(lines[i])
                            unknown_signatures.append(lines[i])
                            i+=1

                        if "ALTERATION" in lines[i]:
                            i+=1
                            #print(lines[i])
                            while "Foundation" not in lines[i]:
                                alts_unknown.append(lines[i])
                                i+=1
                    except:
                        print("Error in Genomic Findings")      
 
        
            #Now create a dictionary in order to produce and excel file: 

            #For genenomic_findings
            for gene in genenomic_findings:
                custData[gene] = "" #initialize a blank string to add to
            for gene, alt in zip(genenomic_findings, alts_findings):
                custData[gene] = custData[gene] + ";" + alt
                custData[gene] = custData[gene].strip(";")
                
            #For genomic_signatures
            for gene in genomic_signatures:
                custData[gene] = "" #initialize a blank string to add to
            for gene, alt in zip(genomic_signatures, alts_signatures):
                custData[gene] = custData[gene] + ";" + alt
                custData[gene] = custData[gene].strip(";")

            #For unknown_signatures
            for gene in unknown_signatures:
                custData[gene] = "" #initialize a blank string to add to
            for gene, alt in zip(unknown_signatures, alts_unknown):
                custData[gene] = custData[gene] + ";" + alt
                custData[gene] = custData[gene].strip(";")


            return custData
        
        elif 'STUDY-RELATED DELETERIOUS ALTERATION(S)' in lines:
            for i in range(len(lines)):
                print(lines[i])
                if 'FMI Test Order #' in lines[i]:
                    custData['FMI_Test'] = lines[i+1]
                elif 'Subject ID' in lines[i]:
                    custData['Subjet'] = lines[i+1]
                elif 'Test Type' in lines[i]:
                    custData['Test_Type'] = lines[i][10:]
                elif 'Report Date' in lines[i]:
                    custData['Date'] = lines[i][12:]
                elif 'Partner Name' in lines[i]:
                    custData['Partner_Name']= lines[i][13:]        
                elif 'Partner Study ID' in lines[i]:
                    custData['Partner_Study'] = lines[i][17:]
                elif 'FMI Study ID' in lines[i]:
                    if 'TEST' not in lines[i+1]:
                        custData['FMI_Study_ID'] = lines[i][13:]+lines[i+1]
                    else:
                        custData['FMI_Study_ID'] = lines[i][13:]  
                elif 'Site ID' in lines[i]:
                    custData['Site_ID'] = lines[i][8:]
                elif 'Date of Birth' in lines[i]:
                    custData['Date_of_Birth'] = lines[i][14:]   
                elif 'Diagnosis' in lines[i]:
                    custData['Diagnosis'] = lines[i][10:]
                elif 'Specimen ID' in lines[i]:
                    custData['Specimen_ID'] = lines[i][12:]
                elif 'Sample Type' in lines[i]:
                    custData['Sample_type'] = lines[i][12:]
                elif 'Site' in lines[i]:
                    custData['Site'] = lines[i][5:]
                elif 'Collection Date' in lines[i]:
                    custData['Collection_Date'] = lines[i][16:]
                elif 'Received Date' in lines[i]:
                    custData['Received_Date'] = lines[i][14:]
                elif 'Visit Type' in lines[i]:
                    custData['Visit_Type'] = lines[i][11:]
                elif "STUDY-RELATED DELETERIOUS ALTERATION(S)" in lines[i]:
                            #print(lines[i])
                            while lines[i]!='GENE':
                                print(lines[i])
                                i+=1
                            try:
                                i+=1
                                while "ALTERATION" not in lines[i]: 
                                    genenomic_findings.append(lines[i])
                                    i+=1

                                if "ALTERATION" in lines[i]:
                                    j=0
                                    i+=1
                                    #print(lines[i])
                                    while j<len(genenomic_findings):
                                        alts_findings.append(lines[i])
                                        j+=1
                                        i+=1
                            except:
                                print("STUDY-RELATED ALTERATION(S) IDENTIFIED")
            #For genenomic_findings
            for gene in genenomic_findings:
                custData[gene] = "" #initialize a blank string to add to
            for gene, alt in zip(genenomic_findings, alts_findings):
                custData[gene] = custData[gene] + ";" + alt
                custData[gene] = custData[gene].strip(";")
            
            return custData

def detectData_Pfizer(string):
    """
    Allow to extract info from Pfizer files
    :Param: string
    :return : Dictionary with all the elements extracted.
    """
#Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
   
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []

    #print(lines)

    #Vemos que tipo de FoundationOne es:
    if 'Test Type FoundationOne Liquid AB1' in lines:
        print("Liquid")
        for i in range(len(lines)):
            print(lines[i])
            if 'FMI Test Order #' in lines[i]:
                custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                custData['Subjet'] = lines[i+1]
            elif 'Test Type' in lines[i]:
                custData['Test_Type'] = lines[i][10:]
            elif 'Report Date' in lines[i]:
                custData['Date'] = lines[i][12:]
            elif 'Partner Name' in lines[i]:
                custData['Partner_Name']= lines[i][13:]        
            elif 'Partner Study ID' in lines[i]:
                custData['Partner_Study'] = lines[i][17:]
            elif 'FMI Study ID' in lines[i]:
                if 'TEST' not in lines[i+1]:
                    custData['FMI_Study_ID'] = lines[i][13:]+lines[i+1]
                else:
                    custData['FMI_Study_ID'] = lines[i][13:]  
            elif 'Site ID' in lines[i]:
                custData['Site_ID'] = lines[i][8:]
            elif 'Date of Birth' in lines[i]:
                custData['Date_of_Birth'] = lines[i][14:]   
            elif 'Diagnosis' in lines[i]:
                custData['Diagnosis'] = lines[i][10:]
            elif 'Specimen ID' in lines[i]:
                custData['Specimen_ID'] = lines[i][12:]
            elif 'Sample Type' in lines[i]:
                custData['Sample_type'] = lines[i][12:]
            elif 'Site' in lines[i]:
                custData['Site'] = lines[i][5:]
            elif 'Collection Date' in lines[i]:
                custData['Collection_Date'] = lines[i][16:]
            elif 'Received Date' in lines[i]:
                custData['Received_Date'] = lines[i][14:]
            elif 'Visit Type' in lines[i]:
                custData['Visit_Type'] = lines[i][11:]
            elif "STUDY-RELATED ALTERATION(S) IDENTIFIED" in lines[i]:
                        #print(lines[i])
                        while lines[i]!='GENE':
                            print(lines[i])
                            i+=1
                        try:
                            i+=1
                            while "ALTERATION" not in lines[i]: 
                                genenomic_findings.append(lines[i])
                                i+=1

                            if "ALTERATION" in lines[i]:
                                j=0
                                i+=1
                                #print(lines[i])
                                while j<len(genenomic_findings):
                                    alts_findings.append(lines[i])
                                    j+=1
                                    i+=1
                        except:
                            print("STUDY-RELATED ALTERATION(S) IDENTIFIED")
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
        
        return custData
        

    #Comprobamos que sea SOLID
    elif 'Test Type FoundationOne DX1 (SOLID)' in lines:
        print("Solid")
        for i in range(len(lines)):
            print(lines[i])
            if 'FMI Test Order #' in lines[i]:
                custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                custData['Subjet'] = lines[i+1]
            elif 'Test Type' in lines[i]:
                custData['Test_Type'] = lines[i][10:]
            elif 'Report Date' in lines[i]:
                custData['Date'] = lines[i][12:]
            elif 'Partner Name' in lines[i]:
                custData['Partner_Name']= lines[i][13:]        
            elif 'Partner Study ID' in lines[i]:
                custData['Partner_Study'] = lines[i][17:]
            elif 'FMI Study ID' in lines[i]:
                custData['FMI_Study_ID'] = lines[i][13:]  
            elif 'Site ID' in lines[i]:
                custData['Site_ID'] = lines[i][8:]
            elif 'Date of Birth' in lines[i]:
                custData['Date_of_Birth'] = lines[i][14:]   
            elif 'Diagnosis' in lines[i]:
                custData['Diagnosis'] = lines[i][10:]
            elif 'Specimen ID' in lines[i]:
                custData['Specimen_ID'] = lines[i][12:]
            elif 'Sample Type' in lines[i]:
                custData['Sample_type'] = lines[i][12:]
            elif 'Site' in lines[i]:
                custData['Site'] = lines[i][5:]
            elif 'Collection Date' in lines[i]:
                custData['Collection_Date'] = lines[i][16:]
            elif 'Received Date' in lines[i]:
                custData['Received_Date'] = lines[i][14:]
            elif 'Visit Type' in lines[i]:
                custData['Visit_Type'] = lines[i][11:]
            elif "STUDY-RELATED ALTERATION(S) IDENTIFIED" in lines[i]:
                        #print(lines[i])
                        while lines[i]!='GENE':
                            print(lines[i])
                            i+=1
                        try:
                            i+=1
                            while "ALTERATION" not in lines[i]: 
                                genenomic_findings.append(lines[i])
                                i+=1

                            if "ALTERATION" in lines[i]:
                                j=0
                                i+=1
                                #print(lines[i])
                                while j<len(genenomic_findings):
                                    alts_findings.append(lines[i])
                                    j+=1
                                    i+=1
                        except:
                            print("Error in Genomic Findings")          
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
        
        return custData


# If the sample is liquid or Liquid AB1




    else:
        pass


#path=r'C:/Users/enriq/Dropbox/Lector_adobe/PDF/'

#Change directory
#os.chdir(path)
# #Create a list with the pdf files. 
# pdfs = []
# for file in glob.glob("*.pdf"):
#     pdfs.append(file)
# #print (pdfs)

# #Create a list where we are going to save our dictionaries generated. 
# dicts_fundation_one=[]
# for pdf in pdfs:
#     string = convert_pdf_to_txt(pdf)
#     #print(string)
#     #print("NOMBRE DEL PDF: "+ pdf +"\n"+string)
#     print(detect_type_of_file(string))
        


# path = r'/Users/pax-32/Dropbox/Lector_adobe/PDF/tumor.pdf'
path=r'C:/Users/enriq/Dropbox/Lector_adobe/PDF/ORD-0900636-01.pdf'

string=convert_pdf_to_txt(path)
test=detect_type_of_file(string)

custData=detectData(string,test)
print(custData)







def detectData_Roche(string):

    #Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
   
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []
    
    

    for i in range(len(lines)):
        #print(lines[i])
        if 'FMI Test Order #' in lines[i]:
            custData['FMI_Test'] = lines[i+1]
        elif 'Subject ID' in lines[i]:
            custData['Subjet'] = lines[i+1]
        elif 'Test Type' in lines[i]:
            custData['Test_Type'] = lines[i][10:]
        elif 'Partner Name' in lines[i]:
            custData['Partner_Name']= lines[i][13:]        
        elif 'Partner Study ID' in lines[i]:
            custData['Partner_Study'] = lines[i][17:]
        elif 'FMI Study ID' in lines[i]:
            custData['FMI_Study_ID'] = lines[i][13:]  
        elif 'Report Date' in lines[i]:
            custData['Date'] = lines[i+1]
        elif 'Site ID' in lines[i]:
            custData['Site_ID'] = lines[i][7:]
        elif 'Date of Birth' in lines[i]:
            custData['Date_of_Birth'] = lines[i][14:]   
        elif 'Diagnosis' in lines[i]:
            custData['Diagnosis'] = lines[i][10:]
        elif 'Specimen ID' in lines[i]:
            custData['Specimen_ID'] = lines[i][12:]
        elif 'Sample Type' in lines[i]:
            custData['Sample_type'] = lines[i][12:]
        elif 'Site' in lines[i]:
            custData['Site'] = lines[i][5:]
        elif 'Collection Date' in lines[i]:
            custData['Collection_Date'] = lines[i][16:]
        elif 'Received Date' in lines[i]:
            custData['Received_Date'] = lines[i][14:]
        elif 'Visit Type' in lines[i]:
            custData['Visit_Type'] = lines[i][11:]
            
        #Potential Enrollment Eligible Alterations
        elif "Potential Enrollment Eligible Alterations" in lines[i]:
            while lines[i]!='GENE':
                #print(lines[i])
                i+=1
            try:
                i+=1
                if 'None Detected' in lines[i]:
                    continue
                    print(lines[i])
                else:
                    while "ALTERATION" not in lines[i]: 
                        genes_pot.append(lines[i])
                        i+=1

                    if "ALTERATION" in lines[i]:
                        i+=1
                        #print(lines[i])
                        while "GENOMIC FINDINGS" not in lines[i]:
                            alts_pot.append(lines[i])
                            i+=1
            except:
                print("Error in Potential Enrollment Eligible Alterations")

        #Genomic signatures
        elif "GENOMIC FINDINGS" in lines[i]:
            #print(lines[i])
            while lines[i]!='GENE':
                #print(lines[i])
                i+=1
            try:
                i+=1
                while "ALTERATION" not in lines[i]: 
                    genenomic_findings.append(lines[i])
                    i+=1

                if "ALTERATION" in lines[i]:
                    i+=1
                    #print(lines[i])
                    while "GENOMIC SIGNATURES" not in lines[i]:
                        alts_findings.append(lines[i])
                        i+=1
            except:
                print("Error in Genomic Findings")
                
        #Variants of unkwnon significance
        elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
            while lines[i]!='GENE':
                #print(lines[i])
                i+=1
            try:
                i+=1
                while "ALTERATION" not in lines[i]: 
                    #print(lines[i])
                    unknown_signatures.append(lines[i])
                    i+=1

                if "ALTERATION" in lines[i]:
                    i+=1
                    #print(lines[i])
                    while "Foundation" not in lines[i]:
                        alts_unknown.append(lines[i])
                        i+=1
            except:
                print("Error in Genomic Findings")      
        #Biomarker
        elif 'GENOMIC SIGNATURES' in lines[i]:
            while lines[i]!='Biomarker':
                i+=1
            try:
                i+=1
                while 'Result' not in lines[i]:
                    if 'Tumor Mutational' in lines[i]:
                        genomic_signatures.append(lines[i][0:24])
                        alts_signatures.append(lines[i][24:])
                        i+=1
                    else:
                        genomic_signatures.append(lines[i])
                        alts_signatures.append(lines[i+1])
                        i+=2
            except:
                print("Error in genomic signatures")

    #print(genomic_signatures)
    #print(alts_signatures)

    #Now create a dictionary in order to produce and excel file: 

    #For pottential genes
    for gene in genes_pot:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(genes_pot, alts_pot):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")

    #For genenomic_findings
    for gene in genenomic_findings:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(genenomic_findings, alts_findings):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")
        
     #For genomic_signatures
    for gene in genomic_signatures:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(genomic_signatures, alts_signatures):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")

     #For unknown_signatures
    for gene in unknown_signatures:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(unknown_signatures, alts_unknown):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")


    return custData


def fundation_one_generator(dicts_fundation_one):
    #Elements of foundation: 
    foundation_one = ['FMI_Test', 'Subjet', 'Date', 'Test_Type', 'Specimen_ID', 'Sample_type', 'Site', 'Collection_Date', 'Received_Date', 'Visit_Type', 'Partner_Name', 'Partner_Study', 'FMI_Study_ID', 'Site_ID', 'Date_of_Birth', 'Diagnosis',"ABL1","ACVR1B","AKT1","AKT2","AKT3","ALK","ALOX12B","AMER1", "APC","AR","ARAF","ARFRP1","ARID1A","ASXL1","ATM","ATR","ATRX","AURKA","AURKB","AXIN1","AXL","BAP1","BARD1","BCL2","BCL2L1","BCL2L2","BCL6","BCOR","BCORL1","BRAF","BRCA1","BRCA2","BRD4","BRIP1","BTG1","BTG2","BTK","C11orf30","CALR","CARD11","CASP8","CBFB","CBL","CCND1","CCND2","CCND3","CCNE1","CD22","CD274","CD70","CD79A","CD79B","CDC73","CDH1","CDK12","CDK4","CDK6","CDK8","CDKN1A","CDKN1B","CDKN2A","CDKN2B","CDKN2C","CEBPA","CHEK1","CHEK2","CIC","CREBBP","CRKL","CSF1R","CSF3R","CTCF","CTNNA1","CTNNB1","CUL3","CUL4A","CXCR4","CYP17A1","DAXX","DDR1","DDR2","DIS3","DNMT3A","DOT1L","EED","EGFR","EP300","EPHA3","EPHB1","EPHB4","ERBB2","ERBB3","ERBB4","ERCC4","ERG","ERRFI1","ESR1","EZH2","FAM46C","FANCA","FANCC","FANCG","FANCL","FAS","FBXW7","FGF10","FGF12","FGF14","FGF19","FGF23","FGF3","FGF4","FGF6","FGFR1","FGFR2","FGFR3","FGFR4","FH","FLCN","FLT1","FLT3","FOXL2","FUBP1","GABRA6","GATA3","GATA4","GATA6","GID4","GNA11","GNA13","GNAQ","GNAS","GRM3","GSK3B","H3F3A","HDAC1","HGF","HNF1A","HRAS","HSD3B1","ID3","IDH1","IDH2","IGF1R","IKBKE","IKZF1","INPP4B","IRF2","IRF4","IRS2","JAK1","JAK2","JAK3","JUN","KDM5A","KDM5C","KDM6A","KDR","KEAP1","KEL","KIT","KLHL6","KMT2A","KMT2D","KRAS","LTK","LYN","MAF","MAP2K1","MAP2K2","MAP2K4","MAP3K1","MAP3K13","MAPK1","MCL1","MDM2","MDM4","MED12","MEF2B","MEN1","MERTK","MET","MITF","MKNK1","MLH1","MPL","MRE11A","MSH2","MSH3","MSH6","MST1R","MTAP","MTOR","MUTYH","MYC","MYCL","MYCN","MYD88","NBN","NF1","NF2","NFE2L2","NFKBIA","NKX2-1","NOTCH1","NOTCH2","NOTCH3","NPM1","NRAS","NT5C2","NTRK1","NTRK2","NTRK3","P2RY8","PALB2","PARK2","PARP1","PARP2","PARP3","PAX5","PBRM1","PDCD1","PDCD1LG2","PDGFRA","PDGFRB","PDK1","PIK3C2B","PIK3C2G","PIK3CA","PIK3CB","PIK3R1","PIM1","PMS2","POLD1","POLE","PPARG","PPP2R1A","PPP2R2A","PRDM1","PRKAR1A","PRKCI","PTCH1","PTEN","PTPN11","PTPRO","QKI","RAC1","RAD21","RAD51","RAD51B","RAD51C","RAD51D","RAD52","RAD54L","RAF1","RARA","RB1","RBM10","REL","RET","RICTOR","RNF43","ROS1","RPTOR","SDHA","SDHB","SDHC","SDHD","SETD2","SF3B1","SGK1","SMAD2","SMAD4","SMARCA4","SMARCB1","SMO","SNCAIP","SOCS1","SOX2","SOX9","SPEN","SPOP","SRC","STAG2","STAT3","STK11","SUFU","SYK","TBX3","TEK","TET2","TGFBR2","TIPARP","TNFAIP3","TNFRSF14","TP53","TSC1","TSC2","TYRO3","U2AF1","VEGFA","VHL","WHSC1","WHSC1L1","WT1","XPO1","XRCC2","ZNF217","ZNF703"]
    df = pd.DataFrame(data=None, columns=foundation_one, dtype=None, copy=False)

    for d in dicts_fundation_one:
        df = df.append(d, ignore_index=True).fillna(0)
    print(df)
    df.to_excel (r'Foundation_One_dataframe.xlsx', index = True, header=True)
    print(os.getcwd)
