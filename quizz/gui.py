import tkinter
from tkinter import *
from PIL import Image, ImageTk

root = Tk()

# Create a photoimage object of the image in the path
image1 = Image.open("about.png")
test = ImageTk.PhotoImage(image1)

label1 = tkinter.Label(image=test)
label1.image = test

# Position image
label1.place(x=100, y=10)
root.mainloop()