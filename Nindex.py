vocabulary=[]


f=open("./corpus1.txt",encoding='utf8')
data=f.read().split("\n")
f.close()

vocabulary=data
n=2


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
            slist.append(poslist)
        i+=1
    return slist


def lengthCof(word1,word2):
    len1=len(word1)
    len2=len(word2)
    if(len1>len2):
        return (len2/len1)
    return (len1/len2)


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
    sortRanks=dict(sortRanks[0:10])
    print(sortRanks)
    for key in sortRanks.keys():
        freq = sortRanks.get(key)
        score = freq + lengthCof(word,key)
        sortRanks[key]=score
    sortRanks=sorted(sortRanks.items(), key=lambda x:x[1],reverse=True)   
    sortRanks=dict(sortRanks)

    print(sortRanks)
    return sortRanks



# * refining ranks when first letter is confident
def refine1(word,ranks):
    for key in ranks.keys():
        freq=0
        if(word[0]==key[0]):
            freq=1
        score = freq + ranks.get(key)
        ranks[key]=score
        sortedRanks=sorted(ranks.items(), key=lambda x:x[1],reverse=True)
    sortedRanks=dict(sortedRanks)
    print(sortedRanks)
    return sortedRanks


# * refining ranks when last letter is confident
def refine2(word,ranks):
    len1=len(word)
    for key in ranks.keys():
        len2=len(key)
        freq=0
        if(word[len1-1]==key[len2-1]):
            freq=1
        score = freq + ranks.get(key)
        ranks[key]=score
        sortedRanks=sorted(ranks.items(), key=lambda x:x[1],reverse=True)
    sortedRanks=dict(sortedRanks)
    return sortedRanks


wrongWord="హొంతకార"
d2Index=creatNIndex(n,vocabulary)
slist=generateSuggestedList(wrongWord,d2Index,n)
ranks=ranking(wrongWord,slist)


# * function invocations for refining ranks
refine1(wrongWord,ranks)
# refine2(wrong,ranks)

# print(ranks)