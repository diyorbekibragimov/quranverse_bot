from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("File Open")

root.filename = filedialog.askopenfilename(initialdir="A:/programming/nw/modules/tk", title="Select a File", filetypes=(("png files", "*.png"), ("all files", "*.*")))

mainloop()