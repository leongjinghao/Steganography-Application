from tkinter import *
from tkinter.filedialog import askopenfilename
import shutil
import os

from PIL import Image

class GUI:
    background = 'lightgrey'
    test = 'white'
    def __init__(self):

        mainGUI = Tk(className='Steganography program')  # Sets window name
        mainGUI.geometry("900x700+100+50")  # Sets window size
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

        #Delete button
        deleteButton = Button(mainMenuFrame, text="Delete")
        deleteButton.config(font=("Arial", 15))
        deleteButton.place(relx=0.35, rely=0.35, relheight=0.05, relwidth=0.1)

        #Delete Radio button
        deleteValue = StringVar(mainMenuFrame, "1")
        Radiobutton(mainMenuFrame, text='Payload', variable=deleteValue, value='1', background=self.background).place(relx=0.5, rely=0.35, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='Cover', variable=deleteValue, value='2', background=self.background).place(relx=0.6, rely=0.35, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='All', variable=deleteValue, value='3', background=self.background).place(relx=0.7, rely=0.35, relheight=0.05, relwidth=0.1)

        #View button
        viewButton = Button(mainMenuFrame, text="View")
        viewButton.config(font=("Arial", 15))
        viewButton.place(relx=0.35, rely=0.5, relheight=0.05, relwidth=0.1)

        # View Radio button
        viewValue = StringVar(mainMenuFrame, "1")
        Radiobutton(mainMenuFrame, text='Payload', variable=viewValue, value='1', background=self.background).place(relx=0.5, rely=0.5, relheight=0.05, relwidth=0.1)
        Radiobutton(mainMenuFrame, text='Cover', variable=viewValue, value='2', background=self.background).place(relx=0.6, rely=0.5, relheight=0.05, relwidth=0.1)


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
        if uploadValue is "1":
            print("hi")
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

    def image(self):
        from PIL import Image
        x = 0
        y = 0
        im = Image.open('test.tiff')  # Can be many different formats.
        pixels = list(im.getdata())
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        #print(pixels)

class Steganography:
    def __init__(self):
        x=1

if __name__ == '__main__':
    main_GUI = GUI() #Instantiates a multiScraperGUI object.
    main_GUI.image()
