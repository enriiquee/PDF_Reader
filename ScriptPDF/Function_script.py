import xlsxwriter, glob, os
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from six import StringIO

"""
This script contains the functions that we are going to use to perform the different tasks (Convert pdf to text, detect the type of file we have, detect the type of data and the functions that correspond to each type of 
pdf. )

"""

    
def convert_pdf_to_txt(path):
    """
    We define the function to convert the pdfs into lines. 
    :input: path of the files
    :return: lines of the pdf
    """
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

def detect_type_of_file(string, pdf):
    """
    Because there are different file types, we will create a function that detects what type of file it is: 
    We check that the files contain the Partner Name, as they exist of Clovis, Pfizer and Roche
    """
    type_of_file=""
    # print(string)
    if 'Partner Name' in string or 'PARTNER NAME' in string: 
        lines = list(filter(None,string.split('\n')))
        #print(lines) 
        for i in range(len(lines)): #Comprobamos de que tipo de Partner es. 
            if 'Partner Name' in lines[i] or 'PARTNER NAME' in lines[i]:
                #print(lines[i] + 'Nombre del archivo: '+ pdf )
                if 'Pfizer Inc' in lines[i]:
                    type_of_file='Pfizer Inc'
                    return type_of_file
                elif 'Clovis Oncology' in lines[i] or 'CLOVIS ONCOLOGY' in lines[i]:
                    type_of_file='Clovis Oncology'
                    return type_of_file
                elif 'Roche Pharma' in lines[i] or 'Roche' in lines[i]:
                    type_of_file='Roche Pharma'
                    return type_of_file
                elif 'BRISTOL-MYERS' in lines[i]:
                    type_of_file='Bristol-Myers'
                    return type_of_file
                elif 'Johnson and Johnson' in lines[i] or 'Janssen' in lines[i]:
                    type_of_file='Janssen'
                    return type_of_file
                    # print("Detecto Janssen")
                else:
                    type_of_file='No cumple formato'
                    print("Hay un archivo que no cumple este formato "+pdf)
                    return type_of_file
    
    elif 'Janssen Study' in string:
        type_of_file='Janssen'
        return type_of_file

    elif 'INVITAE DIAGNOSTIC TESTING RESULTS' in string:
        type_of_file='Invitae'
        return type_of_file       
    else:
         print('No contiene información sobre el Partner. ' + 'Nombre del archivo: '+ pdf )

        # Eliminamos las tabulaciones. 
        # lines = list(filter(None,string.split('\n')))

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
        
def detectData(string, type_of_partner, pdf,TypeOftest):
    """
    Here we detect what kind of data we have based on Partner Name used previously. 
    """
    if type_of_partner=='Pfizer Inc':
        # print("Detecto Pfizer")
        return detectData_Pfizer(string, pdf,TypeOftest)
    elif type_of_partner=='Clovis Oncology':
        # print("Detecto Clovis")
        return detectData_Clovis(string, pdf,TypeOftest)
    elif type_of_partner=='Roche Pharma':
        # print("Detecto Roche")
        return detectData_Roche(string, pdf,TypeOftest)
    elif type_of_partner=='Bristol-Myers':
        # print("Detecto Bristol")
        return detectData_Bristol(string,pdf,TypeOftest)
    elif type_of_partner=='Janssen':
        # print("Detecto Janssen")
        return detectData_Janssen(string,pdf,TypeOftest)
    elif type_of_partner=='Invitae':
        # print("Detecto Bristol")
        return detectData_Invitae(string,pdf,TypeOftest)

        

def detect_Type_of_pdf(string, pdf):
    """"
    This function allow us to identify what type of file we have.
    """
    
    TypeOftest=""
    lines=list(filter(None, string.split('\n')))
    # print(lines)
    
    if 'alterations within hundreds of cancer related genes. The CF3 test was utilized.' in lines or 'The CF3 test was utilized.' in lines or 'Genes Assayed in CF3:' in lines:
        TypeOftest='CF3'
    elif 'The Foundation Medicine test is a next-generation sequencing (NGS) based assay which identifies' in lines and 'genomic alterations within hundreds of cancer-related genes.' in lines or 'Genes Assayed in DX1:' in lines or 'Test Type FoundationOne DX1' in lines:
        if 'FoundationOne® CDx CTA is designed to include genes known to be somatically altered in human' in lines:
            TypeOftest='CTA_SOLID'
        else:
            TypeOftest='DX1'
    elif 'substitutions, insertions and deletion alterations (indels) and copy number alterations (CNAs) in 324 genes, and select gene rearrangements, as' in lines or 'Test Type FoundationOne DX1 (SOLID)' in lines:
        TypeOftest='CTA_SOLID'
    elif 'This test is a next generation sequencing assay based on the FoundationOne® Liquid CDx CTA assay using the AB1 bait set to detect substitutions,' in lines and 'insertions and deletion alterations (indels) and '\
        'copy number alterations (CNAs) in 324 genes, and select gene rearrangements, as well as genomic' in lines or 'Test Type FoundationOne Liquid AB1' in lines:
        TypeOftest='CTA_LIQUID_AB1'
    elif 'FoundationOne® Liquid is a next generation sequencing (NGS) assay that identifies clinically relevant genomic alterations in circulating tumor DNA.' in lines:
        TypeOftest='CTA_Liquid'
    elif 'The Foundation Medicine test is a next-generation (NGS) based assay which identifies genomic' in lines and 'alterations within 395 cancer-related genes. The T7 assay was utilized (Please see appendices below' in lines or 'Test Type FoundationOne Liquid' in lines:
        TypeOftest='T7_395'
    elif 'FoundationOne is a next-generation sequencing (NGS) based assay that identifies genomic alterations within hundreds of cancer-related genes.' in lines or 'Test Type FoundationOne' in lines:
        if 'STUDY-RELATED DELETERIOUS ALTERATION(S)' in lines:
            TypeOftest=''
        else:
            TypeOftest='T7_315_28'
    elif 'Note: This is a QUALIFIED report. This specimen failed to meet minimum performance' in lines or 'Janssen Study PCR3002 Clinical Trial Assay' in lines:
        TypeOftest='QUALIFIED'

    elif 'INVITAE DIAGNOSTIC TESTING RESULTS' in lines:
        TypeOftest='Invitae'        
    if TypeOftest=="":
        TypeOftest="***Error in: ***"+pdf
        
    return(TypeOftest)
    
    
        
