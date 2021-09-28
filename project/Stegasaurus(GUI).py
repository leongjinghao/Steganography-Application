from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import shutil
import os
import ctypes
import glob
from PIL import Image

class GUI:
    background = 'lightgrey'
    test = 'white'
    items = []
    def __init__(self):

        mainGUI = Tk(className='Steganography program')  # Sets window name
        mainGUI.geometry("1100x700+100+50")  # Sets window size
        mainGUI.configure(bg=self.background) #Sets GUI background color
        mainGUI.resizable(width=True, height=True) #Disallows user from resizing the window.
        self.viewPage(mainGUI)
        mainGUI.mainloop()  # Starts up4 and runs the GUI until user exits

    def mainMenu(self, mainGUI):
        mainMenuFrame = Frame(mainGUI, bg=self.background)
        mainMenuFrame.place(relx=0, rely=0, relheight=0.9, relwidth=1)


        # title = Label(mainMenuFrame, text="", bg = self.background)
        # title.config(font=("MS Sans Serif", 40))
        # title.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)

        #Upload Radio button
        uploadValue = StringVar(mainMenuFrame, "1")
        Radiobutton(mainMenuFrame, text='Payload', variable=uploadValue, value='1', background=self.background).place(relx=0.5, rely=0.2, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='Cover', variable=uploadValue, value='2', background=self.background).place(relx=0.6, rely=0.2, relheight=0.05, relwidth=0.1)



        #Delete Radio button
        deleteValue = StringVar(mainMenuFrame, "1")
        Radiobutton(mainMenuFrame, text='Payload', variable=deleteValue, value='1', background=self.background).place(relx=0.5, rely=0.35, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='Cover', variable=deleteValue, value='2', background=self.background).place(relx=0.6, rely=0.35, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='All', variable=deleteValue, value='3', background=self.background).place(relx=0.7, rely=0.35, relheight=0.05, relwidth=0.1)



        #View button
        viewButton = Button(mainMenuFrame, text="View", command=lambda: [mainMenuFrame.place_forget(), self.viewPage(mainGUI)])
        viewButton.config(font=("Arial", 15))
        viewButton.place(relx=0.35, rely=0.5, relheight=0.05, relwidth=0.1)



        #-----------------------Stats interface-------------------------

    def uploadPage(self, mainGUI):
        uploadFrame = Frame(mainGUI, bg=self.background)
        uploadFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        #Payload button
        payloadButton = Button(uploadFrame, text="Payload", command=lambda: [uploadFrame.place_forget(), self.uploadFile(1), self.viewPage(mainGUI)])
        payloadButton.config(font=("Arial", 25))
        payloadButton.place(relx=0.45, rely=0.35, relheight=0.08, relwidth=0.15)

        #Cover button
        coverButton = Button(uploadFrame, text="Cover", command=lambda: [uploadFrame.place_forget(), self.uploadFile(2), self.viewPage(mainGUI)])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.55, relheight=0.08, relwidth=0.15)

        #Back button
        coverButton = Button(uploadFrame, text="Back", command=lambda: [uploadFrame.place_forget(), self.viewPage(mainGUI)])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.75, relheight=0.08, relwidth=0.15)

    def uploadFile(self, uploadValue):
        filelocation = askopenfilename()
        print(filelocation)
        print(uploadValue)
        if uploadValue == "1":
            destination = "./payload"
        else:
            destination = "./cover"
        source = filelocation

        try:
            shutil.copy2(source, destination,  follow_symlinks=True)
            print("File copied successfully.")

            # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

            # If destination is a directory.
        except IsADirectoryError:
            print("Destination is a directory.")

            # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

            # For other errors
        except:
            print("Error occurred while copying file.")

    def deleteFile(self, deleteValue):
        print(deleteValue)
        if deleteValue == "3":
            dir = './cover'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            dir = './payload'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
            print("All files deleted")



    def viewPage(self, mainGUI):
        viewFrame = Frame(mainGUI, bg=self.background)
        viewFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(viewFrame,
                                  text="Payload files",
                                  bg=self.background)


        title.config(font=("MS Sans Serif", 30))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(viewFrame,
                                  text="Cover files",
                                  bg=self.background)


        title.config(font=("MS Sans Serif", 30))
        title.place(relx=0.35, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(viewFrame,
                                  text="Result files",
                                  bg=self.background)


        title.config(font=("MS Sans Serif", 30))
        title.place(relx=0.7, rely=0, relheight=0.1, relwidth=0.25)



        item_column = ('File Name','File Type')
        payloadList = ttk.Treeview(viewFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            payloadList.heading(item_column[i], text=item_column[i])

        payloadList.column(item_column[0], anchor="w")
        payloadList.column(item_column[1], anchor="n", width=10)
        payloadList.place(relx=0,rely=0.1, relheight=0.5, relwidth=0.3333)

        #item_column = ('File Name','File Type')
        coverList = ttk.Treeview(viewFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            coverList.heading(item_column[i], text=item_column[i])

        coverList.column(item_column[0], anchor="w")
        coverList.column(item_column[1], anchor="n", width=10)
        coverList.place(relx=0.33333,rely=0.1, relheight=0.5, relwidth=0.3333)


        resultList = ttk.Treeview(viewFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            resultList.heading(item_column[i], text=item_column[i])

        if len(payloadList.selection()) > 0:
            payloadList.selection_remove(payloadList.selection()[0])

        resultList.column(item_column[0], anchor="w")
        resultList.column(item_column[1], anchor="n", width=10)
        resultList.place(relx=0.66666,rely=0.1, relheight=0.5, relwidth=0.3333)

        payloadFiles = os.listdir('./payload')

        coverFiles = os.listdir('./cover')

        for f in range(len(payloadFiles)):
            payloadFiles[f] = payloadFiles[f].split('.')
        for f in range(len(coverFiles)):
            coverFiles[f] = coverFiles[f].split('.')


        for i, column in enumerate(payloadFiles, start=0):
            payloadList.insert("", 0, values=(payloadFiles[i]))

        for i, column in enumerate(coverFiles, start=0):
            coverList.insert("", 0, values=(coverFiles[i]))




        viewPayloadHexButton = Button(viewFrame, text="View payload data", command=lambda: [self.retrieveBinaries(payloadList.item(payloadList.selection())['values'], "payload")])
        viewPayloadHexButton.config(font=("Arial", 11))
        viewPayloadHexButton.place(relx=0.05, rely=0.65, relheight=0.05, relwidth=0.15)

        #Hide button
        hideButton = Button(viewFrame, text="Hide payload",  command=lambda: [])
        hideButton.config(font=("Arial", 15))
        hideButton.place(relx=0.8, rely=0.85, relheight=0.05, relwidth=0.15)

        #Extract button
        extractButton = Button(viewFrame, text="Extract payload") #command=lambda: [self.crawlerPage(mainGUI), mainMenuFrame.place_forget()])
        extractButton.config(font=("Arial", 15))
        extractButton.place(relx=0.8, rely=0.9, relheight=0.05, relwidth=0.15)

        viewPayloadHexButton = Button(viewFrame, text="Clear Selection", command=lambda: [self.clearSelection(payloadList,coverList,resultList)])
        viewPayloadHexButton.config(font=("Arial", 11))
        viewPayloadHexButton.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.15)

        #Upload button
        uploadButton = Button(viewFrame, text="Upload", command=lambda: [viewFrame.place_forget(),self.uploadPage(mainGUI)])
        uploadButton.config(font=("Arial", 15))
        uploadButton.place(relx=0.05, rely=0.9, relheight=0.05, relwidth=0.2)

        #Delete button
        uploadButton = Button(viewFrame, text="Delete", command=lambda: [])
        uploadButton.config(font=("Arial", 15))
        uploadButton.place(relx=0.35, rely=0.9, relheight=0.05, relwidth=0.2)

    def clearSelection(self,payloadList, coverList, resultList):
        for item in payloadList.selection():
            payloadList.selection_remove(item)
        for item in coverList.selection():
            coverList.selection_remove(item)
        for item in resultList.selection():
            resultList.selection_remove(item)

    def retrieveBinaries(self, fileSelection, payloadOrCover):

        x = 0
        y = 0
        file = Image.open('./payload/' + '.'.join(fileSelection))
        file = file.convert('RGB')
        pixels = list(file.getdata())
        print(pixels)
        print(pixels)










class Steganography:
    def __init__(self):
        x=1

if __name__ == '__main__':
    main_GUI = GUI() #Instantiates a multiScraperGUI object.

