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
    top2=Toplevel()
    top2.title("Hasil Similarity")

    pathMalware = r'.\Malware'
    pathNonMalware = r'.\Non Malware'

    malware = [os.path.join(pathMalware, f) for f in os.listdir(pathMalware) if os.path.isfile(os.path.join(pathMalware, f))]
    nonMalware = [os.path.join(pathNonMalware, f) for f in os.listdir(pathNonMalware) if os.path.isfile(os.path.join(pathNonMalware, f))]

    similarityMalware = hitungSimilarity(malware)
    similarityNonMalware = hitungSimilarity(nonMalware)

    avgSimilarityMalware = sum(similarityMalware)/len(similarityMalware)*100
    avgSimilarityNonMalware = sum(similarityNonMalware)/len(similarityNonMalware)*100

    if(avgSimilarityMalware>60 and avgSimilarityMalware>avgSimilarityNonMalware):
        hasil = "kemungkinan file adalah sebuah malware"

    elif(avgSimilarityNonMalware>60 and avgSimilarityNonMalware>avgSimilarityMalware):
        hasil = "kemungkinan file adalah bukan malware."

    else:
        hasil = "tidak dapat diklasifikasikan"

    # print(hasil)
    # print(avgSimilarityMalware)
    # print(avgSimilarityNonMalware)

    def writeSimilarity():
        with open('hasilSimilarity.txt', 'w') as f:
            f.write('--- Similarity dengan File Malware ---\n')
            for file, nilai in zip(malware, similarityMalware):
                f.write(f'File: {file}, Similarity: {nilai*100:.2f}%\n')
            f.write('--- Similarity dengan File Non Malware ---\n')
            for file, nilai in zip(nonMalware, similarityNonMalware):
                f.write(f'File: {file}, Similarity: {nilai*100:.2f}%\n')
        messagebox.showinfo('Info','File sudah diperbarui.')

    writeButton = Button(top2, text="Print Hasil Similarity", command=writeSimilarity)
    writeButton.grid(column=0, row=2, columnspan=2)

    frame1 = LabelFrame(top2, text="Rata-rata similarity dengan Malware")
    frame1.grid(column=0, row=0, padx=10, pady=10)

    frame2 = LabelFrame(top2, text="Rata-rata similarity dengan non malware")
    frame2.grid(column=1, row=0, padx=10, pady=10)

    frame3 = LabelFrame(top2, text="Hasil Akhir")
    frame3.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    Hasil1 = Label(frame1, text="{:.2f}%".format(avgSimilarityMalware))
    Hasil1.grid(padx=10, pady=10)

    Hasil2 = Label(frame2, text="{:.2f}%".format(avgSimilarityNonMalware))
    Hasil2.grid(padx=10, pady=10)

    Hasil3 = Label(frame3, text=hasil)
    Hasil3.grid(padx=10, pady=10)

def grayscaleBank(file):
    pathMalware = r'.\Malware'
    file2 = os.path.join(pathMalware, file)

    with open(file2, 'rb') as f:
        data = f.read()

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

    cv2.imshow(file, numpy_array_2d)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def entropyBank(file):
    pathMalware = r'.\Malware'
    file2 = os.path.join(pathMalware, file)
    with open(file2, 'rb') as f:
        data = f.read()

    arrayBank = convertToGrayscale2(data)

    listEntropi = []
    tempHeight = []

    for i in range(len(arrayBank)):
        baris = arrayBank[i]
        nilaiEntropi = hitungEntropi(baris)
        listEntropi.append(nilaiEntropi)
        tempHeight.append(i)

    plt.plot(tempHeight, listEntropi, marker="+")
    plt.show()

def openBank():
    top = Toplevel()
    top.geometry("750x800")
    top.title("Bank Malware")

    pathMalware = r'.\Malware'
    namaMalware = os.listdir(pathMalware)

    for idx, name in enumerate(namaMalware):
        row, col = divmod(idx, 5)
        frame = LabelFrame(top, text=name, padx=10, pady=10)
        frame.grid(row=row, column=col, padx=10, pady=10)
        btn_grayscale = Button(frame, text="Grayscale", padx=13, command=lambda n=name: grayscaleBank(n))
        btn_grayscale.pack()
        btn_entropy = Button(frame, text="Entropy Graph", command=lambda n=name: entropyBank(n))
        btn_entropy.pack()

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
btn_hasil = Button(frame2, text="Lihat Persentase Hasil Perbandingan",command=lihatHasil,padx=19,pady=10)
btn_hasil.grid(row=3,column=0,pady=15)

root.mainloop()