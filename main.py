from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from math import sqrt, ceil
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
    else:
        messagebox.showwarning("Warning", "Tidak ada file yang di upload!")
        x = 0
    

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
        label2 = Label(image=cv2.imshow('im',im))
        label2.grid(row = 3, column=0)
        
def createEntropyGraph():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        global listEntropi,tempHeight
        bitmap = Image.open('im.png')
        bitmap = bitmap.convert('L')
        bitmap = bitmap.convert('1')
        z = list(bitmap.getdata())
        
        listEntropi = []
        tempHeight = []
        for i in range(bitmap.height):

            baris = z[i * bitmap.width:(i + 1) * bitmap.width]
            if baris!=0:
                entropi = stats.entropy(baris)
                listEntropi.append(entropi)
                tempHeight.append(i)

        plt.plot(tempHeight,listEntropi,marker="+")
        plt.show()


def hitungTrueRate():
    global y_true
    global arrayRate

    #keadaan file pada bank malware
    y_true = [1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0]
    confusionMatrix = confusion_matrix(y_true, prediction)

    TP = confusionMatrix[1][1]
    TN = confusionMatrix[0][0]
    FP = confusionMatrix[0][1]
    FN = confusionMatrix[1][0]

    TPR = TP / (TP + FN)

    FPR = FP / (TN + FP)

    arrayRate = []

    arrayRate.append(TPR)
    arrayRate.append(FPR)

    print("TPR:", TPR)
    print("FPR:", FPR)

def cosineSimilarity(list1, list2):
    dot_product = sum(a * b for a, b in zip(list1, list2))
    norm_list1 = sqrt(sum(a ** 2 for a in list1))
    norm_list2 = sqrt(sum(b ** 2 for b in list2))
    return dot_product / (norm_list1 * norm_list2)

def detectMalware():
    arrayMalware = []
    arrayBenign = []
        
    for i in range(len(arrayHasilSimilarity)):
        if y_true[i] == 0 :
            arrayBenign.append(arrayHasilSimilarity[i])
        else :
            arrayMalware.append(arrayHasilSimilarity[i])
        
    averageMalware = mean(arrayMalware)
    averageBenign = mean(arrayBenign)

    #digunakan untuk pengecekan rata-rata persentase kemiripan dari file malware dan file benign yang ada pada bank
    print("rata-rata similarity dengan file malware = "+str(averageMalware))
    print("rata-rata similarity dengan file benign = "+str(averageBenign))
        
    for i in range(len(arrayHasilSimilarity)):
        if arrayHasilSimilarity[i] > 99.8:
            if y_true[i] == 1:
                hasil = "Kemungkinan Besar File adalah Sebuah Malware"
                hasil2 = "Dapat dipastikan file yang diupload adalah sebuah Malware!"
                break
            else:
                hasil = "Kemungkinan Besar File bukan Sebuah Malware"
                hasil2 = "Dapat dipastikan file yang diupload bukan sebuah Malware!"
                break
                    
        else :
            if averageMalware > averageBenign:

                #jika file dengan similarity tertinggi = malware dan nilai TPR paling tinggi
                if y_true[arrayHasilSimilarity.index(max(arrayHasilSimilarity))] == 1 and arrayRate.index(max(arrayRate)) == 0:
                    hasil = "Malware 1"
                    hasil2 = "File yang diupload adalah Malware!"
                    
                #jika file dengan similarity tertinggi = malware dan nilai FPR paling tinggi
                elif y_true[arrayHasilSimilarity.index(max(arrayHasilSimilarity))] == 1 and arrayRate.index(max(arrayRate)) == 1:
                    hasil = "Bukan Malware 1"
                    hasil2 = "File yang diupload adalah bukan Malware!"
                #jika file dengan similarity tertinggi = benign tapi nilai TPR paling tinggi
                elif y_true[arrayHasilSimilarity.index(max(arrayHasilSimilarity))] == 0 and arrayRate.index(max(arrayRate)) == 0:
                    hasil = "Bukan Malware 2"
                    hasil2 = "File yang diupload adalah bukan Malware!"
                else:
                    hasil = "Malware 2"
                    hasil2 = "File yang diupload adalah Malware!"
                        
            elif averageBenign > averageMalware:

                #jika file dengan similarity tertinggi = malware dan nilai FPR paling tinggi
                if y_true[arrayHasilSimilarity.index(max(arrayHasilSimilarity))] == 1 and arrayRate.index(max(arrayRate)) == 1:
                    hasil = "Bukan Malware 3"
                    hasil2 = "File yang diupload adalah bukan Malware!"
                    
                #jika file dengan similarity tertinggi = malware dan nilai TPR paling tinggi
                elif y_true[arrayHasilSimilarity.index(max(arrayHasilSimilarity))] == 1 and arrayRate.index(max(arrayRate)) == 0:
                    hasil = "Malware 3"
                    hasil2 = "File yang diupload adalah Malware!"

                #jika file dengan similarity tertinggi = benign dan nilai FPR paling tinggi
                elif y_true[arrayHasilSimilarity.index(max(arrayHasilSimilarity))] == 0 and arrayRate.index(max(arrayRate)) == 1:
                    hasil = "Malware 4"
                    hasil2 = "File yang diupload adalah Malware!"
                else:
                    hasil = "Bukan Malware 4"
                    hasil2 = "File yang diupload adalah bukan Malware!"
    
    return(hasil,hasil2)

