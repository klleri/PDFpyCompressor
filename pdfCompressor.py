# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 17:08:58 2021

@author: Lucas
"""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from PDFNetPython3 import *
import os
import sys
import getpass
import tkinter.ttk as ttk



window = Tk()
window.title("PUC Minas - Poços de Caldas")
window.geometry('1000x500')
window.config(bg = '#0497e5')


###                         defs                    ### 

def fileLabelCliked():
    
    global aux
    global file_name_without_extension
    global arquivoAntigo
    
    filename = askopenfilename(filetypes=[('pdf file', '*.pdf')])
    aux = filename

    file_path = filename
    arquivoAntigo = os.path.getsize(filename)
    
    file_name = os.path.basename(file_path)
    index_of_dot = file_name.index('.')
    file_name_without_extension = file_name[:index_of_dot]
    filename = file_name_without_extension
    
    fileName1.insert(0, file_name_without_extension )
    newName.insert(0, "{}_opt".format(file_name_without_extension))
    
    return()
    
def savedFile():
    
    save = askdirectory()
    saveName.insert(0, save)

def convert():
    
    
    if not fileName1.get():
        messagebox.showinfo('Aviso', 'Escolha o arquivo para ser convertido')
        
    elif not saveName.get():
        messagebox.showinfo('Aviso', 'Escolha o caminho que ficará salvo o arquivo')
    
    elif not newName.get():
        messagebox.showinfo('Aviso', 'Escolha o nome do novo arquivo')
    
    elif not selectConvert.get():
        messagebox.showinfo('Aviso', 'Escolha o tipo de conversão')
        
    elif selectConvert.get() == "Nomal Compress":
        input_path = aux
        output_path = saveName.get()
        input_filename = file_name_without_extension
        
        doc = PDFDoc(input_path)
        doc.InitSecurityHandler()
        Optimizer.Optimize(doc)
    
        doc.Save(output_path+ "//" + newName.get() + ".pdf", SDFDoc.e_linearized)
        doc.Close()
        arquivoNovo = os.path.getsize(output_path + "//" + newName.get() + ".pdf")
    
        arquivoAntigo1 = arquivoAntigo/(1024*1024)
        arquivoNovo = arquivoNovo/(1024*1024)
    
        messagebox.showinfo('Fim', 'Comprimido com sucesso \n ----------------------------\n Arquivo Original : {:0.2f}MB  \n Arquivo Otimizado: {:0.2f}MB'.format(arquivoAntigo1, arquivoNovo))
        
    
    else:
        input_path = aux
        output_path = saveName.get()
        input_filename = file_name_without_extension
        
        doc = PDFDoc(input_path)
        doc.InitSecurityHandler()
        image_settings = ImageSettings()
        
        # low quality jpeg compression
        image_settings.SetCompressionMode(ImageSettings.e_jpeg)
        image_settings.SetQuality(1)
        
        # Set the output dpi to be standard screen resolution
        image_settings.SetImageDPI(144,96)
        
        # this option will recompress images not compressed with
        # jpeg compression and use the result if the new image
        # is smaller.
        image_settings.ForceRecompression(True)
        
        # this option is not commonly used since it can 
        # potentially lead to larger files.  It should be enabled
        # only if the output compression specified should be applied
        # to every image of a given type regardless of the output image size
        #image_settings.ForceChanges(True)
        
        opt_settings = OptimizerSettings()
        opt_settings.SetColorImageSettings(image_settings)
        opt_settings.SetGrayscaleImageSettings(image_settings)
        
        # use the same settings for both color and grayscale images
        Optimizer.Optimize(doc, opt_settings)
        
        doc.Save(output_path+ "//" + newName.get() + ".pdf", SDFDoc.e_linearized)
        print(output_path + newName.get() + ".pdf")
        doc.Close()
        
        arquivoNovo = os.path.getsize(output_path + "//" + newName.get() + ".pdf")
    
        arquivoAntigo1 = arquivoAntigo/(1024*1024)
        arquivoNovo = arquivoNovo/(1024*1024)
    
        messagebox.showinfo('Fim', 'Comprimido com sucesso \n ----------------------------\n Arquivo Original : {:0.2f}MB  \n Arquivo Otimizado: {:0.2f}MB'.format(arquivoAntigo1, arquivoNovo))
    



###-------------------------------------------------### 



###                     File  Label                 ###      
fileLabel = Label(window, text="Arquivo: ", bg = "#0497e5")
fileLabel.place(relx=0.5, rely=0.2, anchor=CENTER)

fileName1 = Entry( window, width= 43, font=( "Calibri", 14))
fileName1.place(relx=0.65, rely=0.25, anchor=CENTER)

fileButton = Button(window, text="Selecionar", command=fileLabelCliked)
fileButton.place(relx=0.91, rely=0.25, anchor=CENTER)
###-------------------------------------------------###   

###             Where file gonna be saved           ###      
saveLabel = Label(window, text="Onde ficará salvo: ", bg = "#0497e5")
saveLabel.place(relx=0.52, rely=0.3, anchor=CENTER)

saveName = Entry(window, width= 43, font=( "Calibri", 14))
saveName.place(relx=0.65, rely=0.35, anchor=CENTER)

saveButton = Button(window, text="Selecionar", command=savedFile)
saveButton.place(relx=0.91, rely=0.35, anchor=CENTER)
###-------------------------------------------------###      

###                 new file name Label             ###      
newLabel = Label(window, text="Nome do novo arquivo: ", bg = "#0497e5")
newLabel.place(relx=0.54, rely=0.4, anchor=CENTER)

newName = Entry(window, width= 43, font=( "Calibri", 14))
newName.place(relx=0.65, rely=0.45, anchor=CENTER)

###-------------------------------------------------### 

###                    combobox                     ###

selectConvert = ttk.Combobox(window, width = 50, state='readonly') 
selectConvert.place(relx=0.65, rely=0.55, anchor=CENTER)

  
selectConvert['values'] = ('Nomal Compress',  
                          'Super Compress',) 
###-------------------------------------------------### 

###                  convert button                 ###
      
convertButton = Button(window,text='Converter', command=convert)
convertButton.config(height = 5, width = 15)
convertButton.place(relx=0.65, rely=0.70, anchor=CENTER)


###-------------------------------------------------###    


window.mainloop()