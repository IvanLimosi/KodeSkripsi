from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from math import sqrt, ceil
import cv2
import matplotlib.pyplot as plt
from scipy import stats


#variable untuk cek apakah file sudah diupload
x=0

root = Tk()
root.geometry("650x400")
root.title("Aplikasi Pengecekan Kemiripan Malware")


frame = LabelFrame(root, text="Upload File", padx=150,pady=150)
frame.grid(row=0,column=0,padx=10)
frame2 = LabelFrame(root, text="Menu",pady=15)
frame2.grid(row=0,column=1,padx=10)


#upload file sekaligus convert ke bitmap images
def upload():
    global data
    global data2
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
        data2 = bytearray(binary_file.read())
        

def convertToGrayscale():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        #ambil panjang data dalam bytes
        len1 = len(data)
        #buat vektor dari panjang data dalam bytes
        d = np.frombuffer(data, dtype=np.uint8)
        #Hitung akar kuadrat dari panjang data dan dibulatkan ke atas agar hasil dari gambar akan dekat dengan persegi
        sqrt_len = int(ceil(sqrt(len1)))
        #Panjang data baru
        len2 = sqrt_len*sqrt_len
        #jumlah sisa bytes yang harus di tambahkan angka 0 agar dapat menjadi sama
        pad_len = len2 - len1
        #tambah 0 di akhir
        padded_d = np.hstack((d,np.zeros(pad_len, np.uint8)))
        #ubah data menjadi array 2 dimensi
        im = np.reshape(padded_d,(sqrt_len, sqrt_len))
        #simpan gambar menjadi im.png
        cv2.imwrite('im.png',im)
        #tampilkan gambar di perangkat lunak
        label2 = Label(image=cv2.imshow('im',im)).grid(row = 3, column=0)

def createEntropyGraph():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        # convert grayscale image jadi bitmap img
        bitmap = Image.open('im.png')
        # bitmap = bitmap.convert('L')
        z = list(bitmap.getdata())
        # ambil data panjang dan lebar
        width,height = bitmap.size
        # byte_freq = {}
        # for byte in data:
        #     if byte in byte_freq:
        #         byte_freq[byte] += 1
        #     else:
        #         byte_freq[byte] = 1

        # total_bytes = len(data)
        # probabilities = [byte_freq[byte] / total_bytes for byte in byte_freq]

        # entropy = -sum(p * np.log(p) for p in probabilities)

        # plt.plot(entropy,'ro')
        # plt.show()
        global tempEntropi,tempHeight
        tempEntropi = []
        tempHeight = []
        for i in range(bitmap.height):
            #ambil tiap baris dari data bitmap
            baris = z[i * bitmap.width:(i + 1) * bitmap.width]

            # print(width)
            # print(i)
            # print(baris)
            # print(len(baris))
            # break
            # z = baris.getdata()

            # hitung entropy dari tiap baris di data bitmap
            entropi = stats.entropy(baris)
            tempEntropi.append(entropi)
            tempHeight.append(i)
            # print(entropi)
            # print(type(i))
            # print(type(entropi))
        # plot di entropy graph
        plt.plot(tempHeight,tempEntropi,marker="+")
        plt.show()
        # print(width,height)
    

def lihatHasil():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        top2 = Toplevel()
        top2.geometry("200x300")
        top2.title("Hasil Similarity")
        #nanti bikin bitmap banyak untuk tiap malware yang ada dibank malware. dibuat juga buat entropy sama grayscale masing-masing
        bitmap2 = Image.open('im2.png')
        z2 = list(bitmap2.getdata())
        # bitmap2 = bitmap2.convert('1')
        # ambil data panjang dan lebar
        width,height = bitmap2.size
        tempEntropi2 = []
        hasil = 0
        tempHeight2 = []
        for i2 in range(bitmap2.height):
            #ambil tiap baris dari data bitmap
            baris2 = z2[i2 * bitmap2.width:(i2 + 1) * bitmap2.width]
            
            # hitung entropy dari tiap baris di data bitmap
            entropi2 = stats.entropy(baris2)
            tempEntropi2.append(entropi2)
            tempHeight2.append(i2)
        
        for i,j in zip(tempEntropi,tempEntropi2):
            hasil = hasil + abs(i-j)
            # print(hasil)

        hasil2 = 1/(1+hasil) * 100
        print(hasil2)
        

def openBank():
    top = Toplevel()
    top.geometry("500x400")
    top.title("Bank Malware")

    frameA = LabelFrame(top, text="Cerber", padx=10,pady=10)
    frameA.grid(row=0,column=0,padx=10, pady=10)
    btn_grayscaleA = Button(frameA, text="Grayscale", padx= 13)
    btn_grayscaleA.pack()
    btn_entropyA = Button(frameA, text="Entropy Graph")
    btn_entropyA.pack()

    frameB = LabelFrame(top, text="Cerber", padx=10,pady=10)
    frameB.grid(row=0,column=1,padx=10, pady=10)
    btn_grayscaleB = Button(frameB, text="Grayscale", padx= 13)
    btn_grayscaleB.pack()
    btn_entropyB = Button(frameB, text="Entropy Graph" )
    btn_entropyB.pack()

    frameC = LabelFrame(top, text="Cerber", padx=10,pady=10)
    frameC.grid(row=0,column=2,padx=10, pady=10)
    btn_grayscaleC = Button(frameC, text="Grayscale", padx= 13)
    btn_grayscaleC.pack()
    btn_entropyC = Button(frameC, text="Entropy Graph" )
    btn_entropyC.pack()

    frameD = LabelFrame(top, text="Cerber", padx=10,pady=10)
    frameD.grid(row=1,column=0,padx=10, pady=10)
    btn_grayscaleD = Button(frameD, text="Grayscale", padx= 13)
    btn_grayscaleD.pack()
    btn_entropyD = Button(frameD, text="Entropy Graph" )
    btn_entropyD.pack()

    frameE = LabelFrame(top, text="Cerber", padx=10,pady=10)
    frameE.grid(row=1,column=1,padx=10, pady=10)
    btn_grayscaleE = Button(frameE, text="Grayscale", padx= 13)
    btn_grayscaleE.pack()
    btn_entropyE = Button(frameE, text="Entropy Graph" )
    btn_entropyE.pack()

    frameF = LabelFrame(top, text="Cerber", padx=10,pady=10)
    frameF.grid(row=1,column=2,padx=10, pady=10)
    btn_grayscaleF = Button(frameF, text="Grayscale", padx= 13)
    btn_grayscaleF.pack()
    btn_entropyF = Button(frameF, text="Entropy Graph" )
    btn_entropyF.pack()


#button untuk upload file
btn_upload = Button(frame, text="Upload File",command=upload)
btn_upload.pack()

#button untuk buka bank malware
btn_bank = Button(frame2, text="Bank Malware",padx=75,pady=10,command=openBank)
btn_bank.grid(row=0,column=0,pady=15)

#button untuk mengkonversi menjadi grayscale image
btn_grayscale = Button(frame2, text="Converts To Grayscale",command=convertToGrayscale,padx=55,pady=10)
btn_grayscale.grid(row=1,column=0,pady=15)

#button untuk membuat entropy graph
btn_entropy = Button(frame2, text="Create Entropy Graphs",padx=55,pady=10,command=createEntropyGraph)
btn_entropy.grid(row=2,column=0,pady=15)

btn_hasil = Button(frame2, text="Lihat Persentase Hasil Perbandingan",padx=19,pady=10,command=lihatHasil)
btn_hasil.grid(row=3,column=0,pady=15)

root.mainloop()