def lihatHasil():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        top2 = Toplevel()
        top2.title("Hasil Similarity")
        #nanti bikin bitmap banyak untuk tiap malware yang ada dibank malware. dibuat juga buat entropy sama grayscale masing-masing
        image1 = Image.open('Cryptowall.png')
        image2 = Image.open('Mamba.png')
        image3 = Image.open('RedBoot.png')
        image4 = Image.open('Rex.png')
        image5 = Image.open('WannaCry.png')
        image6 = Image.open('WannaCryPlus.png')
        image7 = Image.open('oriwotw.png')
        image8 = Image.open('hades.png')
        image9 = Image.open('tunic.png')
        image10 = Image.open('petya1.png')
        image11 = Image.open('petya2.png')
        image12 = Image.open('vipasana1.png')
        image13 = Image.open('vipasana2.png')
        image14 = Image.open('vipasana3.png')
        image15 = Image.open('rks.png')
        image16 = Image.open('notepad.png')
        image17 = Image.open('progressReport.png')
        image18 = Image.open('AfterBurner.png')
        image19 = Image.open('CiscoCollabHost.png')
        image20 = Image.open('GithubDesktop.png')
        image21 = Image.open('NetBeans.png')
        image22 = Image.open('ZeroTierOne.png')

        image1 = image1.convert('L')
        image2 = image2.convert('L')
        image3 = image3.convert('L')
        image4 = image4.convert('L')
        image5 = image5.convert('L')
        image6 = image6.convert('L')
        image7 = image7.convert('L')
        image8 = image8.convert('L')
        image9 = image9.convert('L')
        image10 = image10.convert('L')
        image11 = image11.convert('L')
        image12 = image12.convert('L')
        image13 = image13.convert('L')
        image14 = image14.convert('L')
        image15 = image15.convert('L')
        image16 = image16.convert('L')
        image17 = image17.convert('L')
        image18 = image18.convert('L')
        image19 = image19.convert('L')
        image20 = image20.convert('L')
        image21 = image21.convert('L')
        image22 = image22.convert('L')

        image1 = image1.convert('1')
        image2 = image2.convert('1')
        image3 = image3.convert('1')
        image4 = image4.convert('1')
        image5 = image5.convert('1')
        image6 = image6.convert('1')
        image7 = image7.convert('1')
        image8 = image8.convert('1')
        image9 = image9.convert('1')
        image10 = image10.convert('1')
        image11 = image11.convert('1')
        image12 = image12.convert('1')
        image13 = image13.convert('1')
        image14 = image14.convert('1')
        image15 = image15.convert('1')
        image16 = image16.convert('1')
        image17 = image17.convert('1')
        image18 = image18.convert('1')
        image19 = image19.convert('1')
        image20 = image20.convert('1')
        image21 = image21.convert('1')
        image22 = image22.convert('1')

        data1 = list(image1.getdata())
        data2 = list(image2.getdata())
        data3 = list(image3.getdata())
        data4 = list(image4.getdata())
        data5 = list(image5.getdata())
        data6 = list(image6.getdata())
        data7 = list(image7.getdata())
        data8 = list(image8.getdata())
        data9 = list(image9.getdata())
        data10 = list(image10.getdata())
        data11 = list(image11.getdata())
        data12 = list(image12.getdata())
        data13 = list(image13.getdata())
        data14 = list(image14.getdata())
        data15 = list(image15.getdata())
        data16 = list(image16.getdata())
        data17 = list(image17.getdata())
        data18 = list(image18.getdata())
        data19 = list(image19.getdata())
        data20 = list(image20.getdata())
        data21 = list(image21.getdata())
        data22 = list(image22.getdata())

        tempEntropi1 = []
        tempEntropi2 = []
        tempEntropi3 = []
        tempEntropi4 = []
        tempEntropi5 = []
        tempEntropi6 = []
        tempEntropi7 = []
        tempEntropi8 = []
        tempEntropi9 = []
        tempEntropi10 = []
        tempEntropi11 = []
        tempEntropi12 = []
        tempEntropi13 = []
        tempEntropi14 = []
        tempEntropi15 = []
        tempEntropi16 = []
        tempEntropi17 = []
        tempEntropi18 = []
        tempEntropi19 = []
        tempEntropi20 = []
        tempEntropi21 = []
        tempEntropi22 = []

        # tempHeight2 = []
        for i in range(image1.height):
            baris1 = data1[i * image1.width:(i + 1) * image1.width]
            if baris1!=0:
                entropi1 = stats.entropy(baris1)
                tempEntropi1.append(entropi1)
                # tempHeight2.append(i)

        for i in range(image2.height):
            baris2 = data2[i * image2.width:(i + 1) * image2.width]
            if baris2!=0:
                entropi2 = stats.entropy(baris2)
                tempEntropi2.append(entropi2)
                # tempHeight2.append(i)

        for i in range(image3.height):
            baris3 = data3[i * image3.width:(i + 1) * image3.width]
            if baris3!=0:
                entropi3 = stats.entropy(baris3)
                tempEntropi3.append(entropi3)
                # tempHeight2.append(i)
                
        for i in range(image4.height):
            baris4 = data4[i * image4.width:(i + 1) * image4.width]
            if baris4!=0:
                entropi4 = stats.entropy(baris4)
                tempEntropi4.append(entropi4)
                # tempHeight2.append(i)

        for i in range(image5.height):
            baris5 = data5[i * image5.width:(i + 1) * image5.width]
            if baris5!=0:
                entropi5 = stats.entropy(baris5)
                tempEntropi5.append(entropi5)
                # tempHeight2.append(i)

        for i in range(image6.height):
            baris6 = data6[i * image6.width:(i + 1) * image6.width]
            if baris6!=0:
                entropi6 = stats.entropy(baris6)
                tempEntropi6.append(entropi6)
                # tempHeight2.append(i)
        
        for i in range(image7.height):
            baris7 = data7[i * image7.width:(i + 1) * image7.width]
            if baris7!=0:
                entropi7 = stats.entropy(baris7)
                tempEntropi7.append(entropi7)
                # tempHeight2.append(i)
        
        for i in range(image8.height):
            baris8 = data8[i * image8.width:(i + 1) * image8.width]
            if baris8!=0:
                entropi8 = stats.entropy(baris8)
                tempEntropi8.append(entropi8)
                # tempHeight2.append(i)

        for i in range(image9.height):
            baris9 = data9[i * image9.width:(i + 1) * image9.width]
            if baris9!=0:
                entropi9 = stats.entropy(baris9)
                tempEntropi9.append(entropi9)
                # tempHeight2.append(i)
        
        for i in range(image10.height):
            baris10 = data10[i * image10.width:(i + 1) * image10.width]
            if baris10!=0:
                entropi10 = stats.entropy(baris10)
                tempEntropi10.append(entropi10)
                # tempHeight2.append(i)
        
        for i in range(image10.height):
            baris11 = data11[i * image11.width:(i + 1) * image11.width]
            if baris11!=0:
                entropi11 = stats.entropy(baris11)
                tempEntropi11.append(entropi11)
                # tempHeight2.append(i)
        
        for i in range(image12.height):
            baris12 = data12[i * image12.width:(i + 1) * image12.width]
            if baris12!=0:
                entropi12 = stats.entropy(baris12)
                tempEntropi12.append(entropi12)
                # tempHeight2.append(i)

        for i in range(image13.height):
            baris13 = data13[i * image13.width:(i + 1) * image13.width]
            if baris13!=0:
                entropi13 = stats.entropy(baris13)
                tempEntropi13.append(entropi13)
                # tempHeight2.append(i)

        for i in range(image14.height):
            baris14 = data14[i * image14.width:(i + 1) * image14.width]
            if baris14!=0:
                entropi14 = stats.entropy(baris14)
                tempEntropi14.append(entropi14)
                # tempHeight2.append(i)
        
        for i in range(image15.height):
            baris15 = data15[i * image15.width:(i + 1) * image15.width]
            if baris15!=0:
                entropi15 = stats.entropy(baris15)
                tempEntropi15.append(entropi15)
                # tempHeight2.append(i)

        for i in range(image16.height):
            baris16 = data16[i * image16.width:(i + 1) * image16.width]
            if baris14!=0:
                entropi16 = stats.entropy(baris16)
                tempEntropi16.append(entropi16)
                # tempHeight2.append(i)

        for i in range(image17.height):
            baris17 = data17[i * image17.width:(i + 1) * image17.width]
            if baris17!=0:
                entropi17 = stats.entropy(baris17)
                tempEntropi17.append(entropi17)
                # tempHeight2.append(i)

        for i in range(image18.height):
            baris18 = data18[i * image18.width:(i + 1) * image18.width]
            if baris18!=0:
                entropi18 = stats.entropy(baris18)
                tempEntropi18.append(entropi18)
                # tempHeight2.append(i)

        for i in range(image19.height):
            baris19 = data19[i * image19.width:(i + 1) * image19.width]
            if baris19!=0:
                entropi19 = stats.entropy(baris19)
                tempEntropi19.append(entropi19)
                # tempHeight2.append(i)

        for i in range(image20.height):
            baris20 = data20[i * image20.width:(i + 1) * image20.width]
            if baris20!=0:
                entropi20 = stats.entropy(baris20)
                tempEntropi20.append(entropi20)
                # tempHeight2.append(i)

        for i in range(image21.height):
            baris21 = data21[i * image21.width:(i + 1) * image21.width]
            if baris21!=0:
                entropi21 = stats.entropy(baris21)
                tempEntropi21.append(entropi21)
                # tempHeight2.append(i)

        for i in range(image22.height):
            baris22 = data22[i * image22.width:(i + 1) * image22.width]
            if baris22!=0:
                entropi22 = stats.entropy(baris22)
                tempEntropi22.append(entropi22)
                # tempHeight2.append(i)

        #bersihkan list prediksi tiap kali lihat hasil
        prediction.clear()

        hasilSimilarity1 = cosineSimilarity(listEntropi,tempEntropi1)*100
        hasilSimilarity2 = cosineSimilarity(listEntropi,tempEntropi2)*100
        hasilSimilarity3 = cosineSimilarity(listEntropi,tempEntropi3)*100
        hasilSimilarity4 = cosineSimilarity(listEntropi,tempEntropi4)*100
        hasilSimilarity5 = cosineSimilarity(listEntropi,tempEntropi5)*100
        hasilSimilarity6 = cosineSimilarity(listEntropi,tempEntropi6)*100
        hasilSimilarity7 = cosineSimilarity(listEntropi,tempEntropi7)*100
        hasilSimilarity8 = cosineSimilarity(listEntropi,tempEntropi8)*100
        hasilSimilarity9 = cosineSimilarity(listEntropi,tempEntropi9)*100
        hasilSimilarity10 = cosineSimilarity(listEntropi,tempEntropi10)*100
        hasilSimilarity11 = cosineSimilarity(listEntropi,tempEntropi11)*100
        hasilSimilarity12 = cosineSimilarity(listEntropi,tempEntropi12)*100
        hasilSimilarity13 = cosineSimilarity(listEntropi,tempEntropi13)*100
        hasilSimilarity14 = cosineSimilarity(listEntropi,tempEntropi14)*100
        hasilSimilarity15 = cosineSimilarity(listEntropi,tempEntropi15)*100
        hasilSimilarity16 = cosineSimilarity(listEntropi,tempEntropi16)*100
        hasilSimilarity17 = cosineSimilarity(listEntropi,tempEntropi17)*100
        hasilSimilarity18 = cosineSimilarity(listEntropi,tempEntropi18)*100
        hasilSimilarity19 = cosineSimilarity(listEntropi,tempEntropi19)*100
        hasilSimilarity20 = cosineSimilarity(listEntropi,tempEntropi20)*100
        hasilSimilarity21 = cosineSimilarity(listEntropi,tempEntropi21)*100
        hasilSimilarity22 = cosineSimilarity(listEntropi,tempEntropi22)*100
        
        
        if (hasilSimilarity1 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity2 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity3 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity4 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity5 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity6 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        #untuk prediksi jika sebuah file adalah benign file akan digunakan threshold sebesar 85%
        if (hasilSimilarity7 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity8 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity9 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity10 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity11 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity12 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity13 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)

        if (hasilSimilarity14 >= 70):
            prediction.append(1)
        else:
            prediction.append(0)
        
        if (hasilSimilarity15 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity16 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity17 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity18 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity19 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity20 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity21 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        if (hasilSimilarity22 >= 85):
            prediction.append(0)
        else:
            prediction.append(1)

        hitungTrueRate()

        global arrayHasilSimilarity
        arrayHasilSimilarity = []

        arrayHasilSimilarity.append(hasilSimilarity1)
        arrayHasilSimilarity.append(hasilSimilarity2)
        arrayHasilSimilarity.append(hasilSimilarity3)
        arrayHasilSimilarity.append(hasilSimilarity4)
        arrayHasilSimilarity.append(hasilSimilarity5)
        arrayHasilSimilarity.append(hasilSimilarity6)
        arrayHasilSimilarity.append(hasilSimilarity7)
        arrayHasilSimilarity.append(hasilSimilarity8)
        arrayHasilSimilarity.append(hasilSimilarity9)
        arrayHasilSimilarity.append(hasilSimilarity10)
        arrayHasilSimilarity.append(hasilSimilarity11)
        arrayHasilSimilarity.append(hasilSimilarity12)
        arrayHasilSimilarity.append(hasilSimilarity13)
        arrayHasilSimilarity.append(hasilSimilarity14)
        arrayHasilSimilarity.append(hasilSimilarity15)
        arrayHasilSimilarity.append(hasilSimilarity16)
        arrayHasilSimilarity.append(hasilSimilarity17)
        arrayHasilSimilarity.append(hasilSimilarity18)
        arrayHasilSimilarity.append(hasilSimilarity19)
        arrayHasilSimilarity.append(hasilSimilarity20)
        arrayHasilSimilarity.append(hasilSimilarity21)
        arrayHasilSimilarity.append(hasilSimilarity22)

        #jalankan function untuk mendeteksi malware
        hasilA,hasilB = detectMalware()
        print(hasilA)

        frame1 = LabelFrame(top2,text="Cryptowall",padx=10)
        frame1.grid(column=0,row=0)
        frame2 = LabelFrame(top2,text="Mamba",padx=10)
        frame2.grid(column=0,row=1)
        frame3 = LabelFrame(top2,text="RedBoot",padx=10)
        frame3.grid(column=0,row=2)
        frame4 = LabelFrame(top2,text="Rex",padx=10)
        frame4.grid(column=0,row=3)
        frame5 = LabelFrame(top2,text="WannaCry",padx=10)
        frame5.grid(column=0,row=4)
        frame6 = LabelFrame(top2,text="WannaCry+",padx=10)
        frame6.grid(column=0,row=5)
        frame7 = LabelFrame(top2,text="oriwotw.exe",padx=10)
        frame7.grid(column=1,row=0)
        frame8 = LabelFrame(top2,text="hades.exe",padx=10)
        frame8.grid(column=1,row=1)
        frame9 = LabelFrame(top2,text="tunic.exe",padx=10)
        frame9.grid(column=1,row=2)
        frame10 = LabelFrame(top2,text="Petya(v1)",padx=10)
        frame10.grid(column=1,row=3)
        frame11 = LabelFrame(top2,text="Petya(v2)",padx=10)
        frame11.grid(column=1,row=4)
        frame12 = LabelFrame(top2,text="Vipasana(v1)",padx=10)
        frame12.grid(column=1,row=5)
        frame13 = LabelFrame(top2,text="Vipasana(v2)",padx=10)
        frame13.grid(column=2,row=0)
        frame14 = LabelFrame(top2,text="Vipasana(v3)",padx=10)
        frame14.grid(column=2,row=1)
        frame15 = LabelFrame(top2,text="Rks.pdf",padx=10)
        frame15.grid(column=2,row=2)
        frame16 = LabelFrame(top2,text="Notepad.exe",padx=10)
        frame16.grid(column=2,row=3)
        frame17 = LabelFrame(top2,text="ProgressReport.pdf",padx=10)
        frame17.grid(column=2,row=4)
        frame18 = LabelFrame(top2,text="AfterBurner.exe",padx=10)
        frame18.grid(column=2,row=5)
        frame19 = LabelFrame(top2,text="Webex.exe",padx=10)
        frame19.grid(column=0,row=6)
        frame20 = LabelFrame(top2,text="Github.exe",padx=10)
        frame20.grid(column=1,row=6)
        frame21 = LabelFrame(top2,text="NetBeans.exe",padx=10)
        frame21.grid(column=2,row=6)
        frame22 = LabelFrame(top2,text="ZeroTierOne.exe",padx=15)
        frame22.grid(column=0,row=7)

        Hasil1 = Label(frame1,text=hasilSimilarity1)
        Hasil1.pack()
        Hasil1.config(text="{:.2f}%".format(hasilSimilarity1))

        Hasil2 = Label(frame2,text=hasilSimilarity2)
        Hasil2.pack()
        Hasil2.config(text="{:.2f}%".format(hasilSimilarity2))

        Hasil3 = Label(frame3,text=hasilSimilarity3)
        Hasil3.pack()
        Hasil3.config(text="{:.2f}%".format(hasilSimilarity3))

        Hasil4 = Label(frame4,text=hasilSimilarity4)
        Hasil4.pack()
        Hasil4.config(text="{:.2f}%".format(hasilSimilarity4))

        Hasil5 = Label(frame5,text=hasilSimilarity5)
        Hasil5.pack()
        Hasil5.config(text="{:.2f}%".format(hasilSimilarity5))

        Hasil6 = Label(frame6,text=hasilSimilarity6)
        Hasil6.pack()
        Hasil6.config(text="{:.2f}%".format(hasilSimilarity6))

        Hasil7 = Label(frame7,text=hasilSimilarity7)
        Hasil7.pack()
        Hasil7.config(text="{:.2f}%".format(hasilSimilarity7))

        Hasil8 = Label(frame8,text=hasilSimilarity8)
        Hasil8.pack()
        Hasil8.config(text="{:.2f}%".format(hasilSimilarity8))

        Hasil9 = Label(frame9,text=hasilSimilarity9)
        Hasil9.pack()
        Hasil9.config(text="{:.2f}%".format(hasilSimilarity9))

        Hasil10 = Label(frame10,text=hasilSimilarity10)
        Hasil10.pack()
        Hasil10.config(text="{:.2f}%".format(hasilSimilarity10))

        Hasil11 = Label(frame11,text=hasilSimilarity11)
        Hasil11.pack()
        Hasil11.config(text="{:.2f}%".format(hasilSimilarity11))

        Hasil12 = Label(frame12,text=hasilSimilarity12)
        Hasil12.pack()
        Hasil12.config(text="{:.2f}%".format(hasilSimilarity12))

        Hasil13 = Label(frame13,text=hasilSimilarity13)
        Hasil13.pack()
        Hasil13.config(text="{:.2f}%".format(hasilSimilarity13))

        Hasil14 = Label(frame14,text=hasilSimilarity14)
        Hasil14.pack()
        Hasil14.config(text="{:.2f}%".format(hasilSimilarity14))

        Hasil15 = Label(frame15,text=hasilSimilarity15)
        Hasil15.pack()
        Hasil15.config(text="{:.2f}%".format(hasilSimilarity15))

        Hasil16 = Label(frame16,text=hasilSimilarity16)
        Hasil16.pack()
        Hasil16.config(text="{:.2f}%".format(hasilSimilarity16))

        Hasil17 = Label(frame17,text=hasilSimilarity17)
        Hasil17.pack()
        Hasil17.config(text="{:.2f}%".format(hasilSimilarity17))

        Hasil18 = Label(frame18,text=hasilSimilarity18)
        Hasil18.pack()
        Hasil18.config(text="{:.2f}%".format(hasilSimilarity18))

        Hasil19 = Label(frame19,text=hasilSimilarity19)
        Hasil19.pack()
        Hasil19.config(text="{:.2f}%".format(hasilSimilarity19))

        Hasil20 = Label(frame20,text=hasilSimilarity20)
        Hasil20.pack()
        Hasil20.config(text="{:.2f}%".format(hasilSimilarity20))

        Hasil21 = Label(frame21,text=hasilSimilarity21)
        Hasil21.pack()
        Hasil21.config(text="{:.2f}%".format(hasilSimilarity21))

        Hasil22 = Label(frame22,text=hasilSimilarity22)
        Hasil22.pack()
        Hasil22.config(text="{:.2f}%".format(hasilSimilarity22))

        HasilAkhir = Label(top2,text = hasilB, padx=70)
        HasilAkhir.grid(column=0,row=8,columnspan = 3)

        width = HasilAkhir.winfo_reqwidth()
        top2.geometry(f"{width}x500")

        # frame1.config(text="{:.1f}%".format(hasilSimilarity1))

def grayscaleBank(image):
    image = cv2.imread(image)
    window_name = 'Grayscale Image Malware'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def entropyBank(image):
    gambar = Image.open(image)
    array = list(gambar.getdata())
    gambar = gambar.convert('L')
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

    frameK = LabelFrame(top, text="vipasana2", padx=10,pady=10)
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

btn_hasil = Button(frame2, text="Lihat Persentase Hasil Perbandingan",padx=19,pady=10,command=lihatHasil)
btn_hasil.grid(row=3,column=0,pady=15)

root.mainloop()