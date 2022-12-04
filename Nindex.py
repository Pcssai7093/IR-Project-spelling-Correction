vocabulary=[]
import re
import random
n=3

f=open("./corpus1.txt",encoding='utf8')
data=f.read().split("\n")
f.close()

vocabulary=data

def generateNGrams(n,word):
    nGrams=[]
    i = 0
    size = len(word)
    while((i+n-1)<size):
        nGrams.append(word[i:i+n])
        i+=1
    return nGrams

def creatNIndex(n,vocabulary):
    nIndex = dict()
    for word in vocabulary:
        Ngrams=generateNGrams(n,word)
        for gram in Ngrams:
            if(nIndex.get(gram)==None):
                nIndex[gram]=[word]
            else:
                tlist=nIndex[gram]
                tlist.append(word)
                nIndex[gram]=tlist
    return nIndex


def checkSpelling(word):
    if word not in vocabulary:
        return False
    return True


def generateSuggestedList(word,Bindex,n):
    size=len(word)
    i=0
    slist=[]
    while((i+n-1)<size):
        bg=word[i:i+n]
        poslist=Bindex.get(bg)
        if(poslist!=None):
            poslist=list(set(poslist))
            slist.append(poslist)
        i+=1
    return slist


def lengthCof(word1,word2):
    len1=len(word1)
    len2=len(word2)
    if(len1>len2):
        k=((len2/len1))
        return k
    else:
        k=((len1/len2))
        return k


def editDistance(str1, str2, m, n):
    if m == 0:
        return n
   
    if n == 0:
        return m

    if str1[m-1] == str2[n-1]:
        return editDistance(str1, str2, m-1, n-1)

    return 1 + min(editDistance(str1, str2, m, n-1),    # Insert
                   editDistance(str1, str2, m-1, n),    # Remove
                   editDistance(str1, str2, m-1, n-1)    # Replace
                   )


def editDistanceScore(word1,word2):
    if(lengthCof(word1,word2)<=0.6):
        return 0
    value=editDistance(word1,word2,len(word1),len(word2))
    if(value==1 or value==0):
        return 1
    else: 
        return (1/(2**(value-1)))


def ranking(word,slist):
    lCoefficient=len(word)
    ranks=dict()
    for list in slist:
        for str in list:
            freq=ranks.get(str)
            if(freq==None):
                ranks[str]=1
            else:
                ranks[str]=freq+1
    sortRanks=sorted(ranks.items(), key=lambda x:x[1],reverse=True)
    sortRanks=dict(sortRanks[0:20])
    for key in sortRanks.keys():
        freq = sortRanks.get(key)
        editScore=editDistanceScore(word,key)
        score = freq + editScore
        sortRanks[key]=score
    sortRanks=sorted(sortRanks.items(), key=lambda x:x[1],reverse=True)   
    sortRanks=dict(sortRanks)
    return sortRanks



# * refining ranks when first letter is confident
def refine1(word,ranks,i):
    for key in ranks.keys():
        freq=0
        if(word[0]==key[0]):
            freq=i
            score = freq + ranks.get(key)
            ranks[key]=score
    sortedRanks=sorted(ranks.items(), key=lambda x:x[1],reverse=True)
    return sortedRanks


# * refining ranks when last letter is confident
def refine2(word,ranks,i):
    len1=len(word)
    for key in ranks.keys():
        len2=len(key)
        freq=0
        if(word[len1-1]==key[len2-1]):
            freq=i
            score = freq + ranks.get(key)
            ranks[key]=score
    sortedRanks=sorted(ranks.items(), key=lambda x:x[1],reverse=True)
    return sortedRanks



d2Index=creatNIndex(n,vocabulary)


# * function invocations for refining ranks


# * correct list of 50 words
f1 = open("list1.txt",encoding="utf8")
data1=f1.read()
data1=re.sub("'","",data1)
data1=data1.split(",")
f1.close()

# * wrong list of 50 words (single edit distancs)
f2 = open("list2.txt",encoding="utf8")
data2=f2.read()
data2=re.sub("'","",data2)
data2=data2.split(",")
f2.close()


#  * function for precision
# def precision(data1,data2):
#     i = 0
#     totWords=50
#     crctedWords=0
#     while(i<50):
#         WrngWord=data2[i]
#         CrctWord=data1[i]
#         suglist=generateSuggestedList(WrngWord,d2Index,n)
#         ranks=ranking(WrngWord,suglist)
#         ranks=refine1(WrngWord,ranks)
#         sugWord=ranks[0][0]
#         print(WrngWord," ",CrctWord," ", sugWord)
#         if(sugWord==CrctWord):
#             crctedWords+=1
#         i+=1
#     return (crctedWords/totWords)
# print(precision(data1,data2))



# * pseudo relavance feedback 

def pseudoRF(word,ranks):
    tempranks=list(ranks.keys())
    tempranks=tempranks[0:5]
    size=len(word)
    firstMatches=0
    endMatches=0
    firstLetter=word[0]
    endLetter=word[size-1]
    for i in tempranks:
        size2=len(i)
        if(i[0]==firstLetter):
            firstMatches+=1
        elif(i[size2-1]==endLetter):
            endMatches+=1
    print(firstMatches,endMatches)
    if(firstMatches>=endMatches):
        return dict(refine1(word,ranks,firstMatches)[0:20])
    else:
        return dict(refine2(word,ranks,endMatches)[0:20])
    


option=-1
def mainMenu():
    print("1. spelling suggester")
    print("2. evaluate spelling suggester")
    print("***[enter the respective number to navigate]")
    global option
    option=int(input("Enter:\n"))

print("--------Welcome to the cli tool for Spell checker--------\n\n")

def spellCheckMenu(word):
    n = int(input("Enter the index size:\n"))
    index=creatNIndex(n,vocabulary)
    slist=generateSuggestedList(word,index,n)
    ranks=ranking(word,slist)
    print(ranks)
    return ranks

mainMenu()
if(option==1):
    word=input("Enter the word:\n")
    ranks=spellCheckMenu(word)
    fb=input("Not satisfied with result? (yes/no)")
    while(fb=="yes"):
        if(fb=="yes"):
            print("Try with other index: Enter 1")
            print("Try filters: Enter 2")
            print("Try pseudo relavance feedback: Enter 3")
            option=int(input("Enter input:"))
            if(option==1):
                spellCheckMenu(word)
            elif(option==2):
                print("Are you confident with first letter: Enter 1")
                print("Are you confident with second letter: Enter 2")
                filterOption=int(input("Enter input:"))
                if(filterOption==1):
                    print(refine1(word,ranks,1))
                elif(filterOption==2):
                    print(refine2(word,ranks,1))
            elif(option==3):
                print(pseudoRF(word,ranks))
            fb=input("Not satisfied with result? (yes/no)")
    print("Thank you! have a good day")
#  * edit distance calculator


