from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from math import sqrt, ceil
import math
import cv2
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import confusion_matrix
from statistics import mean
import os


#Inisialisasi variabel

x=0
label = None
global prediction
prediction = []


#upload file sekaligus convert ke bitmap images
def upload():
    global x
    global data
    global label
    global filename
    if label is not None:
        label.grid_forget()

    root.filename = filedialog.askopenfilename(initialdir="/Skripsi", title="upload a file", filetypes=(("all files", "*.*"), ("jpg files", "*.jpg")))
    x = 1
    filename = os.path.basename(root.filename)
    label = Label(root, text=filename)
    label.grid(row=2, column=0)

    if root.filename:
        with open(root.filename, 'rb') as binary_file:
            data=binary_file.read()
            # print(data)
    else:
        messagebox.showwarning("Warning", "Tidak ada file yang di upload!")
        x = 0

# def convertToGrayscale():
#     if x==0:
#         messagebox.showerror(title=None, message="File Belum Diupload!")
#     else:
#         #ambil panjang data dalam bytes
#         len1 = len(data)
#         #buat vektor dari panjang data dalam bytes
#         d = np.frombuffer(data, dtype=np.uint8)
#         #Hitung akar kuadrat dari panjang data dan dibulatkan ke atas agar hasil dari gambar akan dekat dengan persegi
#         sqrt_len = int(ceil(sqrt(len1)))
#         #Panjang data baru
#         len2 = sqrt_len*sqrt_len
#         #jumlah sisa bytes yang harus di tambahkan angka 0 agar dapat menjadi sama
#         pad_len = len2 - len1
#         #tambah 0 di akhir
#         padded_d = np.hstack((d,np.zeros(pad_len, np.uint8)))
#         #ubah data menjadi array 2 dimensi
#         im = np.reshape(padded_d,(sqrt_len, sqrt_len))
#         #simpan gambar menjadi im.png
#         cv2.imwrite('im.png',im)
#         #tampilkan gambar di perangkat lunak
#         label2 = Label(image=cv2.imshow('im',im))
#         label2.grid(row = 3, column=0)

def convertToGrayscale():
    global array_2d
    global width, height
    width = int(ceil(sqrt(len(data))))
    height = int(ceil(sqrt(len(data))))
    array_2d = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            index = i * width + j
            if index < len(data):
                array_2d[i][j] = data[index]
            else:
                break

    numpy_array_2d = np.array(array_2d, dtype=np.uint8)

    cv2.imwrite('im.png',numpy_array_2d)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #tampilkan gambar di perangkat lunak
    label2 = Label(image=cv2.imshow('im',numpy_array_2d))
    label2.grid(row = 3, column=0)
    # return array_2d

def hitungEntropi(data):
    arrayHasil = {}
    for i in data:
        if i in arrayHasil:
            arrayHasil[i] += 1
        else:
            arrayHasil[i] = 1

    entropy = 0.0
    for i in arrayHasil.values():
        p = i / len(data)  
        entropy -= p * math.log2(p)  

    return entropy

def createEntropyGraph():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        global listEntropi,tempHeight
        listEntropi = []
        tempHeight = []

        for i in range(height):
            baris = array_2d[i]
            # nilaiEntropi = hitungEntropi(baris)
            nilaiEntropi = hitungEntropi(baris)
            listEntropi.append(nilaiEntropi)
            tempHeight.append(i)

        plt.plot(tempHeight,listEntropi,marker="+")
        plt.show()

def calculateEntropyList(data2):
    EntropyList = []
    for i in range (len(data2)):
        baris = data2[i]
        nilaiEntropi = hitungEntropi(baris)
        EntropyList.append(nilaiEntropi)
    return EntropyList

def convertToGrayscale2(data2):
    width = int(ceil(sqrt(len(data2))))
    height = int(ceil(sqrt(len(data2))))
    array_2d = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            index = i * width + j
            if index < len(data2):
                array_2d[i][j] = data2[index]
            else:
                break
    return array_2d


def cosineSimilarity(list1, list2):
    dot_product = sum(a * b for a, b in zip(list1, list2))
    norm_list1 = sqrt(sum(a ** 2 for a in list1))
    norm_list2 = sqrt(sum(b ** 2 for b in list2))
    return dot_product / (norm_list1 * norm_list2)

def hitungSimilarity(listData):
    similarities = []
    for i in range (len(listData)):
        fileData = open(listData[i],'rb').read()
        dataGrayscale = convertToGrayscale2(fileData)
        dataEntropi = calculateEntropyList(dataGrayscale)
        similarity = cosineSimilarity(listEntropi,dataEntropi)
        similarities.append(similarity)

    return similarities

def lihatHasil():
    malware = []
    nonMalware = []

    similarityMalware = hitungSimilarity(malware)
    #disini untuk tampilkan tiap kemiripan dengan malware.
    similarityNonMalware = hitungSimilarity(nonMalware)

    avgSimilarityMalware = sum(similarityMalware)/len(similarityMalware)
    avgSimilarityNonMalware = sum(similarityNonMalware)/len(similarityNonMalware)

    if(avgSimilarityMalware>avgSimilarityNonMalware):
        hasil = "ada kemungkinan file sebuah malware."
    




def grayscaleBank(image):
    image = cv2.imread(image)
    window_name = 'Grayscale Image Malware'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def entropyBank(image):
    gambar = Image.open(image)
    array = list(gambar.getdata())
    listEntropi = []
    listHeight = []
    for i in range(gambar.height):
        baris = array[i * gambar.width:(i+1) * gambar.width]
        if baris!=0:
            entropi = stats.entropy(baris)
            listEntropi.append(entropi)
            listHeight.append(i)

    plt.plot(listHeight,listEntropi,marker="+")
    plt.show()
        

