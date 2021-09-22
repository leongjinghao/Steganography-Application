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
        self.mainMenu(mainGUI)
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

        #Upload button
        uploadButton = Button(mainMenuFrame, text="Upload", command=lambda: [self.uploadFile(uploadValue.get())])
        uploadButton.config(font=("Arial", 15))
        uploadButton.place(relx=0.35, rely=0.2, relheight=0.05, relwidth=0.1)

        #Delete Radio button
        deleteValue = StringVar(mainMenuFrame, "1")
        Radiobutton(mainMenuFrame, text='Payload', variable=deleteValue, value='1', background=self.background).place(relx=0.5, rely=0.35, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='Cover', variable=deleteValue, value='2', background=self.background).place(relx=0.6, rely=0.35, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='All', variable=deleteValue, value='3', background=self.background).place(relx=0.7, rely=0.35, relheight=0.05, relwidth=0.1)

        #Delete button
        deleteButton = Button(mainMenuFrame, text="Delete", command=lambda: [self.deleteFile(deleteValue.get())])
        deleteButton.config(font=("Arial", 15))
        deleteButton.place(relx=0.35, rely=0.35, relheight=0.05, relwidth=0.1)

        #View button
        viewButton = Button(mainMenuFrame, text="View", command=lambda: [mainMenuFrame.place_forget(), self.viewPage(mainGUI)])
        viewButton.config(font=("Arial", 15))
        viewButton.place(relx=0.35, rely=0.5, relheight=0.05, relwidth=0.1)

        #Hide button
        hideButton = Button(mainMenuFrame, text="Hide payload",  command=lambda: [print(uploadValue.get(),deleteValue.get(),viewValue.get())])
        hideButton.config(font=("Arial", 15))
        hideButton.place(relx=0.2, rely=0.9, relheight=0.1, relwidth=0.2)

        #Extract button
        extractButton = Button(mainMenuFrame, text="Extract payload") #command=lambda: [self.crawlerPage(mainGUI), mainMenuFrame.place_forget()])
        extractButton.config(font=("Arial", 15))
        extractButton.place(relx=0.6, rely=0.9, relheight=0.1, relwidth=0.2)

        #-----------------------Stats interface-------------------------

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
        title.place(relx=0, rely=0, relheight=0.1, relwidth=0.5)

        title = Label(viewFrame,
                                  text="Cover files",
                                  bg=self.background)


        title.config(font=("MS Sans Serif", 30))
        title.place(relx=0.5, rely=0, relheight=0.1, relwidth=0.5)



        item_column = ('File Name','File Type')
        payloadList = ttk.Treeview(viewFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            payloadList.heading(item_column[i], text=item_column[i])

        payloadList.column(item_column[0], anchor="w")
        payloadList.column(item_column[1], anchor="n", width=10)
        payloadList.place(relx=0,rely=0.1, relheight=0.5, relwidth=0.5)

        item_column = ('File Name','File Type')
        coverList = ttk.Treeview(viewFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            coverList.heading(item_column[i], text=item_column[i])

        coverList.column(item_column[0], anchor="w")
        coverList.column(item_column[1], anchor="n", width=10)
        coverList.place(relx=0.5,rely=0.1, relheight=0.5, relwidth=0.5)

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


        backButton = Button(viewFrame, text="Back", command=lambda: [viewFrame.place_forget(), self.mainMenu(mainGUI)])
        backButton.config(font=("Arial", 30))
        backButton.place(relx=0.05, rely=0.85, relheight=0.1, relwidth=0.2)

        viewPayloadHexButton = Button(viewFrame, text="View payload data", command=lambda: [self.retrieveBinaries(payloadList.item(payloadList.selection())['values'], "payload")])
        viewPayloadHexButton.config(font=("Arial", 11))
        viewPayloadHexButton.place(relx=0.05, rely=0.65, relheight=0.1, relwidth=0.15)

    def retrieveBinaries(self, fileSelection, payloadOrCover):

        x = 0
        y = 0
        file = Image.open('./payload/' + '.'.join(fileSelection))
        file = file.convert('RGB')
        pixels = list(file.getdata())
        print(pixels)
        #width, height = file.size
        #pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        print(pixels)
        #ctypes.windll.user32.MessageBoxW(0, "Your text", fileSelection[0], 1)

    # def image(self):
    #     from PIL import Image
    #     x = 0
    #     y = 0
    #     im = Image.open('test.tiff')  # Can be many different formats.
    #     pixels = list(im.getdata())
    #     width, height = im.size
    #     pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    #     #print(pixels)







class Steganography:
    def __init__(self):
        x=1

if __name__ == '__main__':
    main_GUI = GUI() #Instantiates a multiScraperGUI object.

