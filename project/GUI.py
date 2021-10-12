from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import shutil
import os
import ctypes
import glob
from PIL import Image, ImageTk, ImageOps
import cv2, numpy as np
from steganography import Steganography
import pymsgbox  # pip install PyMsgBox
from PIL import Image


class GUI:
    background = 'lightgrey'
    testbg = 'red'
    test = 'white'
    items = []
    message = ""
    typeFlag = ""
    selectedPayload = ""
    selectedCover = ""
    errorFlag = 0
    allowedImg = ['png', "PNG", "jpg", "gif", "jpeg", "bmp"]


    def __init__(self):

        mainGUI = Tk(className='Steganography program')  # Sets window name
        mainGUI.geometry("1100x700+100+50")  # Sets window size
        mainGUI.configure(bg=self.background)  # Sets GUI background color
        mainGUI.resizable(width=True, height=True)  # Disallows user from resizing the window.
        self.viewPage(mainGUI)
        mainGUI.mainloop()  # Starts up4 and runs the GUI until user exits

    def viewPage(self, mainGUI):
        viewFrame = Frame(mainGUI, bg=self.background)
        viewFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(viewFrame,
                      text="Payload files",
                      bg=self.background)

        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(viewFrame,
                      text="Cover files",
                      bg=self.background)

        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0.25, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(viewFrame,
                      text="Stego files",
                      bg=self.background)

        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0.5, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(viewFrame,
                      text="Extracted files",
                      bg=self.background)

        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0.75, rely=0, relheight=0.1, relwidth=0.25)



        item_column = ('File Name', 'File Type')
        payloadList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            payloadList.heading(item_column[i], text=item_column[i])

        payloadList.column(item_column[0], anchor="w")
        payloadList.column(item_column[1], anchor="n", width=10)
        payloadList.place(relx=0, rely=0.1, relheight=0.5, relwidth=0.25)


        coverList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            coverList.heading(item_column[i], text=item_column[i])

        coverList.column(item_column[0], anchor="w")
        coverList.column(item_column[1], anchor="n", width=10)
        coverList.place(relx=0.25, rely=0.1, relheight=0.5, relwidth=0.25)

        resultList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            resultList.heading(item_column[i], text=item_column[i])

        resultList.column(item_column[0], anchor="w")
        resultList.column(item_column[1], anchor="n", width=10)
        resultList.place(relx=0.5, rely=0.1, relheight=0.5, relwidth=0.25)

        extractList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            extractList.heading(item_column[i], text=item_column[i])

        extractList.column(item_column[0], anchor="w")
        extractList.column(item_column[1], anchor="n", width=10)
        extractList.place(relx=0.75, rely=0.1, relheight=0.5, relwidth=0.25)



        payloadFiles = os.listdir('./payload')

        coverFiles = os.listdir('./cover')

        resultFiles = os.listdir('./result')

        extractFiles = os.listdir('./extracted')

        for f in range(len(payloadFiles)):
            payloadFiles[f] = payloadFiles[f].split('.')
        for i, column in enumerate(payloadFiles, start=0):
            payloadList.insert("", 0, values=(payloadFiles[i]))

        for f in range(len(coverFiles)):
            coverFiles[f] = coverFiles[f].split('.')
        for i, column in enumerate(coverFiles, start=0):
            coverList.insert("", 0, values=(coverFiles[i]))

        for f in range(len(resultFiles)):
            resultFiles[f] = resultFiles[f].split('.')
        for i, column in enumerate(resultFiles, start=0):
            resultList.insert("", 0, values=(resultFiles[i]))

        for f in range(len(extractFiles)):
            extractFiles[f] = extractFiles[f].split('.')
        for i, column in enumerate(extractFiles, start=0):
            extractList.insert("", 0, values=(extractFiles[i]))

        payloadList.bind("<Double-1>", lambda event: self.DoubleClick(event, payloadList, 1))
        coverList.bind("<Double-1>", lambda event: self.DoubleClick(event, coverList, 2))
        resultList.bind("<Double-1>", lambda event: self.DoubleClick(event, resultList, 3))
        extractList.bind("<Double-1>", lambda event: self.DoubleClick(event, extractList, 4))

        # Hide button
        hideButton = Button(viewFrame, text="Hide payload",
                            command=lambda: [viewFrame.place_forget(), self.coverSelectionPage(mainGUI)])
        hideButton.config(font=("Arial", 15))
        hideButton.place(relx=0.6, rely=0.9, relheight=0.05, relwidth=0.15)

        # Extract button
        extractButton = Button(viewFrame,
                               text="Extract payload", command=lambda: [viewFrame.place_forget(), self.resultSelectionPage(mainGUI)])
        extractButton.config(font=("Arial", 15))
        extractButton.place(relx=0.8, rely=0.9, relheight=0.05, relwidth=0.15)

        # Upload button
        uploadButton = Button(viewFrame, text="Upload",
                              command=lambda: [viewFrame.place_forget(), self.uploadPage(mainGUI)])
        uploadButton.config(font=("Arial", 15))
        uploadButton.place(relx=0.05, rely=0.9, relheight=0.05, relwidth=0.2)

        # Delete button
        uploadButton = Button(viewFrame, text="Delete",
                              command=lambda: [viewFrame.place_forget(), self.deletePage(mainGUI)])
        uploadButton.config(font=("Arial", 15))
        uploadButton.place(relx=0.35, rely=0.9, relheight=0.05, relwidth=0.2)

    "Double click function"
    def DoubleClick(self, event, tree, type):
        try:
            if type == 1:
                image = Image.open('payload/'+'.'.join(tree.item(tree.selection())['values']))
                image.show()
            elif type == 2:
                image = Image.open('cover/'+'.'.join(tree.item(tree.selection())['values']))
                image.show()
            elif type == 3:
                image = Image.open(str('result/'+'.'.join(tree.item(tree.selection())['values'])))
                image.show()
            elif type == 4:
                image = Image.open('extracted/'+'.'.join(tree.item(tree.selection())['values']))
                image.show()
        except:
            print("Images can only be seen")
        #print(item)



    def uploadPage(self, mainGUI):
        uploadFrame = Frame(mainGUI, bg=self.background)
        uploadFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(uploadFrame, text="What would you like to upload?", bg=self.background)
        title.config(font=("Arial", 40))
        title.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)

        # Payload button
        payloadButton = Button(uploadFrame, text="Payload",
                               command=lambda: [uploadFrame.place_forget(), self.uploadFile("1"),
                                                self.viewPage(mainGUI)])
        payloadButton.config(font=("Arial", 25))
        payloadButton.place(relx=0.45, rely=0.35, relheight=0.08, relwidth=0.15)

        # Cover button
        coverButton = Button(uploadFrame, text="Cover",
                             command=lambda: [uploadFrame.place_forget(), self.uploadFile("2"), self.viewPage(mainGUI)])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.55, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(uploadFrame, text="Back",
                            command=lambda: [uploadFrame.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.75, relheight=0.08, relwidth=0.15)

    def deletePage(self, mainGUI):
        deleteFrame = Frame(mainGUI, bg=self.background)
        deleteFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(deleteFrame, text="What would you like to delete?", bg=self.background)
        title.config(font=("Arial", 40))
        title.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)

        # Payload button
        payloadButton = Button(deleteFrame, text="Payload", command=lambda: [deleteFrame.place_forget(), self.deleteSinglePage(mainGUI,1)])
        payloadButton.config(font=("Arial", 25))
        payloadButton.place(relx=0.45, rely=0.25, relheight=0.07, relwidth=0.15)

        # Cover button
        coverButton = Button(deleteFrame, text="Cover", command=lambda: [deleteFrame.place_forget(), self.deleteSinglePage(mainGUI,2)])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.35, relheight=0.07, relwidth=0.15)

        # Result button
        coverButton = Button(deleteFrame, text="Stego", command=lambda: [deleteFrame.place_forget(), self.deleteSinglePage(mainGUI,3)])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.45, relheight=0.07, relwidth=0.15)

        # Extracted button
        coverButton = Button(deleteFrame, text="Extracted", command=lambda: [deleteFrame.place_forget(), self.deleteSinglePage(mainGUI,4)])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.55, relheight=0.07, relwidth=0.15)

        # All button
        AllButton = Button(deleteFrame, text="All Files",
                           command=lambda: [deleteFrame.place_forget(), self.deleteFile("3"), self.viewPage(mainGUI)])
        AllButton.config(font=("Arial", 25))
        AllButton.place(relx=0.45, rely=0.65, relheight=0.07, relwidth=0.15)

        # Back button
        backButton = Button(deleteFrame, text="Back",
                            command=lambda: [deleteFrame.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    #delete page for specific storage
    def deleteSinglePage(self, mainGUI, type):
        deleteSelectionFrame = Frame(mainGUI, bg=self.background)
        deleteSelectionFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(deleteSelectionFrame, text="Choose the file to delete.", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0, relheight=0.1, relwidth=0.8)

        item_column = ('File Name', 'File Type')

        deleteList = ttk.Treeview(deleteSelectionFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            deleteList.heading(item_column[i], text=item_column[i])

        deleteList.column(item_column[0], anchor="w")
        deleteList.column(item_column[1], anchor="n", width=10)
        deleteList.place(relx=0, rely=0.1, relheight=0.5, relwidth=1)

        if type == 1:
            listfiles = os.listdir('./payload')
        if type == 2:
            listfiles = os.listdir('./cover')
        if type == 3:
            listfiles = os.listdir('./result')
        if type == 4:
            listfiles = os.listdir('./extracted')

        for f in range(len(listfiles)):
            listfiles[f] = listfiles[f].split('.')

        for i, column in enumerate(listfiles, start=0):
            deleteList.insert("", 0, values=(listfiles[i]))

        # Delete button
        deleteButton = Button(deleteSelectionFrame, text="Delete", command=lambda: [[deleteSelectionFrame.place_forget(),self.removeFile(deleteList.item(deleteList.selection())['values'],type),self.deleteSinglePage(mainGUI,type)] if deleteList.item(deleteList.selection())['values'] != "" else 0])
        deleteButton.config(font=("Arial", 25))
        deleteButton.place(relx=0.45, rely=0.75, relheight=0.07, relwidth=0.15)

        # Back button
        backButton = Button(deleteSelectionFrame, text="Back", command=lambda: [deleteSelectionFrame.place_forget(),self.deletePage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.07, relwidth=0.15)

    def removeFile(self, selection, type):
        try:
            if type == 1:
                storage = "payload/"
            elif type == 2:
                storage = "cover/"
            elif type == 3:
                storage = "result/"
            elif type == 4:
                storage = "extracted/"
            selection = '.'.join(selection)
            os.remove(storage+selection)
        except:
            print("Error deleting")

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
            shutil.copy2(source, destination, follow_symlinks=True)
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
        """Delete files"""
        print(deleteValue)
        if deleteValue == "3":
            dir = './cover'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            dir = './payload'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            dir = './extracted'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            dir = './result'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            print("All files deleted")

    def clearSelection(self, payloadList, coverList, resultList):
        for item in payloadList.selection():
            payloadList.selection_remove(item)
        for item in coverList.selection():
            coverList.selection_remove(item)
        for item in resultList.selection():
            resultList.selection_remove(item)

    def SingleClick(self, event, tree, type, mainGUI):
        if type == 1:
            directory = 'payload/'
        if type == 2:
            directory = 'cover/'
        if type == 3:
            directory = 'result/'

        frame = Frame(mainGUI, bg=self.background)
        frame.place(relx=0.05, rely=0.65, relheight=0.3, relwidth=0.3)
        frame.place_forget()
        frame.place(relx=0.05, rely=0.65, relheight=0.3, relwidth=0.3)
        item = tree.item(tree.selection())['values']
        #check if image
        try:
            if item != "":
                for i in range(len(self.allowedImg)):
                    if item[1] == self.allowedImg[i]:
                        img = Image.open(directory+'.'.join(item))
                        img2 = ImageTk.PhotoImage(img)
                        imagewidth = img2.width()
                        imageheight = img2.height()

                        ratio = imageheight / imagewidth

                        if imageheight > 320:
                            diff = imageheight - 320
                            imageheight = imageheight - diff
                            imagewidth = imageheight / ratio

                        if imagewidth > 320:
                            diff = imagewidth - 320
                            imagewidth = imagewidth - diff
                            imageheight = ratio * imagewidth
                        img = img.resize((int(imagewidth), int(imageheight)))
                        img2 = ImageTk.PhotoImage(img)
                        panel = Label(frame, image=img2)
                        frame.photo = img2
                        panel.pack(side="bottom", expand="yes")
        except:
            pass





    def coverSelectionPage(self, mainGUI):
        coverSelectionFrame = Frame(mainGUI, bg=self.background)
        coverSelectionFrame.place(relx=0, rely=0, relheight=1, relwidth=1)


        title = Label(coverSelectionFrame, text="Choose your cover file", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0, relheight=0.1, relwidth=0.8)

        title = Label(coverSelectionFrame, text="Preview", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.15, rely=0.58, relheight=0.1, relwidth=0.1)

        item_column = ('File Name', 'File Type')

        coverLists = ttk.Treeview(coverSelectionFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            coverLists.heading(item_column[i], text=item_column[i])



        coverLists.column(item_column[0], anchor="w")
        coverLists.column(item_column[1], anchor="n", width=10)


        coverLists.place(relx=0, rely=0.1, relheight=0.5, relwidth=1)


        coverFiles = os.listdir('./cover')

        for f in range(len(coverFiles)):
            coverFiles[f] = coverFiles[f].split('.')

        for i, column in enumerate(coverFiles, start=0):
            coverLists.insert("", 0, values=(coverFiles[i]))

        coverLists.bind("<ButtonRelease-1>", lambda event: self.SingleClick(event, coverLists, 2, mainGUI))

        # Submit button
        submitButton = Button(coverSelectionFrame, text="Submit", command=lambda: [
            [coverSelectionFrame.place_forget(),
             self.payloadSelectionPage(mainGUI, coverLists.item(coverLists.selection())['values'])] if coverLists.item(coverLists.selection())['values'] != "" else [
                self.displayError("file")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.65, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(coverSelectionFrame, text="Back",
                            command=lambda: [coverSelectionFrame.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    def payloadSelectionPage(self, mainGUI, coverSelection):
        payloadSelectionFrame = Frame(mainGUI, bg=self.background)
        payloadSelectionFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.selectedCover = '.'.join(coverSelection)
        print(self.selectedCover)

        title = Label(payloadSelectionFrame, text="Choose your payload file.", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0, relheight=0.1, relwidth=0.8)

        title = Label(payloadSelectionFrame, text="Preview", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.15, rely=0.58, relheight=0.1, relwidth=0.1)

        item_column = ('File Name', 'File Type')

        payloadList = ttk.Treeview(payloadSelectionFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            payloadList.heading(item_column[i], text=item_column[i])

        payloadList.column(item_column[0], anchor="w")
        payloadList.column(item_column[1], anchor="n", width=10)
        payloadList.place(relx=0, rely=0.1, relheight=0.5, relwidth=1)

        payloadFiles = os.listdir('./payload')

        for f in range(len(payloadFiles)):
            payloadFiles[f] = payloadFiles[f].split('.')

        for i, column in enumerate(payloadFiles, start=0):
            payloadList.insert("", 0, values=(payloadFiles[i]))

        payloadList.bind("<ButtonRelease-1>", lambda event: self.SingleClick(event, payloadList, 1, mainGUI))

        # Submit button
        submitButton = Button(payloadSelectionFrame, text="Submit", command=lambda: [
            [payloadSelectionFrame.place_forget(),
             self.nameFilePage(mainGUI, payloadList.item(payloadList.selection())['values'])] if payloadList.item(payloadList.selection())['values'] != "" else [
                self.displayError("file")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.65, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(payloadSelectionFrame, text="Back",
                            command=lambda: [payloadSelectionFrame.place_forget(), self.coverSelectionPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    def resultSelectionPage(self, mainGUI):
        resultSelectionPage = Frame(mainGUI, bg=self.background)
        resultSelectionPage.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(resultSelectionPage, text="Select file to extract data from", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0, relheight=0.1, relwidth=0.8)

        title = Label(resultSelectionPage, text="Preview", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.15, rely=0.58, relheight=0.1, relwidth=0.1)

        item_column = ('File Name', 'File Type')

        resultList = ttk.Treeview(resultSelectionPage, columns=item_column, show='headings')
        for i in range(len(item_column)):
            resultList.heading(item_column[i], text=item_column[i])

        resultList.column(item_column[0], anchor="w")
        resultList.column(item_column[1], anchor="n", width=10)
        resultList.place(relx=0, rely=0.1, relheight=0.5, relwidth=1)

        payloadFiles = os.listdir('./result')

        for f in range(len(payloadFiles)):
            payloadFiles[f] = payloadFiles[f].split('.')

        for i, column in enumerate(payloadFiles, start=0):
            resultList.insert("", 0, values=(payloadFiles[i]))

        #Single bit or multi bit
        uploadValue = StringVar(resultSelectionPage, "1")
        Radiobutton(resultSelectionPage, text='Single-Bit mode', variable=uploadValue, value='1', background=self.background).place(relx=0.7, rely=0.8, relheight=0.05, relwidth=0.1)
        Radiobutton(resultSelectionPage, text='Multi-Bit mode', variable=uploadValue, value='2', background=self.background).place(relx=0.8, rely=0.8, relheight=0.05, relwidth=0.1)

        #txt/img/wav?
        decodeValue = StringVar(resultSelectionPage)
        decodeValue.set("txt")
        dropdown = OptionMenu(resultSelectionPage, decodeValue, "Text file (.txt)", "Document file (.pdf/.doc/.ppt/etc.)", "Images (jpg/png/gif/etc.)", "Audio (wav)",  "Audio (mp3)", "Video (mp4)")
        dropdown.config(font=("Arial", 15))
        dropdown.place(relx=0.65, rely=0.67, relheight=0.05, relwidth=0.3)

        title = Label(resultSelectionPage, text="File type:", bg=self.background)
        title.config(font=("Arial", 15))
        title.place(relx=0.65, rely=0.6, relheight=0.05, relwidth=0.3)

        title = Label(resultSelectionPage, text="Decoding parameters", bg=self.background)
        title.config(font=("Arial", 15))
        title.place(relx=0.65, rely=0.75, relheight=0.05, relwidth=0.3)

        #Item quantity scroller
        itemQuantityScroller = Scale(resultSelectionPage, from_=0, to=7, orient=HORIZONTAL, resolution = 1)
        itemQuantityScroller.place(relx=0.65, rely=0.85, relheight=0.07, relwidth=0.3)

        resultList.bind("<ButtonRelease-1>", lambda event: self.SingleClick(event, resultList, 3, mainGUI))

        # Submit button
        submitButton = Button(resultSelectionPage, text="Submit", command=lambda: [
            [resultSelectionPage.place_forget(), self.extractData(uploadValue.get(), itemQuantityScroller.get(), decodeValue.get(), ".".join(resultList.item(resultList.selection())['values']))
             ,self.viewPage(mainGUI)] if resultList.item(resultList.selection())['values'] != "" else [
                self.displayError("file")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.65, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(resultSelectionPage, text="Back",
                            command=lambda: [resultSelectionPage.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    def extractData(self, mode, bitSelect, fileType, name):
        if fileType == 'Text file (.txt)':
            fileType = 'txt'
        elif fileType == 'Document file (.pdf/.doc/.ppt/etc.)':
            fileType = 'img'
        elif fileType == 'Images (jpg/png/gif/etc.)':
            fileType = 'img'
        elif fileType == 'Audio (wav)':
            fileType = 'wav'
        elif fileType == 'Audio (mp3)':
            fileType = 'img'
        elif fileType == 'Audio (mp4)':
            fileType = 'img'

        print(mode,bitSelect)
        print(name)
        steganography = Steganography("", "", int(mode), int(bitSelect), "")
        steganography.setStegoImagePath('result/' + name)
        steganography.setStegoExtractPath('decoded_file')
        steganography.setExtractFileType(fileType)
        print(fileType)
        try:
            dir = './extracted'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
            steganography.decode()
        except:

            pymsgbox.alert('The parameters that you have selected are wrong', 'Error')

    def nameFilePage(self, mainGUI, payloadSelection):
        self.errorFlag = 0
        namingPageFrame = Frame(mainGUI, bg=self.background)
        namingPageFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.selectedPayload = '.'.join(payloadSelection)
        print(self.selectedPayload)

        title = Label(namingPageFrame, text="Single-bit or multi-bit?.", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.8)

        title = Label(namingPageFrame, text="If multi-bit, select number of bits to modify", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0.35, relheight=0.1, relwidth=0.8)

        title = Label(namingPageFrame, text="Name the file", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0.55, relheight=0.1, relwidth=0.8)

        #Single bit or multi bit
        uploadValue = StringVar(namingPageFrame, "1")
        Radiobutton(namingPageFrame, text='Single-Bit mode', variable=uploadValue, value='1', background=self.background).place(relx=0.4, rely=0.3, relheight=0.05, relwidth=0.1)
        Radiobutton(namingPageFrame, text='Multi-Bit mode', variable=uploadValue, value='2', background=self.background).place(relx=0.5, rely=0.3, relheight=0.05, relwidth=0.1)

        #Item quantity scroller
        itemQuantityScroller = Scale(namingPageFrame, from_=0, to=7, orient=HORIZONTAL, resolution = 1)
        itemQuantityScroller.place(relx=0.35, rely=0.45, relheight=0.07, relwidth=0.3)

        nameParameter = StringVar()
        nameEntered = Entry(namingPageFrame, textvariable=nameParameter)
        nameEntered.config(font=("Arial", 15))
        nameEntered.place(relx=0.3, rely=0.65, relheight=0.05, relwidth=0.4)

        # Submit button
        submitButton = Button(namingPageFrame, text="Submit", command=lambda: [
            [namingPageFrame.place_forget(),self.catchSubmit("cover/" + self.selectedCover,"payload/" + self.selectedPayload, int(uploadValue.get()), int(itemQuantityScroller.get()), nameEntered.get())
             ,[self.displayHide(nameEntered.get(), mainGUI)] if self.errorFlag == 0 else self.nameFilePage(mainGUI,payloadSelection)] if nameParameter.get() != "" else [
                self.displayError("name")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.75, relheight=0.08, relwidth=0.15)

        exitButton = Button(namingPageFrame, text="Exit", command=lambda: [namingPageFrame.place_forget(), self.viewPage(mainGUI)])
        exitButton.config(font=("Arial", 25))
        exitButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)


    def catchSubmit(self, cover, payload, uploadValue, bit, name):
        try:
            Steganography(cover,payload,uploadValue,bit,name).hideData()
        except:
            self.errorFlag = 1
            print("error flag triggered")
            pymsgbox.alert("Payload is too big", 'Error')


    def displayError(self, type):
        if type == "file":
            pymsgbox.alert('Please select file', 'Error')

        if type == "message":
            pymsgbox.alert('Please input message', 'Error')

        if type == "name":
            pymsgbox.alert("File name can't be empty", 'Error')

    def displayHide(self, result, mainGUI):






        hideFrame = Frame(mainGUI, bg=self.background)
        hideFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(hideFrame,
                      text="Cover",
                      bg=self.background)
        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(hideFrame,
                      text="Payload",
                      bg=self.background)
        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0.36, rely=0, relheight=0.1, relwidth=0.25)

        title = Label(hideFrame,
                      text="Stego",
                      bg=self.background)
        title.config(font=("MS Sans Serif", 25))
        title.place(relx=0.74, rely=0, relheight=0.1, relwidth=0.25)





        viewFrame = Frame(hideFrame, bg=self.background)
        viewFrame.place(relx=0, rely=0.1, relheight=0.5, relwidth=0.3)

        viewFrame2 = Frame(hideFrame, bg=self.background)
        viewFrame2.place(relx=0.35, rely=0.1, relheight=0.5, relwidth=0.3)

        viewFrame3 = Frame(hideFrame, bg=self.background)
        viewFrame3.place(relx=0.7, rely=0.1, relheight=0.5, relwidth=0.3)


        #Cover part --------------------------------------------------------------
        img = Image.open("cover/"+self.selectedCover)


        img2 = ImageTk.PhotoImage(img)

        imagewidth = img2.width()
        imageheight = img2.height()

        ratio = imageheight/imagewidth

        if imageheight > 320:
            diff = imageheight - 320
            imageheight = imageheight - diff
            imagewidth = imageheight/ratio

        if imagewidth > 320:
            diff = imagewidth - 320
            imagewidth = imagewidth - diff
            imageheight = ratio * imagewidth

        img = img.resize((int(imagewidth),int(imageheight)))
        img2 = ImageTk.PhotoImage(img)

        panel = Label(viewFrame, image=img2)
        viewFrame.photo = img2
        panel.pack(side="bottom",  expand="yes")

        for i in range(len(self.allowedImg)):
            if self.selectedPayload.split('.')[-1] == self.allowedImg[i]:
                # Result part --------------------------------------------------------------
                img = Image.open("payload/" + self.selectedPayload)

                img2 = ImageTk.PhotoImage(img)

                imagewidth = img2.width()
                imageheight = img2.height()

                ratio = imageheight / imagewidth

                if imageheight > 320:
                    diff = imageheight - 320
                    imageheight = imageheight - diff
                    imagewidth = imageheight / ratio

                if imagewidth > 320:
                    diff = imagewidth - 320
                    imagewidth = imagewidth - diff
                    imageheight = ratio * imagewidth

                img = img.resize((int(imagewidth), int(imageheight)))
                img2 = ImageTk.PhotoImage(img)

                panel = Label(viewFrame2, image=img2)
                viewFrame2.photo = img2
                panel.pack(side="bottom", expand="yes")

        #Result part --------------------------------------------------------------
        try:
            img = Image.open("result/" + result +".png")

            img2 = ImageTk.PhotoImage(img)

            imagewidth = img2.width()
            imageheight = img2.height()

            ratio = imageheight/imagewidth

            if imageheight > 320:
                diff = imageheight - 320
                imageheight = imageheight - diff
                imagewidth = imageheight/ratio

            if imagewidth > 320:
                diff = imagewidth - 320
                imagewidth = imagewidth - diff
                imageheight = ratio * imagewidth

            img = img.resize((int(imagewidth),int(imageheight)))
            img2 = ImageTk.PhotoImage(img)

            panel = Label(viewFrame3, image=img2)
            viewFrame3.photo = img2
            panel.pack(side="bottom",  expand="yes")
        except:
            pass



        # Exit button
        backButton = Button(hideFrame, text="Continue",
                            command=lambda: [hideFrame.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)







if __name__ == '__main__':
    main_GUI = GUI()