def openBank():
    top = Toplevel()
    top.geometry("525x400")
    top.title("Bank Malware")

    frameA = LabelFrame(top, text="Cryptowall", padx=10,pady=10)
    frameA.grid(row=0,column=0,padx=10, pady=10)
    btn_grayscaleA = Button(frameA, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameA.cget("text")+'.png'))
    btn_grayscaleA.pack()
    btn_entropyA = Button(frameA, text="Entropy Graph", command=lambda: entropyBank(frameA.cget("text")+'.png'))
    btn_entropyA.pack()

    frameB = LabelFrame(top, text="Mamba", padx=10,pady=10)
    frameB.grid(row=0,column=1,padx=10, pady=10)
    btn_grayscaleB = Button(frameB, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameB.cget("text")+'.png'))
    btn_grayscaleB.pack()
    btn_entropyB = Button(frameB, text="Entropy Graph", command=lambda: entropyBank(frameB.cget("text")+'.png'))
    btn_entropyB.pack()

    frameC = LabelFrame(top, text="RedBoot", padx=10,pady=10)
    frameC.grid(row=0,column=2,padx=10, pady=10)
    btn_grayscaleC = Button(frameC, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameC.cget("text")+'.png'))
    btn_grayscaleC.pack()
    btn_entropyC = Button(frameC, text="Entropy Graph", command=lambda: entropyBank(frameC.cget("text")+'.png'))
    btn_entropyC.pack()

    frameD = LabelFrame(top, text="Rex", padx=10,pady=10)
    frameD.grid(row=1,column=0,padx=10, pady=10)
    btn_grayscaleD = Button(frameD, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameD.cget("text")+'.png'))
    btn_grayscaleD.pack()
    btn_entropyD = Button(frameD, text="Entropy Graph", command=lambda: entropyBank(frameD.cget("text")+'.png'))
    btn_entropyD.pack()

    frameE = LabelFrame(top, text="WannaCry", padx=10,pady=10)
    frameE.grid(row=1,column=1,padx=10, pady=10)
    btn_grayscaleE = Button(frameE, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameE.cget("text")+'.png'))
    btn_grayscaleE.pack()
    btn_entropyE = Button(frameE, text="Entropy Graph", command=lambda: entropyBank(frameE.cget("text")+'.png'))
    btn_entropyE.pack()

    frameF = LabelFrame(top, text="WannaCryPlus", padx=10,pady=10)
    frameF.grid(row=1,column=2,padx=10, pady=10)
    btn_grayscaleF = Button(frameF, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameF.cget("text")+'.png'))
    btn_grayscaleF.pack()
    btn_entropyF = Button(frameF, text="Entropy Graph", command=lambda: entropyBank(frameF.cget("text")+'.png'))
    btn_entropyF.pack()

    frameG = LabelFrame(top, text="petya1", padx=10,pady=10)
    frameG.grid(row=0,column=3,padx=10, pady=10)
    btn_grayscaleG = Button(frameG, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameG.cget("text")+'.png'))
    btn_grayscaleG.pack()
    btn_entropyG = Button(frameG, text="Entropy Graph", command=lambda: entropyBank(frameG.cget("text")+'.png'))
    btn_entropyG.pack()
    
    frameH = LabelFrame(top, text="petya2", padx=10,pady=10)
    frameH.grid(row=1,column=3,padx=10, pady=10)
    btn_grayscaleH = Button(frameH, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameH.cget("text")+'.png'))
    btn_grayscaleH.pack()
    btn_entropyH = Button(frameH, text="Entropy Graph", command=lambda: entropyBank(frameH.cget("text")+'.png'))
    btn_entropyH.pack()

    frameI = LabelFrame(top, text="vipasana1", padx=10,pady=10)
    frameI.grid(row=2,column=0,padx=10, pady=10)
    btn_grayscaleI = Button(frameI, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameI.cget("text")+'.png'))
    btn_grayscaleI.pack()
    btn_entropyI = Button(frameI, text="Entropy Graph", command=lambda: entropyBank(frameI.cget("text")+'.png'))
    btn_entropyI.pack()

    frameJ = LabelFrame(top, text="vipasana2", padx=10,pady=10)
    frameJ.grid(row=2,column=1,padx=10, pady=10)
    btn_grayscaleJ = Button(frameJ, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameJ.cget("text")+'.png'))
    btn_grayscaleJ.pack()
    btn_entropyJ = Button(frameJ, text="Entropy Graph", command=lambda: entropyBank(frameJ.cget("text")+'.png'))
    btn_entropyJ.pack()

    frameK = LabelFrame(top, text="vipasana3", padx=10,pady=10)
    frameK.grid(row=2,column=2,padx=10, pady=10)
    btn_grayscaleK = Button(frameK, text="Grayscale", padx= 13, command=lambda: grayscaleBank(frameK.cget("text")+'.png'))
    btn_grayscaleK.pack()
    btn_entropyK = Button(frameK, text="Entropy Graph", command=lambda: entropyBank(frameK.cget("text")+'.png'))
    btn_entropyK.pack()

#==========================================================


root = Tk()
root.geometry("650x400")
root.title("Aplikasi Pengecekan Kemiripan Malware")

frame = LabelFrame(root, text="Upload File", padx=150,pady=150)
frame.grid(row=0,column=0,padx=10)
frame2 = LabelFrame(root, text="Menu",pady=15)
frame2.grid(row=0,column=1,padx=10)

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

#,command=lihatHasil
btn_hasil = Button(frame2, text="Lihat Persentase Hasil Perbandingan",padx=19,pady=10)
btn_hasil.grid(row=3,column=0,pady=15)

root.mainloop()