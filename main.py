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
    if label is not None:
        label.grid_forget()

    root.filename = filedialog.askopenfilename(initialdir="/Skripsi", title="upload a file", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
    x = 1

    label = Label(root, text=root.filename)
    label.grid(row=2, column=0)

    with open(root.filename, 'rb') as binary_file:
        data=binary_file.read()
    

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

# def hitungFalseRate():
#     true_labels = [1,1,1,1,1,1,0,0,0]

#     false_positives = 0
#     false_negatives = 0

#     for i in range(len(true_labels)):
#         if prediction[i] == 1 and true_labels[i] == 0:
#             false_positives += 1
#         elif prediction[i] == 0 and true_labels[i] == 1:
#             false_negatives += 1
    
#     total_negatives = true_labels.count(0)
#     total_positives = true_labels.count(1)

#     fpr = false_positives / total_negatives
#     fnr = false_negatives / total_positives

#     print("False positive rate:", fpr)
#     print("False negative rate:", fnr)

def hitungTrueRate():
    # true_labels = [1,1,1,1,1,1,0,0,0]

    # # Calculate the number of true positive and true negative predictions
    # true_positives = 0
    # true_negatives = 0
    # for i in range(len(true_labels)):
    #     if prediction[i] == 1 and true_labels[i] == 1:
    #         true_positives += 1
    #     elif prediction[i] == 0 and true_labels[i] == 0:
    #         true_negatives += 1

    # # Calculate the true positive rate (TPR) and true negative rate (TNR)
    # total_positives = true_labels.count(1)
    # total_negatives = true_labels.count(0)
    # tpr = true_positives / total_positives
    # tnr = true_negatives / total_negatives

    # print("True positive rate:", tpr)
    # print("True negative rate:", tnr)
    # global confusionMatrix

    y_true = [1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0]
    confusionMatrix = confusion_matrix(y_true, prediction)

    TP = confusionMatrix[1][1]
    TN = confusionMatrix[0][0]
    FP = confusionMatrix[0][1]
    FN = confusionMatrix[1][0]

    # Calculate the TPR
    TPR = TP / (TP + FN)

    # Calculate the FPR
    FPR = FP / (TN + FP)

    # Calculate the TNR
    TNR = TN / (TN + FP)

    # Calculate the FNR
    FNR = FN / (TP + FN)

    # Print the results
    print("TPR:", TPR)
    print("FPR:", FPR)
    print("TNR:", TNR)
    print("FNR:", FNR)
    
def cosineSimilarity(list1, list2):
    dot_product = sum(a * b for a, b in zip(list1, list2))
    norm_list1 = sqrt(sum(a ** 2 for a in list1))
    norm_list2 = sqrt(sum(b ** 2 for b in list2))
    return dot_product / (norm_list1 * norm_list2)

# def filter_small_values(x):
#     return x > 1e-10

def lihatHasil():
    if x==0:
        messagebox.showerror(title=None, message="File Belum Diupload!")
    else:
        top2 = Toplevel()
        top2.geometry("300x500")
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

        # hitungFalseRate()
        hitungTrueRate()
        # print(f"{hasilSimilarity:.2f}")

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
        frame17 = LabelFrame(top2,text="ProgressReport.exe",padx=10)
        frame17.grid(column=2,row=4)

        Hasil1 = Label(frame1,text=hasilSimilarity1)
        Hasil1.grid(column=0,row=0)
        Hasil1.config(text="{:.2f}%".format(hasilSimilarity1))

        Hasil2 = Label(frame2,text=hasilSimilarity2)
        Hasil2.grid(column=0,row=1)
        Hasil2.config(text="{:.2f}%".format(hasilSimilarity2))

        Hasil3 = Label(frame3,text=hasilSimilarity3)
        Hasil3.grid(column=0,row=2)
        Hasil3.config(text="{:.2f}%".format(hasilSimilarity3))

        Hasil4 = Label(frame4,text=hasilSimilarity4)
        Hasil4.grid(column=0,row=3)
        Hasil4.config(text="{:.2f}%".format(hasilSimilarity4))

        Hasil5 = Label(frame5,text=hasilSimilarity5)
        Hasil5.grid(column=0,row=4)
        Hasil5.config(text="{:.2f}%".format(hasilSimilarity5))

        Hasil6 = Label(frame6,text=hasilSimilarity6)
        Hasil6.grid(column=0,row=5)
        Hasil6.config(text="{:.2f}%".format(hasilSimilarity6))

        Hasil7 = Label(frame7,text=hasilSimilarity7)
        Hasil7.grid(column=1,row=0)
        Hasil7.config(text="{:.2f}%".format(hasilSimilarity7))

        Hasil8 = Label(frame8,text=hasilSimilarity8)
        Hasil8.grid(column=1,row=1)
        Hasil8.config(text="{:.2f}%".format(hasilSimilarity8))

        Hasil9 = Label(frame9,text=hasilSimilarity9)
        Hasil9.grid(column=1,row=2)
        Hasil9.config(text="{:.2f}%".format(hasilSimilarity9))

        Hasil10 = Label(frame10,text=hasilSimilarity10)
        Hasil10.grid(column=1,row=3)
        Hasil10.config(text="{:.2f}%".format(hasilSimilarity10))

        Hasil11 = Label(frame11,text=hasilSimilarity11)
        Hasil11.grid(column=1,row=4)
        Hasil11.config(text="{:.2f}%".format(hasilSimilarity11))

        Hasil12 = Label(frame12,text=hasilSimilarity12)
        Hasil12.grid(column=1,row=5)
        Hasil12.config(text="{:.2f}%".format(hasilSimilarity12))

        Hasil13 = Label(frame13,text=hasilSimilarity13)
        Hasil13.grid(column=2,row=0)
        Hasil13.config(text="{:.2f}%".format(hasilSimilarity13))

        Hasil14 = Label(frame14,text=hasilSimilarity14)
        Hasil14.grid(column=2,row=1)
        Hasil14.config(text="{:.2f}%".format(hasilSimilarity14))

        Hasil15 = Label(frame15,text=hasilSimilarity15)
        Hasil15.grid(column=2,row=2)
        Hasil15.config(text="{:.2f}%".format(hasilSimilarity15))

        Hasil16 = Label(frame16,text=hasilSimilarity16)
        Hasil16.grid(column=2,row=3)
        Hasil16.config(text="{:.2f}%".format(hasilSimilarity16))

        Hasil17 = Label(frame17,text=hasilSimilarity17)
        Hasil17.grid(column=2,row=4)
        Hasil17.config(text="{:.2f}%".format(hasilSimilarity17))

        # frame1.config(text="{:.1f}%".format(hasilSimilarity1))
def grayscaleBankCryptowall():
    image = cv2.imread('Cryptowall.png')
    window_name = 'Grayscale Image Cryptowall'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def grayscaleBankMamba():
    image = cv2.imread('Mamba.png')
    window_name = 'Grayscale Image Mamba'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def grayscaleBankRedBoot():
    image = cv2.imread('RedBoot.png')
    window_name = 'Grayscale Image RedBoot'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def grayscaleBankRex():
    image = cv2.imread('Rex.png')
    window_name = 'Grayscale Image Rex'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def grayscaleBankWannaCry():
    image = cv2.imread('WannaCry.png')
    window_name = 'Grayscale Image WannaCry'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def grayscaleBankWannaCryPlus():
    image = cv2.imread('WannaCryPlus.png')
    window_name = 'Grayscale Image WannaCryPlus'
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def entropyBankCryptowall():
    gambar = Image.open('Cryptowall.png')
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

def entropyBankMamba():
    gambar = Image.open('Mamba.png')
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

def entropyBankRedBoot():
    gambar = Image.open('RedBoot.png')
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

def entropyBankRex():
    gambar = Image.open('Rex.png')
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

def entropyBankWannaCry():
    gambar = Image.open('WannaCry.png')
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

def entropyBankWannaCryPlus():
    gambar = Image.open('WannaCryPlus.png')
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
    top.geometry("500x400")
    top.title("Bank Malware")

    frameA = LabelFrame(top, text="Cryptowall", padx=10,pady=10)
    frameA.grid(row=0,column=0,padx=10, pady=10)
    btn_grayscaleA = Button(frameA, text="Grayscale", padx= 13,command=grayscaleBankCryptowall)
    btn_grayscaleA.pack()
    btn_entropyA = Button(frameA, text="Entropy Graph",command=entropyBankCryptowall)
    btn_entropyA.pack()

    frameB = LabelFrame(top, text="Mamba", padx=10,pady=10)
    frameB.grid(row=0,column=1,padx=10, pady=10)
    btn_grayscaleB = Button(frameB, text="Grayscale", padx= 13,command=grayscaleBankMamba)
    btn_grayscaleB.pack()
    btn_entropyB = Button(frameB, text="Entropy Graph" ,command=entropyBankMamba)
    btn_entropyB.pack()

    frameC = LabelFrame(top, text="RedBoot", padx=10,pady=10)
    frameC.grid(row=0,column=2,padx=10, pady=10)
    btn_grayscaleC = Button(frameC, text="Grayscale", padx= 13,command=grayscaleBankRedBoot)
    btn_grayscaleC.pack()
    btn_entropyC = Button(frameC, text="Entropy Graph",command=entropyBankRedBoot )
    btn_entropyC.pack()

    frameD = LabelFrame(top, text="Rex", padx=10,pady=10)
    frameD.grid(row=1,column=0,padx=10, pady=10)
    btn_grayscaleD = Button(frameD, text="Grayscale", padx= 13,command=grayscaleBankRex)
    btn_grayscaleD.pack()
    btn_entropyD = Button(frameD, text="Entropy Graph" ,command=entropyBankRex)
    btn_entropyD.pack()

    frameE = LabelFrame(top, text="WannaCry", padx=10,pady=10)
    frameE.grid(row=1,column=1,padx=10, pady=10)
    btn_grayscaleE = Button(frameE, text="Grayscale", padx= 13,command=grayscaleBankWannaCry)
    btn_grayscaleE.pack()
    btn_entropyE = Button(frameE, text="Entropy Graph" ,command=entropyBankWannaCry)
    btn_entropyE.pack()

    frameF = LabelFrame(top, text="WannaCryPlus", padx=10,pady=10)
    frameF.grid(row=1,column=2,padx=10, pady=10)
    btn_grayscaleF = Button(frameF, text="Grayscale", padx= 13,command=grayscaleBankWannaCryPlus)
    btn_grayscaleF.pack()
    btn_entropyF = Button(frameF, text="Entropy Graph" ,command=entropyBankWannaCryPlus)
    btn_entropyF.pack()

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