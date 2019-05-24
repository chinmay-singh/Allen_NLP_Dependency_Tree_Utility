import numpy as np
from nltk.tokenize import word_tokenize
from allennlp.data.tokenizers import Token
from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/biaffine-dependency-parser-ptb-2018.08.23.tar.gz")


def set_pointer():
    global pointer
    pointer = 1

def reset():
    global pointer
    pointer = 0
    

def search(ref,key,path,cpy):
	if ref['word'] == key:
		set_pointer()
		return ref['word']
	else:
		if 'children' in ref:
			for i in range(len(ref['children'])):
				a = search(ref['children'][i],key,path,cpy)
				
				if pointer == 1:
					if ref['word']==cpy['word']:
						path.append(a)
						path.append(cpy['word'])
						return path 
					path.append(a)
					return ref['word']
				
		else:
			pass	

def final(ref,word):
    reset()
    path = []
    good = search(ref,word,path,ref)
    if type(good)==str:
        good.split()
    return good

def distance(tree,word1,word2):
    a = final(tree,word1)
    if a == None:
#         print("$$$$Tree is",tree,"WORD IS",word1)
        return np.full(5,1)
    b = final(tree,word2)
    if b == None:
#         print("$$$$Tree is",tree,"WORD IS",word2)
        return np.full(5,1)
    i = 0
    j = 0
    way = []
    p=0
    if len(a)<=len(b):
        temp = b
        b = a
        a = temp
    if type(a)!=str:
        a.reverse()
    if type(b)==str:
        b = b.split()
    if(all(x in b for x in a)):
        a.reverse()
        while True:
            if a[i]==b[-1]:                
                way.append(b[-1])
                return way
            else:
                way.append(a[i])
                i +=1

    while i<len(a) and j<len(b):
        if a[i] == b[j]:
            p = 1
            pass
        if p==1:
            way.append(b[j])
            j += 1
        else:
            way.append(a[i])
            i += 1
            
    error = 0
    for i in way:
        error+= len(i)
    if error == len(way):
        l = []
        a = (str("".join(way))) 
        l.append(a)
        return l
    else:
        return way  

ref = predictor.predict("There are many things in this world that i don't like, you are one")['hierplane_tree']['root']

len(distance(ref,'i','things'))