def detectData_Clovis(string, pdf, type_of_test):
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
    custData['File']=pdf
    custData['TypeOftest']=type_of_test

    #We do the classification between the two types of files that we have with foundationOne Liquid

    if 'Test Type FoundationOne Liquid' in lines or 'Test Type FoundationOne' in lines:
            
        if 'GENOMIC FINDINGS' in lines:  
            print("Clovis Naranja")
            
            #target_ibdex = lines.index('Result')
            #lines=lines[:target_ibdex+1]
            first_iter=True
            for i in range(len(lines)):
                # print(lines[i])
                if 'FMI Test Order' in lines[i]:
                    if 'FMI_Test' not in custData:
                        custData['FMI_Test'] = lines[i+1]
                elif 'Subject ID' in lines[i]:
                    if 'Subjet' not in custData:
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
                    if lines[i][11:]=="":
                        custData['Date']=lines[i+1]
                    else:
                        custData['Date'] = lines[i][11:]
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
                elif 'Unfortunately, we were not able' in lines[i]:
                    custData['Sample Failure']='Yes'
                

                #GENOMIC FINDINGS
                elif "GENOMIC FINDINGS" in lines[i]:
                    #print(lines[i])
                    while lines[i]!='GENE':
                        #print(lines[i])
                        i+=1
                    try:
                        i+=1
                        while "ALTERATION" not in lines[i]: 
                            if 'GENOMIC SIGNATURES' in lines[i]:
                                i+=1
                            else:
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
                        print("Error in Genomic Findings " + pdf)

                #Biomarker
                elif 'GENOMIC SIGNATURES' in lines[i] and first_iter:
                    first_iter=False
                    try:
                        while 'Biomarker' not in lines[i]:
                            i+=1
                        i+=1
                        while 'Result' not in lines[i]:
                            if 'Not Evaluable' in lines[i]:
                                genomic_signatures.append(lines[i][:-14])
                                alts_signatures.append(lines[i][-13:])
                                i+=1
                            else:
 
                                genomic_signatures.append(lines[i])
                                i+=1
                        if "Result" in lines[i]:
                            if 'Electronically' in lines[i+1]:
                                i+=1
                            else:
                                j=0
                                i+=1
                                #print(lines[i])
                                while j<len(genomic_signatures):
                                    alts_signatures.append(lines[i])
                                    j+=1
                                    i+=1
                    except:
                        print("Error in genomic signatures " +pdf )
                        
                #Variants of unkwnon significance
                elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
                    custData['Study Related']='No'
                    while lines[i]!='GENE':
                        #print(lines[i])
                        i+=1
                    try:
                        i+=1
                        while "ALTERATION" not in lines[i]: 
                            #print(lines[i])
                            unknown_signatures.append(lines[i]+"*")
                            i+=1

                        if "ALTERATION" in lines[i]:
                            i+=1
                            #print(lines[i])
                            while "Foundation" not in lines[i]:
                                alts_unknown.append(lines[i])
                                i+=1
                    except:
                        print("Error in Genomic Findings " +pdf)      
 
        
            #Now create a dictionary in order to produce and excel file: 
            # print(genenomic_findings, alts_findings)
            # print(genomic_signatures,alts_signatures)
            # print(unknown_signatures,alts_unknown )
            
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
            print('Clovis Blanco/Negro')

            for i in range(len(lines)):
                # print(lines[i])
                if 'FMI Test Order #' in lines[i]:
                    if 'FMI_Test' not in custData:
                        custData['FMI_Test'] = lines[i+1]
                elif 'Subject ID' in lines[i]:
                    if 'Subjet' not in custData:
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
                elif 'Year of Birth' in lines[i]:
                    custData['Date_of_Birth'] = lines[i][13:]   
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
                                # print(lines[i])
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
                                print("STUDY-RELATED ALTERATION(S) IDENTIFIED "+ pdf)
            #For genenomic_findings
            for gene in genenomic_findings:
                custData[gene] = "" #initialize a blank string to add to
            for gene, alt in zip(genenomic_findings, alts_findings):
                custData[gene] = custData[gene] + ";" + alt
                custData[gene] = custData[gene].strip(";")
            
            return custData

    else:
        print('Clovis ')
        first_iter=True
        custData['Test_Type']='Foundation Medicine'
        custData['Visit_Type']='Not applicable'
        custData['Date_of_Birth']='Not applicable'
        custData['FMI_Test']='Not applicable'
        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI Test Order' in lines[i]:
                custData['FMI_Test'] = lines[i][12:]
            elif 'PARTNER SUBJECT ID' in lines[i]:
                if 'Subjet' not in custData:
                    custData['Subjet'] = lines[i+1]
            elif 'PARTNER NAME' in lines[i]:
                custData['Partner_Name']= lines[i][13:]        
            elif 'PARTNER STUDY ID' in lines[i]:
                custData['Partner Study ID'] = lines[i][17:]
            elif 'FMI STUDY ID' in lines[i]:
                custData['FMI_Study_ID'] = lines[i][13:]  
            elif 'REPORT DATE' in lines[i]:
                if lines[i][11:]=="":
                    custData['Date']=lines[i+1]
                else:
                    custData['Date'] = lines[i][11:]
            elif 'Site ID' in lines[i]:
                custData['Site_ID'] = lines[i][8:]
            elif 'Date of Birth' in lines[i]:
                custData['Date_of_Birth'] = lines[i][14:]   
            elif 'DIAGNOSIS' in lines[i]:
                custData['Diagnosis'] = lines[i+1]
            elif 'SPECIMEN TYPE' in lines[i]:
                custData['Site'] = lines[i][14:]
            elif 'SAMPLE TYPE' in lines[i]:
                custData['Sample_type'] = lines[i][12:]
                if custData['Sample_type']=='Peripheral Blood':
                    custData['Site']=lines[i][23:]

            elif 'COLLECTION DATE' in lines[i]:
                custData['Collection_Date'] = lines[i][16:]
            elif 'RECEIVED DATE' in lines[i]:
                custData['Received_Date'] = lines[i][14:]
            elif 'Visit Type' in lines[i]:
                custData['Visit_Type'] = lines[i][11:]
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'

            #GENOMIC FINDINGS
            elif "STUDY-RELATED DELETERIOUS ALTERATION(S) IDENTIFIED" in lines[i]:

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
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(genenomic_findings):
                            alts_findings.append(lines[i])
                            j+=1
                            i+=1
                except:
                    print("Error in Genomic Findings " + pdf)

            #Biomarker
            elif 'CANCER RELATED ALTERATIONS IDENTIFIED' in lines[i] and first_iter:
                first_iter=False
                try:
                    while 'GENE' not in lines[i]:
                        i+=1
                    i+=1
                    while 'ALTERATION' not in lines[i]:
                        if 'Not Evaluable' in lines[i]:
                            genomic_signatures.append(lines[i][:-14])
                            genomic_signatures.append(lines[i][-13:])
                            i+=1
                        elif 'No reportable variants' in lines[i]:
                            break
                        else:
                            genomic_signatures.append(lines[i])
                            i+=1
                    if "ALTERATION" in lines[i]:
                        if 'Electronically' in lines[i+1]:
                            i+=1
                        else:
                            j=0
                            i+=1
                            #print(lines[i])
                            while j<len(genomic_signatures):
                                alts_signatures.append(lines[i])
                                j+=1
                                i+=1
                except:
                    print("Error in genomic signatures " +pdf )
                    
            #Variants of unkwnon significance
            elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
                custData['Study Related']='No'
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        if 'No reportable variants detected' in lines[i]:
                            break
                        else:                            
                            #print(lines[i])
                            unknown_signatures.append(lines[i]+"*")
                            i+=1

                    if "ALTERATION" in lines[i]:
                        i+=1
                        j=0
                        
                        
                        #print(lines[i])
                        while j<len(unknown_signatures):
                            alts_unknown.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Genomic Findings " +pdf)      

    
        #Now create a dictionary in order to produce and excel file: 
        # print(genenomic_findings, alts_findings)
        # print(genomic_signatures,alts_signatures)
        # print(unknown_signatures,alts_unknown )
        
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
            
        # #For genomic_signatures
        for gene in genomic_signatures:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genomic_signatures, alts_signatures):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")

        # #For unknown_signatures
        for gene in unknown_signatures:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(unknown_signatures, alts_unknown):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")

        #print(custData)
        return custData

def detectData_Pfizer(string, pdf,type_of_test):
    """
    Allow to extract info from Pfizer files
    :Param: string, pdf, type_of_test
    :return : Dictionary with all the elements extracted.
    """
    #Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
   
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []
    custData['File']=pdf
    custData['TypeOftest']=type_of_test


    #print(lines)

    #Vemos que tipo de FoundationOne es:
    if 'Test Type FoundationOne Liquid AB1' in lines:
        print("Pfizer FoundationOne Liquid AB1")

        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI Test Order' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                custData['Subjet'] = lines[i+1]
            elif 'Test Type' in lines[i]:
                custData['Test_Type'] = lines[i][10:]
            elif 'Report Date' in lines[i]:
                if 'Date' not in custData:
                    if lines[i][12:]!="":
                        custData['Date'] = lines[i][12:]
                    else:
                        custData['Date']=lines[i+1]
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
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'
            elif "STUDY-RELATED ALTERATION(S) IDENTIFIED" in lines[i]:
        
                        #print(lines[i])
                        while lines[i]!='GENE':
                            # print(lines[i])
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
                            print("STUDY-RELATED ALTERATION(S) IDENTIFIED "+ pdf)
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
        
        return custData
    #Comprobamos que sea SOLID
    elif 'Test Type FoundationOne DX1 (SOLID)' in lines:
        print("Pfizer Solid")
        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI Test Order' in lines[i]:
                if 'FMI_Test' not in custData:
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
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'

            elif "STUDY-RELATED ALTERATION(S) IDENTIFIED" in lines[i]:
        
                        #print(lines[i])
                        while lines[i]!='GENE':
                            # print(lines[i])
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
                            print("Error in Genomic Findings "+ pdf)          
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
        
        return custData

    elif 'Test Type FoundationOne DX1' in lines:
        print('Pfizer FoundationOne DX1 solo')
        if 'GENOMIC FINDINGS' in lines:
            first_iter=True
            # print("Naranja")
                
            #target_ibdex = lines.index('Result')
            #lines=lines[:target_ibdex+1]
        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI Test Order' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                if 'Subjet' not in custData:
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
                if lines[i][11:]=="":
                    custData['Date']=lines[i+1]
                else:
                    custData['Date'] = lines[i][11:]
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
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'

            #GENOMIC FINDINGS
            elif "GENOMIC FINDINGS" in lines[i]:
                #print(lines[i])
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        if 'GENOMIC SIGNATURES' in lines[i]:
                            i+=1
                        else:
                            genenomic_findings.append(lines[i])
                            i+=1

                    if "ALTERATION" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(genenomic_findings):
                            alts_findings.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Genomic Findings "+ pdf)

            #Biomarker
            elif 'GENOMIC SIGNATURES' in lines[i] and first_iter:
                first_iter=False
                try:
                    while lines[i]!='Biomarker':
                        i+=1

                    i+=1
                    while 'Result' not in lines[i]:
                        if 'Not Evaluable' in lines[i]:
                            genomic_signatures.append(lines[i][:-14] )
                            alts_signatures.append(lines[i][-13:])
                            i+=1
                            
                        else:
                            genomic_signatures.append(lines[i])
                            i+=1
                        

                    if "Result" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        if 'Electronically' in lines[i]:
                            continue
                        else:
                            while j<len(genomic_signatures):
                                alts_signatures.append(lines[i])
                                j+=1
                                i+=1
                        
                except:
                    print("Error in genomic signatures "+pdf)
                    
            #Variants of unkwnon significance
            elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
                custData['Study Related']='No'
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        #print(lines[i])
                        unknown_signatures.append(lines[i]+"*")
                        i+=1

                    if "ALTERATION" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(unknown_signatures):
                            alts_unknown.append(lines[i])
                            j+=1
                            i+=1
                except:
                    print("Error in Genomic Findings "+pdf)  
                    
                    
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
        
        # print(genenomic_findings, alts_findings)   
        # print(genomic_signatures, alts_signatures) 
        # print(unknown_signatures, alts_unknown) 
        
        return custData

    else:
        print('Pfizer')
        first_iter=True
        custData['Test_Type']='Foundation Medicine'
        custData['Visit_Type']='Not applicable'
        custData['Date_of_Birth']='Not applicable'
        custData['FMI_Test']='Not applicable'
        
        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI SAMPLE ID' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i][14:]
            elif 'Subject ID' in lines[i]:
                if 'Subjet' not in custData:
                    custData['Subjet'] = lines[i+1]
            elif 'PARTNER NAME' in lines[i]:
                custData['Partner_Name']= lines[i][13:]        
            elif 'PARTNER STUDY ID' in lines[i]:
                custData['Partner Study ID'] = lines[i][17:]
            elif 'FMI STUDY ID' in lines[i]:
                custData['FMI_Study_ID'] = lines[i][13:]  
            elif 'Report Date' in lines[i]:
                if lines[i][11:]=="":
                    custData['Date']=lines[i+1]
                else:
                    custData['Date'] = lines[i][11:]
            elif 'Site ID' in lines[i]:
                custData['Site_ID'] = lines[i][8:]
            elif 'PATIENT DATE OF BIRTH' in lines[i]:
                custData['Date_of_Birth'] = lines[i][21:]   
            elif 'DIAGNOSIS' in lines[i]:
                custData['Diagnosis'] = lines[i][10:]
            elif 'SPECIMEN TYPE' in lines[i]:
                custData['Specimen_ID'] = lines[i][14:]
            elif 'SAMPLE TYPE' in lines[i]:
                custData['Sample_type'] = lines[i][12:]
            elif 'Site' in lines[i]:
                custData['Site'] = lines[i][5:]
            elif 'SPECIMEN SITE' in lines[i]:
                custData['Site']=lines[i][13:]
            elif 'COLLECTION DATE' in lines[i]:
                custData['Collection_Date'] = lines[i][16:]
            elif 'RECEIVED DATE' in lines[i]:
                custData['Received_Date'] = lines[i][14:]
            elif 'Visit Type' in lines[i]:
                custData['Visit_Type'] = lines[i][11:]
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'


            #GENOMIC FINDINGS
            elif "Enrollment Criteria" in lines[i]:
                #print(lines[i])
                while lines[i]!='Gene Name':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "Alteration" not in lines[i]: 
                        genenomic_findings.append(lines[i])
                        i+=1

                    if "Alteration" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(genenomic_findings):
                            alts_findings.append(lines[i])
                            j+=1
                            i+=1
                except:
                    print("Error in Genomic Findings " + pdf)

            #Biomarker
            elif 'Cancer Related Alterations Identified' in lines[i] and first_iter:
                first_iter=False
                try:
                    while 'GENE' not in lines[i]:
                        i+=1
                    i+=1
                    while 'ALTERATION' not in lines[i]:
                        if 'Not Evaluable' in lines[i]:
                            genomic_signatures.append(lines[i][:-14])
                            genomic_signatures.append(lines[i][-13:])
                            i+=1
                        elif 'No alterations detected' in lines[i]:
                            break
                        else:
                            genomic_signatures.append(lines[i])
                            i+=1
                    if "ALTERATION" in lines[i]:
                        if 'Electronically' in lines[i+1]:
                            i+=1
                        else:
                            j=0
                            i+=1
                            #print(lines[i])
                            while j<len(genomic_signatures):
                                alts_signatures.append(lines[i])
                                j+=1
                                i+=1
                except:
                    print("Error in genomic signatures " +pdf )
                    
            #Variants of unkwnon significance
            elif "Variants of Unknown Significance Identified" in lines[i]:
                custData['Study Related']='No'
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        #print(lines[i])
                        unknown_signatures.append(lines[i]+"*")
                        i+=1

                    if "ALTERATION" in lines[i]:
                        i+=1
                        j=0
                        #print(lines[i])
                        while j<len(unknown_signatures):
                            alts_unknown.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Genomic Findings " +pdf)      

    
        #Now create a dictionary in order to produce and excel file: 
        # print(genenomic_findings, alts_findings)
        # print(genomic_signatures,alts_signatures)
        # print(unknown_signatures,alts_unknown )
        
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
            
        # #For genomic_signatures
        for gene in genomic_signatures:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genomic_signatures, alts_signatures):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")

        # #For unknown_signatures
        for gene in unknown_signatures:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(unknown_signatures, alts_unknown):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")

        #print(custData)
        return custData

