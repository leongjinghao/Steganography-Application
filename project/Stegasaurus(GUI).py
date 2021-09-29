from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import shutil
import os
import ctypes
import glob
from PIL import Image
import cv2, numpy as np
from steganography import Steganography
import pymsgbox  # pip install PyMsgBox


class GUI:
    background = 'lightgrey'
    test = 'white'
    items = []
    message = ""
    typeFlag = ""
    selectedPayload = ""
    selectedCover = ""

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



        item_column = ('File Name', 'File Type')
        payloadList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            payloadList.heading(item_column[i], text=item_column[i])

        payloadList.column(item_column[0], anchor="w")
        payloadList.column(item_column[1], anchor="n", width=10)
        payloadList.place(relx=0, rely=0.1, relheight=0.5, relwidth=0.3333)


        coverList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            coverList.heading(item_column[i], text=item_column[i])

        coverList.column(item_column[0], anchor="w")
        coverList.column(item_column[1], anchor="n", width=10)
        coverList.place(relx=0.33333, rely=0.1, relheight=0.5, relwidth=0.3333)

        resultList = ttk.Treeview(viewFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            resultList.heading(item_column[i], text=item_column[i])

        if len(payloadList.selection()) > 0:
            payloadList.selection_remove(payloadList.selection()[0])

        resultList.column(item_column[0], anchor="w")
        resultList.column(item_column[1], anchor="n", width=10)
        resultList.place(relx=0.66666, rely=0.1, relheight=0.5, relwidth=0.3333)

        payloadFiles = os.listdir('./payload')

        coverFiles = os.listdir('./cover')

        resultFiles = os.listdir('./result')

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

        # Hide button
        hideButton = Button(viewFrame, text="Hide payload",
                            command=lambda: [viewFrame.place_forget(), self.hidePage(mainGUI)])
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
        payloadButton = Button(deleteFrame, text="Payload", command=lambda: [])
        payloadButton.config(font=("Arial", 25))
        payloadButton.place(relx=0.45, rely=0.25, relheight=0.08, relwidth=0.15)

        # Cover button
        coverButton = Button(deleteFrame, text="Cover", command=lambda: [])
        coverButton.config(font=("Arial", 25))
        coverButton.place(relx=0.45, rely=0.45, relheight=0.08, relwidth=0.15)

        # All button
        AllButton = Button(deleteFrame, text="All Files",
                           command=lambda: [deleteFrame.place_forget(), self.deleteFile("3"), self.viewPage(mainGUI)])
        AllButton.config(font=("Arial", 25))
        AllButton.place(relx=0.4, rely=0.65, relheight=0.08, relwidth=0.25)

        # Back button
        backButton = Button(deleteFrame, text="Back",
                            command=lambda: [deleteFrame.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

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

    def hidePage(self, mainGUI):
        hideFrame = Frame(mainGUI, bg=self.background)
        hideFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(hideFrame, text="What would you like to hide?", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0, relheight=0.1, relwidth=0.8)

        # Message button
        messageButton = Button(hideFrame, text="Message",
                               command=lambda: [hideFrame.place_forget(), self.messagePage(mainGUI)])
        messageButton.config(font=("Arial", 25))
        #messageButton.place(relx=0.45, rely=0.45, relheight=0.08, relwidth=0.15)

        # File button
        fileButton = Button(hideFrame, text="File", command=lambda: [hideFrame.place_forget(), self.coverSelectionPage(mainGUI)])
        fileButton.config(font=("Arial", 25))
        fileButton.place(relx=0.45, rely=0.65, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(hideFrame, text="Back", command=lambda: [hideFrame.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    def messagePage(self, mainGUI):
        messagePageFrame = Frame(mainGUI, bg=self.background)
        messagePageFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.typeFlag = "message" #Indicate that program is dealing with a message

        title = Label(messagePageFrame, text="Please enter message", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)

        messageParameter = StringVar()
        nameEntered = Entry(messagePageFrame, textvariable=messageParameter)
        nameEntered.config(font=("Arial", 15))
        nameEntered.place(relx=0.3, rely=0.20, relheight=0.05, relwidth=0.4)

        # Submit button
        submitButton = Button(messagePageFrame, text="Submit", command=lambda: [[messagePageFrame.place_forget(),
                                                                                 self.coverSelectionPage(mainGUI,
                                                                                                         messageParameter.get())] if messageParameter.get() != "" else [
            self.displayError("message")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.65, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(messagePageFrame, text="Back",
                            command=lambda: [messagePageFrame.place_forget(), self.hidePage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    def coverSelectionPage(self, mainGUI):
        coverSelectionFrame = Frame(mainGUI, bg=self.background)
        coverSelectionFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = Label(coverSelectionFrame, text="Choose your cover file.", bg=self.background)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0, relheight=0.1, relwidth=0.8)

        item_column = ('File Name', 'File Type')

        coverList = ttk.Treeview(coverSelectionFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            coverList.heading(item_column[i], text=item_column[i])

        coverList.column(item_column[0], anchor="w")
        coverList.column(item_column[1], anchor="n", width=10)
        coverList.place(relx=0, rely=0.1, relheight=0.5, relwidth=1)

        coverFiles = os.listdir('./cover')

        for f in range(len(coverFiles)):
            coverFiles[f] = coverFiles[f].split('.')

        for i, column in enumerate(coverFiles, start=0):
            coverList.insert("", 0, values=(coverFiles[i]))

        # Submit button
        submitButton = Button(coverSelectionFrame, text="Submit", command=lambda: [
            [coverSelectionFrame.place_forget(),
             self.payloadSelectionPage(mainGUI, coverList.item(coverList.selection())['values'])] if coverList.item(coverList.selection())['values'] != "" else [
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
        Radiobutton(resultSelectionPage, text='Single-Bit mode', variable=uploadValue, value='1', background=self.background).place(relx=0.1, rely=0.7, relheight=0.05, relwidth=0.1)
        Radiobutton(resultSelectionPage, text='Multi-Bit mode', variable=uploadValue, value='2', background=self.background).place(relx=0.2, rely=0.7, relheight=0.05, relwidth=0.1)

        #Item quantity scroller
        itemQuantityScroller = Scale(resultSelectionPage, from_=1, to=7, orient=HORIZONTAL, resolution = 1)
        itemQuantityScroller.place(relx=0.1, rely=0.85, relheight=0.07, relwidth=0.3)

        # Submit button
        submitButton = Button(resultSelectionPage, text="Submit", command=lambda: [
            [resultSelectionPage.place_forget(), Steganography("","",int(uploadValue.get()),int(itemQuantityScroller.get())).decode('result/'+".".join(resultList.item(resultList.selection())['values']))
             ,self.viewPage(mainGUI)] if resultList.item(resultList.selection())['values'] != "" else [
                self.displayError("file")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.65, relheight=0.08, relwidth=0.15)

        # Back button
        backButton = Button(resultSelectionPage, text="Back",
                            command=lambda: [resultSelectionPage.place_forget(), self.viewPage(mainGUI)])
        backButton.config(font=("Arial", 25))
        backButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)

    def nameFilePage(self, mainGUI, payloadSelection):
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
        itemQuantityScroller = Scale(namingPageFrame, from_=1, to=7, orient=HORIZONTAL, resolution = 1)
        itemQuantityScroller.place(relx=0.35, rely=0.45, relheight=0.07, relwidth=0.3)

        nameParameter = StringVar()
        nameEntered = Entry(namingPageFrame, textvariable=nameParameter)
        nameEntered.config(font=("Arial", 15))
        nameEntered.place(relx=0.3, rely=0.65, relheight=0.05, relwidth=0.4)

        # Submit button
        submitButton = Button(namingPageFrame, text="Submit", command=lambda: [
            [namingPageFrame.place_forget(),Steganography("cover/"+self.selectedCover,"payload/"+self.selectedPayload,mode=int(uploadValue.get()),bitSelect=int(itemQuantityScroller.get())).hideData(nameParameter.get()),
             self.viewPage(mainGUI)] if nameParameter.get() != "" else [
                self.displayError("name")]])
        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.45, rely=0.85, relheight=0.08, relwidth=0.15)





    def displayError(self, type):
        if type == "file":
            pymsgbox.alert('Please select file', 'Error')

        if type == "message":
            pymsgbox.alert('Please input message', 'Error')

        if type == "name":
            pymsgbox.alert("File name can't be empty", 'Error')





if __name__ == '__main__':
    main_GUI = GUI()
