from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from math import sqrt, ceil
import cv2

#variable untuk cek apakah file sudah diupload
x=0

root = Tk()
root.geometry("650x400")


frame = LabelFrame(root, text="Upload File", padx=150,pady=150)
frame.grid(row=0,column=0,padx=10)
frame2 = LabelFrame(root, text="Menu",pady=15)
frame2.grid(row=0,column=1,padx=10)


#upload file sekaligus convert ke bitmap images
def upload():
    global data
    label = None
    global x
    root.filename = filedialog.askopenfilename(initialdir="/Skripsi", title="upload a file", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
    x = 1
    while label is None:
        if label is None:
            label = Label(root, text=root.filename).grid(row=2,column=0)
            break
        else:
            label.grid_forget()
            
    with open(root.filename, 'rb') as binary_file:
        data=binary_file.read()

def convertToGrayscale():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        data_len = len(data)
        d = np.frombuffer(data, dtype=np.uint8)
        sqrt_len = int(ceil(sqrt(data_len)))
        new_len = sqrt_len*sqrt_len
        pad_len = new_len - data_len
        #tambah 0 di akhir
        padded_d = np.hstack((d,np.zeros(pad_len, np.uint8)))
        im = np.reshape(padded_d,(sqrt_len, sqrt_len))
        cv2.imwrite('im.png',im)
        label2 = Label(image=cv2.imshow('im',im)).grid(row = 3, column=0)

def createEntropyGraph():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")

def lihatHasil():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")

def openBank():
    top = Toplevel()
    top.geometry("500x400")
    top.title("Bank Malware")

#button untuk upload file
btn_upload = Button(frame, text="Upload File",command=upload)
btn_upload.pack()

btn_bank = Button(frame2, text="Bank Malware",padx=75,pady=10,command=openBank)
btn_bank.grid(row=0,column=0,pady=15)

btn_grayscale = Button(frame2, text="Converts To Grayscale",command=convertToGrayscale,padx=55,pady=10)
btn_grayscale.grid(row=1,column=0,pady=15)

btn_entropy = Button(frame2, text="Create Entropy Graphs",padx=55,pady=10,command=createEntropyGraph)
btn_entropy.grid(row=2,column=0,pady=15)

btn_hasil = Button(frame2, text="Lihat Persentase Hasil Perbandingan",padx=19,pady=10,command=lihatHasil)
btn_hasil.grid(row=3,column=0,pady=15)

btn_hasil2 = Button(frame2, text="Lihat Persentase Hasil Perbandingan",padx=19,pady=10,command=lihatHasil)
btn_hasil2.grid(row=3,column=0,pady=15)
root.mainloop()