def detectData_Roche(string, pdf,type_of_test):
    """
    Extract the data from Roche files
    """

    #Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
   
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    Enrollment_gene, Enrollment_alt=[],[]
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []
    custData['File']=pdf    
    custData['TypeOftest']=type_of_test
    
    if 'Test Type FoundationOne DX1' in lines:
        print('Roche FoundationOne DX1')
        for i in range(len(lines)):
            #print(lines[i])
            if 'FMI Test Order' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                if 'Subjet' not in custData:
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
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'

                
            #Potential Enrollment Eligible Alterations
            elif "Potential Enrollment Eligible Alterations" in lines[i]:
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    if 'None Detected' in lines[i]:
                        continue
                        # print(lines[i])
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
                    print("Error in Potential Enrollment Eligible Alterations "+pdf)

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
                    print("Error in Genomic Findings "+pdf)
                    
            #Variants of unkwnon significance
            elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
                custData['Study Related']='No'
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        #print(lines[i])
                        unknown_signatures.append(lines[i]+"*")
                        i+=1

                    if "ALTERATION" in lines[i]:
                        i+=1
                        #print(lines[i])
                        while "Foundation" not in lines[i]:
                            alts_unknown.append(lines[i])
                            i+=1
                except:
                    print("Error in Genomic Findings "+pdf)      
            #Biomarker
            elif 'GENOMIC SIGNATURES' in lines[i]:
                while lines[i]!='Biomarker':
                    i+=1
                try:
                    i+=1
                    while 'Result' not in lines[i]:
                        if 'Tumor Mutational' in lines[i]:
                            genomic_signatures.append(lines[i][0:23])
                            alts_signatures.append(lines[i][24:])
                            i+=1
                        else:
                            genomic_signatures.append(lines[i])
                            alts_signatures.append(lines[i+1])
                            i+=2
                except:
                    print("Error in genomic signatures Biomarkers "+pdf)

        #print(genenomic_findings, alts_findings)
        #print(genomic_signatures,alts_signatures)
        #print(unknown_signatures,alts_unknown )

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
    
    else:
        custData['Test_Type']='Foundation Medicine'
        custData['Visit_Type']='Not applicable'
        custData['FMI_Test']='Not applicable'
        print('Roche')
        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI Test Order' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                if 'Subjet' not in custData:
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
                custData['Date_of_Birth'] = lines[i][22:]   
            elif 'Diagnosis' in lines[i]:
                custData['Diagnosis'] = lines[i][10:]
            elif 'Specimen ID' in lines[i]:
                custData['Specimen_ID'] = lines[i][12:]
            elif 'Sample Type' in lines[i]:
                custData['Sample_type'] = lines[i][12:]
            elif 'Sample Type' in lines[i]:
                custData['Site'] = lines[i][5:]
            elif 'Collection Date' in lines[i]:
                custData['Collection_Date'] = lines[i][16:]
            elif 'Received Date' in lines[i]:
                custData['Received_Date'] = lines[i][14:]
            elif 'Visit Type' in lines[i]:
                custData['Visit_Type'] = lines[i][11:]
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'


                
            elif "Enrollment Eligible Alterations" in lines[i]:
                try:
                    while lines[i]!='GENE':
                        i+=1
                    i+=1
                    
                    while "ALTERATION" not in lines[i]:
                        if 'No Eligible Variants Detected' in lines[i]:
                            break
                        else:
                        #print(lines[i])
                            Enrollment_gene.append(lines[i])
                            i+=1 
                    if 'ALTERATION' in lines[i]:
                        i+=1
                        j=0
                        #print(lines[i])
                        while j<len(Enrollment_gene):
                            Enrollment_alt.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Gene Findings "+pdf)

            #Genomic signatures
            elif "Genomic Alterations Identified" in lines[i]:
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
                        j=0
                        #print(lines[i])
                        while j<len(genenomic_findings ):
                            alts_findings.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Genomic Findings "+pdf)
                        
            
            elif "Variants of Unknown Significance Identified" in lines[i]:
                custData['Study Related']='No'
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        #print(lines[i])
                        unknown_signatures.append(lines[i]+"*")
                        i+=1

                    if "ALTERATION" in lines[i]:
                        i+=1
                        j=0
                        #print(lines[i])
                        while j<len(unknown_signatures):
                            alts_unknown.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Genomic Findings " +pdf)      

             
            #Biomarker
            elif 'Advanced Genomic Analysis' in lines[i]:
                while lines[i]!='Biomarker':
                    i+=1
                try:
                    i+=1
                    while 'Status/Score' not in lines[i]:
                        if 'Tumor Mutational' in lines[i]:
                            genomic_signatures.append(lines[i][0:23])
                            alts_signatures.append(lines[i][24:])
                            i+=1
                        else:
                            genomic_signatures.append(lines[i])
                            i+=1
                    if 'Status/Score' in lines[i]:
                        i+=1
                        j=0
                        #print(lines[i])
                        while j<len(genomic_signatures):
                            alts_signatures.append(lines[i])
                            i+=1
                            j+=1  
                except:
                    print("Error in genomic signatures Biomarkers "+pdf)
        # print(Enrollment_gene, Enrollment_alt)
        # print(genenomic_findings, alts_findings)
        # print(genomic_signatures,alts_signatures)
        # print(unknown_signatures,alts_unknown )

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
        
        #print(custData)
        return custData

