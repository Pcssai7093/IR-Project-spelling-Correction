import googletrans
transaltor=googletrans.Translator()
import os
import time
i=0
k=0
engFiles=os.listdir("C:/Users/chandra sekhar/Desktop/chandra sekhar imp/SEM-5/IR/project/telugu data generator/data")
engLen=len(engFiles)

telFiles=os.listdir("C:/Users/chandra sekhar/Desktop/chandra sekhar imp/SEM-5/IR/project/telugu data generator/telData")
telLen=len(telFiles)
progress=telLen

os.chdir("telugu data generator\\telData")

while(progress<engLen):
    f=open("C:/Users/chandra sekhar/Desktop/chandra sekhar imp/SEM-5/IR/project/telugu data generator/data/"+engFiles[progress],'r')
    tdata=f.read().split('\n')
    f.close()
    teluguData=[]
    k=0
    for word in tdata:
        trans=transaltor.translate(word,dest='te',src='en')
        if(trans!=None):
            telword=trans.text
            teluguData.append(telword)
        
        print("file-" +str(progress)+"conversion in progress----")
        k+=1
    fileName="telFile"+str(progress)+".txt"
    f2=open(fileName,'w',encoding='utf8')
    f2.write('\n'.join(teluguData))
    f2.close()
    progress+=1

# while(i<size):
#     tdata=data[i:i+1000]
#     print(len(tdata))
#     fileName="file"+str(k)+".txt"
#     f=open(fileName,'w')
#     f.write('\n'.join(tdata))
#     k+=1
#     i+=1000

# for word in data:
#     telword=transaltor.translate(word,dest='te',src='en').text
#     teluguData.append(telword)
#     i+=1
#     print(i)

# f2=open("./TeluguWords.txt",'w')
# f2.write('\n'.join(teluguData))