def detectData_Bristol(string,pdf,type_of_test):

    """
    Allow to extract info from Bristol information 
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
    custData['File']=pdf

    #We do the classification between the two types of files that we have with foundationOne Liquid
    print('Bristol')
    first_iter=True
    custData['TypeOftest']=type_of_test
    custData['Test_Type']='Foundation Medicine'
    custData['Visit_Type']='Not applicable'
    custData['FMI_Test']='Not applicable'
    #custData['Date_of_Birth']='Not applicable'
    
    for i in range(len(lines)):
        #print(lines[i])
        if 'FMI Test Order' in lines[i]:
            custData['FMI_Test'] = lines[i][12:]
        elif 'PARTNER SUBJECT ID' in lines[i]:
            if 'Subjet' not in custData:
                custData['Subjet'] = lines[i+1]
        elif 'PARTNER NAME' in lines[i]:
            custData['Partner_Name']= lines[i][13:]        
        elif 'PARTNER STUDY ID' in lines[i]:
            custData['Partner Study ID'] = lines[i][17:]
        elif 'FMI STUDY ID' in lines[i]:
            custData['FMI_Study_ID'] = lines[i][13:]  
        elif 'REPORT DATE' in lines[i]:
            if lines[i][11:]=="":
                custData['Date']=lines[i+1]
            else:
                custData['Date'] = lines[i][11:]
        elif 'Site ID' in lines[i]:
            custData['Site_ID'] = lines[i][8:]
        elif 'SUBJECT DATE OF BIRTH' in lines[i]:
            custData['Date_of_Birth'] = lines[i][21:]   
        elif 'DIAGNOSIS' in lines[i]:
            custData['Diagnosis'] = lines[i+1]
        elif 'SPECIMEN TYPE' in lines[i]:
            custData['Specimen_ID'] = lines[i][14:]
        elif 'SAMPLE TYPE' in lines[i]:
            custData['Sample_type'] = lines[i][12:]
            if custData['Sample_type']=='Peripheral Blood':
                custData['Site']=lines[i][23:]
        elif 'COLLECTION DATE' in lines[i]:
            custData['Collection_Date'] = lines[i][16:]
        elif 'RECEIVED DATE' in lines[i]:
            custData['Received_Date'] = lines[i][14:]
            
        elif 'Unfortunately, we were not able' in lines[i]:
            custData['Sample Failure']='Yes'
 
        #GENOMIC FINDINGS
        elif "STUDY-RELATED DELETERIOUS ALTERATION(S) IDENTIFIED" in lines[i]:
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
                    j=0
                    i+=1
                    #print(lines[i])
                    while j<len(genenomic_findings):
                        alts_findings.append(lines[i])
                        j+=1
                        i+=1
            except:
                print("Error in Genomic Findings " + pdf)

        #Biomarker
        elif 'CANCER RELATED ALTERATIONS IDENTIFIED' in lines[i] and first_iter:
            first_iter=False
            try:
                while 'GENE' not in lines[i]:
                    i+=1
                i+=1
                while 'ALTERATION' not in lines[i]:
                    if 'Not Evaluable' in lines[i]:
                        genomic_signatures.append(lines[i][:-14])
                        genomic_signatures.append(lines[i][-13:])
                        i+=1
                    elif 'No reportable variants detected' in lines[i]:
                        break
                    else:
                        genomic_signatures.append(lines[i])
                        i+=1
                if "ALTERATION" in lines[i]:
                    if 'Electronically' in lines[i+1]:
                        i+=1
                    else:
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(genomic_signatures):
                            alts_signatures.append(lines[i])
                            j+=1
                            i+=1
            except:
                print("Error in genomic signatures " +pdf )
            
        elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
            custData['Study Related']='No'
            while lines[i]!='GENE':
                #print(lines[i])
                i+=1
            try:
                i+=1
                while "ALTERATION" not in lines[i]: 
                    #print(lines[i])
                    unknown_signatures.append(lines[i]+"*")
                    i+=1

                if "ALTERATION" in lines[i]:
                    i+=1
                    j=0
                    #print(lines[i])
                    while j<len(unknown_signatures):
                        alts_unknown.append(lines[i])
                        i+=1
                        j+=1
            except:
                print("Error in Genomic Findings " +pdf)   

    #Now create a dictionary in order to produce and excel file: 
    # print(genenomic_findings, alts_findings)
    # print(genomic_signatures,alts_signatures)
    # print(unknown_signatures,alts_unknown )
    
    #For genenomic_findings
    for gene in genenomic_findings:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(genenomic_findings, alts_findings):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")
        
    # #For genomic_signatures
    for gene in genomic_signatures:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(genomic_signatures, alts_signatures):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")

    # #For unknown_signatures
    for gene in unknown_signatures:
        custData[gene] = "" #initialize a blank string to add to
    for gene, alt in zip(unknown_signatures, alts_unknown):
        custData[gene] = custData[gene] + ";" + alt
        custData[gene] = custData[gene].strip(";")

    # print(custData)
    return custData

def detectData_Janssen(string, pdf, type_of_test):
    """
    Allow to extract info from Pfizer files
    :Param: string, pdf, type_of_test
    :return : Dictionary with all the elements extracted.
    """
    #Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
    # print(lines)
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []
    custData['File']=pdf
    custData['TypeOftest']=type_of_test
    first_iter=True


    #print(lines)

    #Vemos que tipo de FoundationOne es:
    if 'Test Type FoundationOne DX1' in lines:
        print("Janssen FoundationOne DX1")

        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI Test Order #' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                custData['Subjet'] = lines[i+1]
            elif 'Test Type' in lines[i]:
                custData['Test_Type'] = lines[i][10:]
            elif 'Report Date' in lines[i]:
                if 'Date' not in custData:
                    if lines[i][12:]!="":
                        custData['Date'] = lines[i][12:]
                    else:
                        custData['Date']=lines[i+1]
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
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'
            
            #GENOMIC FINDINGS
            elif "GENOMIC FINDINGS" in lines[i]:
                #print(lines[i])
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        if 'GENOMIC SIGNATURES' in lines[i]:
                            i+=1
                        else:
                            genenomic_findings.append(lines[i])
                            i+=1

                    if "ALTERATION" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(genenomic_findings):
                            alts_findings.append(lines[i])
                            i+=1
                            j+=1
                except:
                    print("Error in Genomic Findings "+ pdf)

            #Biomarker
            elif 'GENOMIC SIGNATURES' in lines[i] and first_iter:
                first_iter=False
                try:
                    while lines[i]!='Biomarker':
                        i+=1

                    i+=1
                    while 'Result' not in lines[i]:
                        if 'Not Evaluable' in lines[i]:
                            genomic_signatures.append(lines[i][:-14] )
                            alts_signatures.append(lines[i][-13:])
                            i+=1
                            
                        else:
                            genomic_signatures.append(lines[i])
                            i+=1
                        

                    if "Result" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        if 'Electronically' in lines[i]:
                            continue
                        else:
                            while j<len(genomic_signatures):
                                alts_signatures.append(lines[i])
                                j+=1
                                i+=1
                        
                except:
                    print("Error in genomic signatures "+pdf)
                    
            #Variants of unkwnon significance
            elif "VARIANTS OF UNKNOWN SIGNIFICANCE" in lines[i]:
                custData['Study Related']='No'
                while lines[i]!='GENE':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "ALTERATION" not in lines[i]: 
                        #print(lines[i])
                        unknown_signatures.append(lines[i]+"*")
                        i+=1

                    if "ALTERATION" in lines[i]:
                        j=0
                        i+=1
                        #print(lines[i])
                        while j<len(unknown_signatures):
                            alts_unknown.append(lines[i])
                            j+=1
                            i+=1
                except:
                    print("Error in Genomic Findings "+pdf)  
                    
                    
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
        
        # print(custData)
        return custData
    
    elif any("Janssen Study" in s for s in lines):
        print("Janssen Study QUALIFIED")
        custData['Test_Type'] = 'Janssen QUALIFIED'
        custData['Partner_Name']= 'Janssen'
        custData['Date_of_Birth'] = 'No-info'
        custData['Sample_type'] = 'No-info'
        custData['Site'] = 'No-info'
        custData['Received_Date'] = 'No info'
        custData['Visit_Type'] = 'No info'
        for i in range(len(lines)):
            # print(lines[i])
            if 'FMI ID' in lines[i]:
                if 'FMI_Test' not in custData:
                    custData['FMI_Test'] = lines[i+1]
            elif 'Subject ID' in lines[i]:
                custData['Subjet'] = lines[i+1]
            elif 'Report Date' in lines[i]:
                if 'Date' not in custData:
                    if lines[i][12:]!="":
                        custData['Date'] = lines[i][12:]
                    else:
                        custData['Date']=lines[i+1]                     
            elif 'Partner Study ID' in lines[i]:
                custData['Partner_Study'] = lines[i][17:]
            elif 'FMI Study ID' in lines[i]:
                custData['FMI_Study_ID'] = lines[i][13:]  
            elif 'Site ID' in lines[i]:
                custData['Site_ID'] = lines[i][8:]         
            elif 'Subject Diagnosis' in lines[i]:
                custData['Diagnosis'] = lines[i][18:]
            elif 'Specimen ID' in lines[i]:
                custData['Specimen_ID'] = lines[i][12:]
            elif 'Specimen Collection Date' in lines[i]:
                custData['Collection_Date'] = lines[i][25:]            
            elif 'Unfortunately, we were not able' in lines[i]:
                custData['Sample Failure']='Yes'

            elif "Stratification Information" in lines[i]:
                #print(lines[i])
                while lines[i]!='Criteria':
                    #print(lines[i])
                    i+=1
                try:
                    i+=1
                    while "Variant Report" not in lines[i]: 
                        genenomic_findings.append(lines[i])
                        i+=1
                        # print(genenomic_findings)

                    if "GENE" in lines[i+1]:
                        j=0
                        i+=1
                        while 'Status' not in lines[i]:
                            if 'GENE' in lines[i]:
                                i+=1
                            else:
                                genenomic_findings.append(lines[i])
                                i+=1
                                # print(genenomic_findings)

                        i+=1
                        while 'ALTERATION' not in lines[i]:
                            alts_findings.append(lines[i])
                            i+=1
                            j+=1
                        i+=1
                        while j<len(genenomic_findings):
                            alts_findings.append(lines[i])
                            i+=1
                            j+=1
                        # print(alts_findings)
                except:
                    print("Error in Genomic Findings "+ pdf)

                number=len(lines)
                while i < len(lines):
                    if 'None' not in lines[i]:
                        i+=1
                    else: 
                        custData['Sample Failure']='Check the file'
                        i+=1

                     

        
        #For genenomic_findings
        for gene in genenomic_findings:
            custData[gene] = "" #initialize a blank string to add to
        for gene, alt in zip(genenomic_findings, alts_findings):
            custData[gene] = custData[gene] + ";" + alt
            custData[gene] = custData[gene].strip(";")
        
        
        # print(custData)
        return custData
    else:
        print("Detected a type on Janssen that we don't know it.")

def detectData_Invitae(string,pdf,type_of_test):
    """
    Allow to extract info from Invitae files
    :Param: string, pdf, type_of_test
    :return : Dictionary with all the elements extracted.
    """
    #Creamos una lista con las lineas separadas. 
    lines = list(filter(None,string.split('\n')))
    print(lines)
    custData = {} #Diccionario donde se van a ir guardando todas las variables
    genes_pot, alts_pot = [], [] 
    genenomic_findings, alts_findings = [], []
    genomic_signatures, alts_signatures = [], []
    unknown_signatures, alts_unknown = [], []
    custData['File']=pdf
    custData['TypeOftest']=type_of_test
    first_iter=True

    if 'INVITAE DIAGNOSTIC TESTING RESULTS' in lines:
        pass
        print("Invitae")
        if 'RESULT: NEGATIVE' in lines:
            for i in range(len(lines)):
                # print(lines[i])
                if 'Invitae #:' in lines[i]:
                    if 'FMI_Test' not in custData:
                        custData['FMI_Test'] = lines[i+3]
                # elif 'Subject ID' in lines[i]:
                #     custData['Subjet'] = lines[i+1]
                # elif 'Test Type' in lines[i]:
                #     custData['Test_Type'] = lines[i][10:]
                elif 'Report date' in lines[i]:
                    if 'Date' not in custData:
                        custData['Date']=lines[i+3]
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
                elif 'Unfortunately, we were not able' in lines[i]:
                    custData['Sample Failure']='Yes'   
        elif 'RESULT: UNCERTAIN':
            pass
        else:
            print('Invitae Diagnostic Results Error in: ', pdf)
    else:
        print('Invitae files incorrect formart ', pdf)
def detectData_Caris(string,pdf,type_of_test):
    pass


def fundation_one_generator(dicts_fundation_one, pdfs): 
    """
    Create a excel file with the data extracted previously. 
    :input: Dictionary with the data
    :output: excel file. 
    """
    #Elements of foundation: 
    information_main_list=[]
    
    foundation_one=['File','TypeOftest','Study Related','Sample Failure','FMI_Test', 'Date', 'Test_Type', 'Sample_type', 'Site', 'Collection_Date', 'Received_Date', 'Visit_Type', 'Partner_Name', 'FMI_Study_ID', 'Date_of_Birth', 'Diagnosis',"ABL1","ACVR1B","AKT1","AKT2","AKT3","ALK","ALOX12B","AMER1","APC","AR","ARAF","ARFRP1","ARID1A","ASXL1","ATM","ATR","ATRX","AURKA","AURKB","AXIN1","AXL","BAP1","BARD1","BCL2","BCL2L1","BCL2L2","BCL6","BCOR","BCORL1","BRAF","BRCA1","BRCA2","BRD4","BRIP1","BTG1","BTG2","BTK","C11orf30","CALR","CARD11","CASP8","CBFB","CBL","CCND1","CCND2","CCND3","CCNE1","CD22","CD274","CD70","CD79A","CD79B","CDC73","CDH1","CDK12","CDK4","CDK6","CDK8","CDKN1A","CDKN1B","CDKN2A","CDKN2B","CDKN2C","CEBPA","CHEK1","CHEK2","CIC","CREBBP","CRKL","CSF1R","CSF3R","CTCF","CTNNA1","CTNNB1","CUL3","CUL4A","CXCR4","CYP17A1","DAXX","DDR1","DDR2","DIS3","DNMT3A","DOT1L","EED","EGFR","EP300","EPHA3","EPHB1","EPHB4","ERBB2","ERBB3","ERBB4","ERCC4","ERG","ERRFI1","ESR1","EZH2","FAM46C","FANCA","FANCC","FANCG","FANCL","FAS","FBXW7","FGF10","FGF12","FGF14","FGF19","FGF23","FGF3","FGF4","FGF6","FGFR1","FGFR2","FGFR3","FGFR4","FH","FLCN","FLT1","FLT3","FOXL2","FUBP1","GABRA6","GATA3","GATA4","GATA6","GID4","GNA11","GNA13","GNAQ","GNAS","GRM3","GSK3B","H3F3A","HDAC1","HGF","HNF1A","HRAS","HSD3B1","ID3","IDH1","IDH2","IGF1R","IKBKE","IKZF1","INPP4B","IRF2","IRF4","IRS2","JAK1","JAK2","JAK3","JUN","KDM5A","KDM5C","KDM6A","KDR","KEAP1","KEL","KIT","KLHL6","KMT2A","KMT2D","KRAS","LTK","LYN","MAF","MAP2K1","MAP2K2","MAP2K4","MAP3K1","MAP3K13","MAPK1","MCL1","MDM2","MDM4","MED12","MEF2B","MEN1","MERTK","MET","MITF","MKNK1","MLH1","MPL","MRE11A","MSH2","MSH3","MSH6","MST1R","MTAP","MTOR","MUTYH","MYC","MYCL","MYCN","MYD88","NBN","NF1","NF2","NFE2L2","NFKBIA","NKX2-1","NOTCH1","NOTCH2","NOTCH3","NPM1","NRAS","NT5C2","NTRK1","NTRK2","NTRK3","P2RY8","PALB2","PARK2","PARP1","PARP2","PARP3","PAX5","PBRM1","PDCD1","PDCD1LG2","PDGFRA","PDGFRB","PDK1","PIK3C2B","PIK3C2G","PIK3CA","PIK3CB","PIK3R1","PIM1","PMS2","POLD1","POLE","PPARG","PPP2R1A","PPP2R2A","PRDM1","PRKAR1A","PRKCI","PTCH1","PTEN","PTPN11","PTPRO","QKI","RAC1","RAD21","RAD51","RAD51B","RAD51C","RAD51D","RAD52","RAD54L","RAF1","RARA","RB1","RBM10","REL","RET","RICTOR","RNF43","ROS1","RPTOR","SDHA","SDHB","SDHC","SDHD","SETD2","SF3B1","SGK1","SMAD2","SMAD4","SMARCA4","SMARCB1","SMO","SNCAIP","SOCS1","SOX2","SOX9","SPEN","SPOP","SRC","STAG2","STAT3","STK11","SUFU","SYK","TBX3","TEK","TET2","TGFBR2","TIPARP","TNFAIP3","TNFRSF14","TP53","TSC1","TSC2","TYRO3","U2AF1","VEGFA","VHL","WHSC1","WHSC1L1","WT1","XPO1","XRCC2","ZNF217","ZNF703","BCR","CD74","ETV4","ETV5","ETV6","EWSR1","EZR","MYB","NUTM1","RSPO2","SDC4","SLC34A2","TERC","TERT","TMPRSS2","C17orf39","EMSY","FAM123B","MLL","MLL2","MSI","MYCL1","TMB","ETV1","GLI1","GPR124","LRP1B","CDH5","TP53BP1","CHUK","PTPRD","ZNRF3","FANCI","MKNK2","NSD1","SMARCD1","SOX10","STAT4","TOE1","TRRAP","IL7R","SH2B3","CRLF2","GEN1","MLL3","PAK3","TOP2A","ARID1B","FANCD2","RUNX1T1","SLIT2","ABL2","APCDD1","ARID2","BACH1","BCL2A1","BLM","BMPR1A","CDH2","CDH20","CHD2","CHD4","CRBN","CUL4B","CYLD","DICER1","EPHA5","EPHA6","EPHA7","EPHB6","FAM175A","FANCE","FANCF","FANCM","FAT1","FAT3","FGF7","FLT4","FOXP1","FRS2","GALNT12","GATA1","GATA2","GREM1","GRIN2A","HLA-A","HLA-B","HLA-C","HOXB13","HSP90AA1","IGF1","IGF2","IGF2R","INHBA","INSR","KAT6A","KMT2C","LMO1","LRP6","LZTR1","MAGI2","NCOR1","NOTCH4","NUDT1","NUP93","PAK7","PARP4","PHLPP2","PIK3C3","PIK3CG","PIK3R2","PLCG2","PNRC1","PREX2","PRKDC","PRSS1","PRSS8","PTCH2","RAD50","RANBP2","RPA1","RUNX1","SMAD3","SPTA1","TAF1","TNF","TNKS","TNKS2","TOP1","TSHR","WISP3","XRCC3","ZBTB2","Loss of Heterozygosity score","Tumor Mutational Burden Score","Tumor Mutational Burden","Microsatellite Instability"]
    
    CTA_SOLID=["ABL1","ACVR1B","AKT1","AKT2","AKT3","ALK","ALOX12B","AMER1","APC","AR","ARAF","ARFRP1","ARID1A","ASXL1","ATM","ATR","ATRX","AURKA","AURKB","AXIN1","AXL","BAP1","BARD1","BCL2","BCL2L1","BCL2L2","BCL6","BCOR","BCORL1","BRAF","BRCA1","BRCA2","BRD4","BRIP1","BTG1","BTG2","BTK","C11orf30","CALR","CARD11","CASP8","CBFB","CBL","CCND1","CCND2","CCND3","CCNE1","CD22","CD274","CD70","CD79A","CD79B","CDC73","CDH1","CDK12","CDK4","CDK6","CDK8","CDKN1A","CDKN1B","CDKN2A","CDKN2B","CDKN2C","CEBPA","CHEK1","CHEK2","CIC","CREBBP","CRKL","CSF1R","CSF3R","CTCF","CTNNA1","CTNNB1","CUL3","CUL4A","CXCR4","CYP17A1","DAXX","DDR1","DDR2","DIS3","DNMT3A","DOT1L","EED","EGFR","EP300","EPHA3","EPHB1","EPHB4","ERBB2","ERBB3","ERBB4","ERCC4","ERG","ERRFI1","ESR1","EZH2","FAM46C","FANCA","FANCC","FANCG","FANCL","FAS","FBXW7","FGF10","FGF12","FGF14","FGF19","FGF23","FGF3","FGF4","FGF6","FGFR1","FGFR2","FGFR3","FGFR4","FH","FLCN","FLT1","FLT3","FOXL2","FUBP1","GABRA6","GATA3","GATA4","GATA6","GID4","GNA11","GNA13","GNAQ","GNAS","GRM3","GSK3B","H3F3A","HDAC1","HGF","HNF1A","HRAS","HSD3B1","ID3","IDH1","IDH2","IGF1R","IKBKE","IKZF1","INPP4B","IRF2","IRF4","IRS2","JAK1","JAK2","JAK3","JUN","KDM5A","KDM5C","KDM6A","KDR","KEAP1","KEL","KIT","KLHL6","KMT2A","KMT2D","KRAS","LTK","LYN","MAF","MAP2K1","MAP2K2","MAP2K4","MAP3K1","MAP3K13","MAPK1","MCL1","MDM2","MDM4","MED12","MEF2B","MEN1","MERTK","MET","MITF","MKNK1","MLH1","MPL","MRE11A","MSH2","MSH3","MSH6","MST1R","MTAP","MTOR","MUTYH","MYC","MYCL","MYCN","MYD88","NBN","NF1","NF2","NFE2L2","NFKBIA","NKX2-1","NOTCH1","NOTCH2","NOTCH3","NPM1","NRAS","NT5C2","NTRK1","NTRK2","NTRK3","P2RY8","PALB2","PARK2","PARP1","PARP2","PARP3","PAX5","PBRM1","PDCD1","PDCD1LG2","PDGFRA","PDGFRB","PDK1","PIK3C2B","PIK3C2G","PIK3CA","PIK3CB","PIK3R1","PIM1","PMS2","POLD1","POLE","PPARG","PPP2R1A","PPP2R2A","PRDM1","PRKAR1A","PRKCI","PTCH1","PTEN","PTPN11","PTPRO","QKI","RAC1","RAD21","RAD51","RAD51B","RAD51C","RAD51D","RAD52","RAD54L","RAF1","RARA","RB1","RBM10","REL","RET","RICTOR","RNF43","ROS1","RPTOR","SDHA","SDHB","SDHC","SDHD","SETD2","SF3B1","SGK1","SMAD2","SMAD4","SMARCA4","SMARCB1","SMO","SNCAIP","SOCS1","SOX2","SOX9","SPEN","SPOP","SRC","STAG2","STAT3","STK11","SUFU","SYK","TBX3","TEK","TET2","TGFBR2","TIPARP","TNFAIP3","TNFRSF14","TP53","TSC1","TSC2","TYRO3","U2AF1","VEGFA","VHL","WHSC1","WHSC1L1","WT1","XPO1","XRCC2","ZNF217","ZNF703","BCR","CD74","ETV4","ETV5","ETV6","EWSR1","EZR","MYB","NUTM1","RSPO2","SDC4","SLC34A2","TERC","TERT","TMPRSS2","Loss of Heterozygosity score","Tumor Mutational Burden Score","Tumor Mutational Burden","Microsatellite Instability"]
    
    DX1=["ABL1","ALK","ARFRP1","ATRX","BAP1","BCL6","BRCA1","BTG2","CASP8","CCND3","CD74","CDK12","CDKN1B","CHEK1","CSF1R","CUL3","DDR1","EED","EPHB1","ERCC4","ETV5","FAM123B","FANCL","FGF14","FGF6","FH","FUBP1","GNA11","GSK3B","HRAS","IGF1R","IRF4","JUN","KEAP1","LTK","MAP2K4","MDM2","MERTK","MLL","MSH3","MUTYH","MYD88","ACVR1B","ALOX12B","ARID1A","AURKA","BARD1","BCOR","BRCA2","BTK","CBFB","CCNE1","CD79A","CDK4","CDKN2A","CHEK2","CSF3R","CUL4A","DDR2","EGFR","EPHB4","ERG","ETV6","FAM46C","FAS","FGF19","FGFR1","FLCN","GABRA6","GNA13","H3F3A","HSD3B1","IKBKE","IRS2","KDM5A","KEL","LYN","MAP3K1","MDM4","MET","MLL2","MSH6","MYB","NBN","AKT1","APC","ASXL1","AURKB","BCL2","BCORL1","BRD4","C17orf39","CBL","CD22","CD79B","CDK6","CDKN2B","CIC","CTCF","CXCR4","DIS3","EMSY","ERBB2","ERRFI1","EWSR1","FANCA","FBXW7","FGF23","FGFR2","FLT1","GATA3","GNAQ","HDAC1","ID3","IKZF1","JAK1","KDM5C","KIT","MAF","MAP3K13","MED12","MITF","MPL","MST1R","MYC","NF1","AKT2","AR","ATM","AXIN1","BCL2L1","BCR","BRIP1","CALR","CCND1","CD274","CDC73","CDK8","CDKN2C","CREBBP","CTNNA1","CYP17A1","DNMT3A","EP300","ERBB3","ESR1","EZH2","FANCC","FGF10","FGF3","FGFR3","FLT3","GATA4","GNAS","HGF","IDH1","INPP4B","JAK2","KDM6A","KLHL6","MAP2K1","MAPK1","MEF2B","MKNK1","MRE11A","MTAP","MYCL1","NF2","AKT3","ARAF","ATR","AXL","BCL2L2","BRAF","BTG1","CARD11","CCND2","CD70","CDH1","CDKN1A","CEBPA","CRKL","CTNNB1","DAXX","DOT1L","EPHA3","ERBB4","ETV4","EZR","FANCG","FGF12","FGF4","FGFR4","FOXL2","GATA6","GRM3","HNF1A","IDH2","IRF2","JAK3","KDR","KRAS","MAP2K2","MCL1","MEN1","MLH1","MSH2","MTOR","MYCN","NFE2L2","NFKBIA","NPM1","NTRK3","PARP1","PDCD1","PIK3C2B","PIM1","PPP2R1A","PTCH1","RAC1","RAD51D","RB1","RNF43","SDHA","SF3B1","SMARCA4","SOX2","STAG2","TBX3","TGFBR2","TP53","VEGFA","XPO1","NKX2-1","NRAS","NUTM1","PARP2","PDCD1LG2","PIK3C2G","PMS2","PPP2R2A","PTEN","RAD21","RAD52","RBM10","ROS1","SDHB","SGK1","SMARCB1","SOX9","STAT3","TEK","TIPARP","TSC1","VHL","XRCC2","NOTCH1","NT5C2","P2RY8","PARP3","PDGFRA","PIK3CA","POLD1","PRDM1","PTPN11","RAD51","RAD54L","REL","RPTOR","SDHC","SLC34A2","SMO","SPEN","STK11","TERC","TMPRSS2","TSC2","WHSC1","ZNF217","NOTCH2","NTRK1","PALB2","PAX5","PDGFRB","PIK3CB","POLE","PRKAR1A","PTPRO","RAD51B","RAF1","RET","RSPO2","SDHD","SMAD2","SNCAIP","SPOP","SUFU","TERT","TNFAIP3","TYRO3","WHSC1L1","ZNF703","NOTCH3","NTRK2","PARK2","PBRM1","PDK1","PIK3R1","PPARG","PRKCI","QKI","RAD51C","RARA","RICTOR","SDC4","SETD2","SMAD4","SOCS1","SRC","SYK","TET2","TNFRSF14","U2AF1","WT1"]
    
    CF3=["ABL1","ARAF","BTK","CDK4","CTNNB1","ESR1","FLT3","HRAS","KIT","MET","MYD88","PDCD1LG2","PTPN11","SMO","AKT1","ATM","CCND1","CDK6","DDR2","EZH2","FOXL2","IDH1","KRAS","MPL","NF1","RAF1","STK11","ALK","BRAF","CD274","CDKN2A","EGFR","FGFR1","GNA11","IDH2","MAP2K1","MTOR","NPM1","PDGFRA","RB1","TERT","AR","BRCA2","CDH1","CRKL","ERRFI1","FGFR3","GNAS","JAK3","MAP2K2","MYCN","PALB2","PIK3CA","ROS1","VEGFA","APC","BRCA1","CHEK2","ERBB2","FGFR2","GNAQ","JAK2","MYC","NRAS","PDGFRB","RET","TP53","CDK12","MDM2","PTEN"]
    
    CTA_Liquid_AB1=["ABL1","AR","AURKB","BCOR","BTG2","CCND2","CDC73","CDKN2B","CSF3R","FLT1","GNA11","HNF1A","INPP4B","KDM5C","KRAS","MAPK1","MITF","MTAP","NF1","NRAS","PARP1","PDK1","POLE","PTPN11","RAD52","RNF43","SETD2","SNCAIP","STK11","TIPARP","VEGFA","SDHD","ACVR1B","ARAF","AXIN1","BCORL1","BTK","CCND3","CDH1","CDKN2C","CTCF","FLT3","GNA13","HRAS","IRF2","KDM6A","LTK","MCL1","MKNK1","MTOR","NF2","NT5C2","PARP2","PIK3C2B","PPARG","PTPRO","RAD54L","ROS1","SF3B1","SOCS1","SUFU","TMPRSS2","VHL","ALOX12B","ATR","BCL2L1","BRD4","CBFB","CD79A","CDKN1A","CREBBP","CXCR4","GATA4","H3F3A","IGF1R","JAK3","KLHL6","MAP2K4","MEN1","MSH3","MYCN","NOTCH2","P2RY8","PDCD1LG2","PIM1","PRKCI","RAD51B","REL","SDHA","SMARCA4","SRC","TERC","TSC2","XRCC2","AMER1","ATRX","BCL2L2","BRIP1","CBL","CD79B","CDKN1B","CRKL","CYP17A1","GATA6","HDAC1","IKBKE","JUN","KMT2A","MAP3K1","MERTK","MSH6","MYD88","NOTCH3","PALB2","PDGFRA","PMS2","PTCH1","RAD51C","RET","SDHB","SMARCB1","STAG2","TERT","TYRO3","ZNF217","APC","AURKA","BCL6","BTG1","CCND1","CD274","CDKN2A","CSF1R","DAXX","GID4","HGF","IKZF1","KDM5A","KMT2D","MAP3K13","MET","MST1R","NBN","NPM1","PARK2","PDGFRB","POLD1","PTEN","RAD51D","RICTOR","SDHC","SMO","STAT3","TGFBR2","U2AF1","ZNF703","AKT1","ARFRP1","AXL","BCR","C11orf30","CCNE1","CDK12","CEBPA","CTNNA1","FOXL2","GNAQ","HSD3B1","IRF4","KDR","LYN","MDM2","MLH1","MUTYH","NFE2L2","NTRK1","PARP3","PIK3C2G","PPP2R1A","QKI","RAF1","RPTOR","SGK1","SOX2","SYK","TNFAIP3","WHSC1","AKT2","ARID1A","BAP1","BRAF","CALR","CD22","CDK4","CHEK1","CTNNB1","FUBP1","GNAS","ID3","IRS2","KEAP1","MAF","MDM4","MPL","MYB","NFKBIA","NTRK2","PAX5","PIK3CA","PPP2R2A","RAC1","RARA","RSPO2","SLC34A2","SOX9","TBX3","TNFRSF14","WHSC1L1","AKT3","ASXL1","BARD1","BRCA1","CARD11","CD70","CDK6","CHEK2","CUL3","GABRA6","GRM3","IDH1","JAK1","KEL","MAP2K1","MED12","MRE11A","MYC","NKX2-1","NTRK3","PBRM1","PIK3CB","PRDM1","RAD21","RB1","SMAD2","SPEN","TEK","TP53","WT1","ALK","ATM","BCL2","BRCA2","CASP8","CD74","CDK8","CIC","CUL4A","GATA3","GSK3B","IDH2","JAK2","KIT","MAP2K2","MEF2B","MSH2","MYCL","NOTCH1","NUTM1","PDCD1","PIK3R1","PRKAR1A","RAD51","RBM10","SMAD4","SPOP","TET2","TSC1","XPO1"]
    
    CTA_Liquid=["APC","CDK6","FGFR2","PDCD1LG2","AR","CDK12","FOXL2","PTEN","PTPN11","RB1","SMO","STK11","TP53","VEGFA","ATM","BRCA1","BRCA2","CCND1","CD274","CDH1","CDK4","CDKN2A","CHEK2","CRKL","EGFR","ERBB2","ERRFI1","FGFR1","KRAS","MDM2","MET","MYC","MYCN","NF1","PALB2","ABL1","EZH2","JAK2","MTOR","MYD88","NRAS","PIK3CA","RAF1","AKT1","ALK","ARAF","BRAF","BTK","CTNNB1","DDR2","ESR1","RET","FGFR3","FLT3","GNA11","GNAQ","GNAS","HRAS","IDH1","IDH2","JAK3","KIT","MAP2K1","MAP2K2","MPL","NPM1","PDGFRA","PDGFRB","TERT","ROS1"]
    
    T7_395=["ABL1","AKT3","APCDD1","ARID1B","ATRX","BACH1","BCL2L1","BLM","BRD4","CARD11","CCND2","CD79B","CDH5","CDKN1A","CEBPA","CHUK","CRLF2","CUL3","DAXX","DNMT3A","EPHA5","EPHB6","ERG","FAM46C","FANCF","FAS","FGF12","FGF4","FGFR3","FLT3","FUBP1","GATA3","GLI1","GPR124","H3F3A","HNF1A","IDH1","IGF2R","INPP4B","JAK1","KDM5A","KEL","KMT2D","LTK","MAP2K2","MDM2","MERTK","MLH1","MST1R","MYCN","NF2","NOTCH2","NSD1","NUP93","PARP1","PBRM1","PHLPP2","PIK3CB","PMS2","PPP2R1A","PRKDC","PTEN","RAD50","RAD52","RB1","RNF43","RUNX1T1","SETD2","SMAD3","SMO","SOX9","STAG2","SYK","TERT","TNFAIP3","TOP2A","TSC2","VHL","XRCC3","ABL2","ALK","AR","ARID2","AURKA","BAP1","BCL2L2","BMPR1A","BRIP1","CASP8","CCND3","CDC73","CDK12","CDKN1B","CHD2","CIC","CSF1R","CUL4A","DDR1","DOT1L","EPHA6","ERBB2","ERRFI1","FANCA","FANCG","FAT1","FGF14","FGF6","FGFR4","FLT4","GABRA6","GATA4","GNA11","GREM1","HGF","HOXB13","IDH2","IKBKE","INSR","JAK2","KDM5C","KIT","LYN","MAP2K4","MDM4","MET","MPL","MTOR","MYD88","NFE2L2","NOTCH3","NTRK1","PAK3","PARP2","PDCD1LG2","PIK3C2B","PIK3CG","PNRC1","PRDM1","PRSS1","PTPN11","RAD51","RAD54L","RBM10","ROS1","SDHA","SF3B1","SMAD4","SNCAIP","SPEN","STAT3","TAF1","TNFRSF14","TP53","TSHR","WISP3","ZBTB2","ACVR1B","ALOX12B","ARAF","ASXL1","AURKB","BARD1","BCL6","BRAF","BTG1","CBFB","CCNE1","CDH1","CDK4","CDKN2A","CHD4","CRBN","CTCF","CUL4B","DDR2","EGFR","EPHA7","ERBB3","ESR1","FANCC","FANCI","FAT3","FGF19","FGF7","FH","FOXL2","GALNT12","GATA6","GNA13","GRIN2A","HLA-A","HRAS","IGF1","IKZF1","IRF2","JAK3","KDM6A","KLHL6","KRAS","LZTR1","MAP3K1","MED12","MITF","MRE11A","MUTYH","NBN","NFKBIA","NOTCH4","NTRK2","PAK7","PARP3","PDGFRA","PIK3C2G","PIK3R1","POLD1","PREX2","PRSS8","PTPRD","RAD51B","RAF1","REL","RPA1","SDHB","SH2B3","SMARCA4","SOCS1","SPOP","STAT4","TBX3","TNKS","TP53BP1","TYRO3","WT1","ZNF217","AKT1","AMER1","ARFRP1","ATM","AXIN1","BCL2","BCOR","BRCA1","BTK","CBL","CD274","CDH2","CDK6","CDKN2B","CHEK1","CREBBP","CTNNA1","CYLD","DICER1","EP300","EPHB1","ERBB4","EZH2","FANCD2","FANCL","FBXW7","FGF23","FGFR1","FLCN","FOXP1","GATA1","GEN1","GNAQ","GRM3","HLA-B","HSD3B1","IGF1R","IL7R","IRF4","JUN","KDR","KMT2A","LMO1","MAGI2","MAP3K13","MEF2B","MKNK1","MSH2","MYC","NCOR1","NKX2-1","NPM1","NTRK3","PALB2","PARP4","PDGFRB","PIK3C3","PIK3R2","POLE","PRKAR1A","PTCH1","QKI","RANBP2","RET","RPTOR","SDHC","SLIT2","SMARCB1","SOX10","SPTA1","STK11","TEK","TET2","TNKS2","TRRAP","U2AF1","XPO1","ZNF703","AKT2","ARID1A","ATR","AXL","BCL2A1","BCORL1","BRCA2","C11orf30","CCND1","CD79A","CDH20","CDK8","CDKN2C","CHEK2","CRKL","CTNNB1","CYP17A1","DIS3","EPHA3","EPHB4","ERCC4","FAM175A","FANCE","FANCM","FGF10","FGF3","FGFR2","FLT1","FRS2","GATA2","GID4","GNAS","GSK3B","HLA-C","HSP90AA1","IGF2","INHBA","IRS2","KAT6A","KEAP1","LRP1B","MAP2K1","MCL1","MEN1","MKNK2","MSH6","MYCL","NF1","NOTCH1","NRAS","NUDT1","PARK2","PAX5","PDK1","PIK3CA","PLCG2","PPARG","PRKCI","PTCH2","RAC1","RAD51C","RARA","RICTOR","RUNX1","SDHD","SMAD2","SMARCD1","SOX2","SRC","SUFU","TERC","TGFBR2","TOP1","TSC1","VEGFA","XRCC2","ZNRF3","TNF","APC","KMT2C","LRP6","RAD51D","TIPARP"]
    
    T7_315_18=["ABL1","ARAF","AURKB","BCORL1","CARD11","CDC73","CDKN2C","CSF1R","DOT1L","ERG","FANCG","FGF4","FLT4","GATA6","GSK3B","IGF2","JAK2","KIT","MAGI2","MEN1","MYC","NOTCH2","PALB2","PIK3CB","PREX2","RAD50","ROS1","SLIT2","SOX2","SUFU","TOP1","WT1","ALK","ETV5","NTRK1","ABL2","ARFRP1","AXIN1","BLM","CBFB","CDH1","CEBPA","CTCF","EGFR","ERRFI1","FANCL","FGF6","FOXL2","GID4","H3F3A","IKBKE","JAK3","KLHL6","MAP2K1","MET","MYCL","NOTCH3","PARK2","PIK3CG","PRKAR1A","RAD51","RPTOR","SMAD2","SOX9","SYK","TOP2A","XPO1","BCL2","ETV6","NTRK2","ACVR1B","ARID1A","AXL","BRAF","CBL","CDK12","CHD2","CTNNA1","EP300","ESR1","FAS","FGFR1","FOXP1","HGF","IKZF1","JUN","KMT2A","MAP2K2","MITF","NPM1","PAX5","PIK3R1","PRKCI","RAF1","RUNX1","SMAD3","SPEN","TAF1","TET2","TP53","ZBTB2","BCR","PDGFRA","AKT1","ARID1B","BAP1","BRCA1","CCND1","CDK4","CHD4","CTNNB1","EPHA3","EZH2","FAT1","FGFR2","FRS2","GLI1","HNF1A","IL7R","KAT6A","MAP2K4","MLH1","MYCN","NRAS","PBRM1","PIK3R2","PRKDC","RANBP2","RUNX1T1","SMAD4","SPOP","TBX3","TGFBR2","TSC1","ZNF217","AKT2","ARID2","BARD1","BRCA2","CCND2","CDK6","CHEK1","CUL3","EPHA5","FAM46C","FBXW7","FGFR3","FUBP1","GNA11","HRAS","INHBA","KMT2C","MAP3K1","MPL","MYD88","NSD1","PDCD1LG2","PLCG2","PRSS8","RARA","SDHA","SMARCA4","SPTA1","TERC","TNFAIP3","TSC2","ZNF703","AKT3","ASXL1","BRD4","CCND3","CDK8","CHEK2","CYLD","EPHA7","FANCA","FGF10","FGFR4","GABRA6","GNA13","HSD3B1","INPP4B","KDM5A","MCL1","MRE11A","NF1","PMS2","PTCH1","RB1","SDHB","SMARCB1","SRC","TERT","TNFRSF14","TSHR","RET","ATM","BCL2L1","BRIP1","CCNE1","CDKN1A","CIC","DAXX","EPHB1","FANCC","FGF14","FH","GATA1","GNAQ","HSP90AA1","IRF2","KDM5C","KMT2D","MDM2","MSH2","NF2","PDGFRB","POLD1","PTEN","RBM10","SDHC","SMO","STAG2","U2AF1","AMER1","ATR","BCL2L2","BTG1","CD274","CDKN1B","CREBBP","DDR2","ERBB2","FANCD2","FGF19","FLCN","GATA2","GNAS","IDH1","IRF4","KDM6A","MDM4","MSH6","NFE2L2","NTRK3","PDK1","POLE","PTPN11","SDHD","SNCAIP","STAT3","VEGFA","MYB","TMPRSS2","ATRX","BCL6","BTK","CD79A","CDKN2A","CRKL","DICER1","ERBB3","FANCE","FGF23","FLT1","GATA3","GPR124","IDH2","IRS2","KDR","KRAS","MED12","MTOR","NFKBIA","NUP93","PIK3C2B","PPP2R1A","QKI","RICTOR","SETD2","SOCS1","STAT4","VHL","ETV1","APC","AURKA","BCOR","C11orf30","CD79B","CDKN2B","CRLF2","DNMT3A","ERBB4","FANCF","FGF3","FLT3","GATA4","GRIN2A","IGF1R","JAK1","KEAP1","LMO1","MEF2B","MUTYH","NKX2-1","PAK3","PIK3CA","PRDM1","RAC1","RNF43","SF3B1","SOX10","STK11","WISP3","ETV4","AR","GRM3","KEL","LRP1B","NOTCH1","LYN","LZTR1"]
    
    numberOfPDF=0
    df = pd.DataFrame(data=None, columns=foundation_one, dtype=None, copy=False)

    # foundation_one = ['File','FMI_Test', 'Date', 'Test_Type', 'Sample_type', 'Site', 'Collection_Date', 'Received_Date', 'Visit_Type', 'Partner_Name', 'FMI_Study_ID', 'Date_of_Birth', 'Diagnosis','ABL1','ACVR1B','AKT1','AKT2','AKT3','ALK','ALOX12B','AMER1','APC','AR','ARAF','ARFRP1','ARID1A','ASXL1','ATM','ATR','ATRX','AURKA','AURKB','AXIN1','AXL','BAP1','BARD1','BCL2','BCL2L1','BCL2L2','BCL6','BCOR','BCORL1','BRAF','BRCA1','BRCA2','BRD4','BRIP1','BTG1','BTG2','BTK','C11orf30','CALR','CARD11','CASP8','CBFB','CBL','CCND1','CCND2','CCND3','CCNE1','CD22','CD274','CD70','CD79A','CD79B','CDC73','CDH1','CDK12','CDK4','CDK6','CDK8','CDKN1A','CDKN1B','CDKN2A','CDKN2B','CDKN2C','CEBPA','CHEK1','CHEK2','CIC','CREBBP','CRKL','CSF1R','CSF3R','CTCF','CTNNA1','CTNNB1','CUL3','CUL4A','CXCR4','CYP17A1','DAXX','DDR1','DDR2','DIS3','DNMT3A','DOT1L','EED','EGFR','EP300','EPHA3','EPHB1','EPHB4','ERBB2','ERBB3','ERBB4','ERCC4','ERG','ERRFI1','ESR1','EZH2','FAM46C','FANCA','FANCC','FANCG','FANCL','FAS','FBXW7','FGF10','FGF12','FGF14','FGF19','FGF23','FGF3','FGF4','FGF6','FGFR1','FGFR2','FGFR3','FGFR4','FH','FLCN','FLT1','FLT3','FOXL2','FUBP1','GABRA6','GATA3','GATA4','GATA6','GID4','GNA11','GNA13','GNAQ','GNAS','GRM3','GSK3B','H3F3A','HDAC1','HGF','HNF1A','HRAS','HSD3B1','ID3','IDH1','IDH2','IGF1R','IKBKE','IKZF1','INPP4B','IRF2','IRF4','IRS2','JAK1','JAK2','JAK3','JUN','KDM5A','KDM5C','KDM6A','KDR','KEAP1','KEL','KIT','KLHL6','KMT2A','KMT2D','KRAS','LTK','LYN','MAF','MAP2K1','MAP2K2','MAP2K4','MAP3K1','MAP3K13','MAPK1','MCL1','MDM2','MDM4','MED12','MEF2B','MEN1','MERTK','MET','MITF','MKNK1','MLH1','MPL','MRE11A','MSH2','MSH3','MSH6','MST1R','MTAP','MTOR','MUTYH','MYC','MYCL','MYCN','MYD88','NBN','NF1','NF2','NFE2L2','NFKBIA','NKX2-1','NOTCH1','NOTCH2','NOTCH3','NPM1','NRAS','NT5C2','NTRK1','NTRK2','NTRK3','P2RY8','PALB2','PARK2','PARP1','PARP2','PARP3','PAX5','PBRM1','PDCD1','PDCD1LG2','PDGFRA','PDGFRB','PDK1','PIK3C2B','PIK3C2G','PIK3CA','PIK3CB','PIK3R1','PIM1','PMS2','POLD1','POLE','PPARG','PPP2R1A','PPP2R2A','PRDM1','PRKAR1A','PRKCI','PTCH1','PTEN','PTPN11','PTPRO','QKI','RAC1','RAD21','RAD51','RAD51B','RAD51C','RAD51D','RAD52','RAD54L','RAF1','RARA','RB1','RBM10','REL','RET','RICTOR','RNF43','ROS1','RPTOR','SDHA','SDHB','SDHC','SDHD','SETD2','SF3B1','SGK1','SMAD2','SMAD4','SMARCA4','SMARCB1','SMO','SNCAIP','SOCS1','SOX2','SOX9','SPEN','SPOP','SRC','STAG2','STAT3','STK11','SUFU','SYK','TBX3','TEK','TET2','TGFBR2','TIPARP','TNFAIP3','TNFRSF14','TP53','TSC1','TSC2','TYRO3','U2AF1','VEGFA','VHL','WHSC1','WHSC1L1','WT1','XPO1','XRCC2','ZNF217','ZNF703','ALK','BCL2','BCR','BRAF','BRCA1','BRCA2','CD74','EGFR','ETV4','ETV5','ETV6','EWSR1','EZR','FGFR1','FGFR2','FGFR3','KIT','KMT2A','MSH2','MYB','MYC','NOTCH2','NTRK1','NTRK2','NUTM1','PDGFRA','RAF1','RARA','RET','ROS1','RSPO2','SDC4','SLC34A2','TERC','TERT','TMPRSS2','Loss of Heterozygosity score','Tumor Mutational Burden Score','Tumor Mutational Burden','Microsatellite (MS) status','Microsatellite Instability Status','Microsatellite Instability']
    
    # We check what type of file we have. 
    for d in dicts_fundation_one:
        #print(d) 
        if d is None:
            print("El archivo: "+pdfs[numberOfPDF]+" no cumple el formato")
            numberOfPDF+=1

            pass
        else:
            numberOfPDF+=1
            if d['TypeOftest']=='CTA_SOLID':
                for key in CTA_SOLID:
                    if key not in d:
                        d[key]=0
            elif d['TypeOftest']=='DX1':
                for key in DX1:
                    if key not in d:
                        d[key]=0
            elif d['TypeOftest']=='CF3':
                for key in CF3:
                    if key not in d:
                        d[key]=0
            elif d['TypeOftest']=='CTA_LIQUID_AB1':
                for key in CTA_Liquid_AB1:
                    if key not in d:
                        d[key]=0
            elif d['TypeOftest']=='CTA_Liquid':
                for key in CTA_Liquid:
                    if key not in d:
                        d[key]=0
            elif d['TypeOftest']=='T7_395':
                for key in T7_395:
                    if key not in d:
                        d[key]=0
            elif d['TypeOftest']=='T7_315_28':
                for key in T7_315_18:
                    if key not in d:
                        d[key]=0

            elif d['TypeOftest'] is None:
                print('No info about it')
            
            #Add No value in Sample Failure: 
            if 'Sample Failure' not in d:
                d['Sample Failure']='No'
            
            #Add yes to study related. 
            if 'Study Related' not in d:
                d['Study Related']='Yes'
                
            #Combine Microsatellity status:         
            if 'Microsatellite (MS) status' in d:
                d['Microsatellite Instability'] = d.pop('Microsatellite (MS) status')
                
            elif 'Microsatellite Instability Status' in d:
                d['Microsatellite Instability'] = d.pop('Microsatellite Instability Status')
                
            #Change all the none or none detected by 0. 
            for key in d.keys():
                if d[key]=='None' or d[key]=='None Detected' or d[key]=='Not Evaluable' or d[key]=='Not Found':
                    d[key]=0
            
            
            #Change Genes with * without *
            if 'BCR*' in d:
                d['BCR'] = d.pop('BCR*')
            elif 'CD74*' in d:
                d['CD74'] = d.pop('CD74*')
            elif 'MYB*' in d:
                d['MYB'] = d.pop('MYB*')
            elif 'NUTM1*' in d:
                d['NUTM1'] = d.pop('NUTM1*')
            elif 'RSPO2*' in d:	
                d['RSPO2'] = d.pop('RSPO2*')           
            elif 'TERC*' in d:	
                d['TERC'] = d.pop('TERC*')
            elif 'TERT*' in d:
                d['TERT'] = d.pop('TERT*')
            elif 'TMPRSS2*' in d:
                d['TMPRSS2'] = d.pop('TMPRSS2*')
                
                
                
            # addd not analyzed to dicctionaries that doesn't have.
            for i in foundation_one[15::]:
                if i not in d:
                    d[i]='--'

            #Testing Sample Failure:
            if d['Sample Failure']=='Yes':
                for i in foundation_one[16::]:
                    d[i]="-"   
            
            df = df.append(d, ignore_index=True)
    #Eliminamos las columnas que no nos interesan. 
    try:
        if 'Partner_Study' in df.columns:
            df.drop(['Partner_Study'], axis = 1, inplace=True) 
            # del df['Partner_Study, Site_ID,	Specimen_ID,Subjet']
            # df.drop(['column_nameA', 'column_nameB'], axis=1, inplace=True)
    
        if 'Subjet' in df.columns:
            df.drop(['Subjet'], axis = 1, inplace=True) 

        if 'Site_ID' in df.columns:
            df.drop(['Site_ID'], axis = 1, inplace=True) 

        if 'Specimen_ID' in df.columns:
            df.drop(['Specimen_ID'], axis = 1, inplace=True) 

        if 'Partner Study ID' in df.columns:
            df.drop(['Partner Study ID'], axis = 1, inplace=True)        

    except:
        print("Error removing columns")


        
    
    
    
    print(df)
    df.to_excel (r'Foundation_One_dataframe.xlsx', index = True, header=True)
    print(os.getcwd)

