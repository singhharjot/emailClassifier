import os

#maximus = 10000000000000000000000000
minimus = 10000000000
ham_count = 0
spam_count = 0
word_ham = []
word_spam = []
unwanted = ['\n','\t','\r','\'','"',':',';','.','/','!','#','$','%','{','}','(',')','?','&',']','[','-','_']
for fil in os.listdir("ham/"):
    if fil.endswith(".txt"):
        ham_count = ham_count + 1
        #print (fil)
        tobj = open('ham/'+str(fil),'r')
        f = tobj.read()

        for char in unwanted :
            f = f.replace(char,' ')

        f = f.lower()
        f = f.split(' ')
        word_ham += [ij for ij in f if ij != ' ']
        tobj.close()

for fil in os.listdir("spam/"):
    if fil.endswith(".txt"):
        spam_count = spam_count + 1
        #print (fil)
        tobj2 = open('spam/'+str(fil),'r')
        f2 = tobj2.read()
        
        for char in unwanted :
            f2 = f2.replace(char,' ')

        f2 = f2.lower()
        f2 = f2.split(' ')
        word_spam += [ij for ij in f2 if ij != ' ']
        tobj2.close()


#print word_ham
#print word_spam[4]
uniq_spam = list(set(word_spam))
uniq_ham = list(set(word_ham))
p_h = float(ham_count)/float(ham_count + spam_count)
p_s = float(spam_count)/float(ham_count + spam_count)

print('p(h) = ',end='0'),
print(p_h)
print('p(s) = ',end='0'),
print(p_s)
outputty = open('nb_with_Measure.txt','w')
h_num = 0
s_num = 0
TP = 0
TN = 0
FP = 0
FN = 0
total = 0
for lif in os.listdir("test_s_or_h/"):
    isspam = 0
    isham = 0
    if lif.endswith(".txt"):
        liney = str(lif)+'----classified as----> '
        if lif.endswith('.spam.txt'):
            isspam = 1
            total += 1
        elif lif.endswith('.ham.txt'):
            isham = 1
            total += 1
        else :
            print('Invalid file_name : ' + str(lif))
            break

        test = open('test_s_or_h/'+str(lif),'r')
        #test = open('test_spam_ham.txt','r')
        test_read = test.read()

        for char in unwanted:
            test_read = test_read.replace(char,' ')

        test_read = test_read.lower()
        test_read = test_read.split()
        test_uniq = list(set(test_read))

        V = len(uniq_spam) + len(uniq_ham)
        ham_denom = V + len(word_ham)
        spam_denom = V + len(word_spam)

        #print test_uniq
    
        tempy = p_h
        for w in test_uniq:
            tempy = tempy*((float(word_ham.count(w)+1)/float(ham_denom))**test_read.count(w))
            if test_uniq.index(w)%2 == 0:
                tempy = tempy * minimus

        tem = p_s
        for w in test_uniq:
            tem = tem*((float(word_spam.count(w)+1)/float(spam_denom))**test_read.count(w))
            if test_uniq.index(w)%2 == 0:
                tem = tem * minimus
    
        if tem < tempy :
            outputty.write('\n'+liney+'ham')
            h_num += 1
            if isham :
                TN += 1
            else :
                FN += 1
        else :
            outputty.write('\n'+liney+'spam')
            s_num += 1
            if isspam :
                TP += 1
            else :
                FP += 1

        test.close()
outputty.write('\nham : '+str(h_num)+'\nspam : '+str(s_num))

outputty.write('\n\n##                      Correct(spam)   not correct(not spam)')
outputty.write('\n##(spam)selected            TP              FP')
outputty.write('\n##(not spam)not selected    FN              TN')
P = float(TP)/float(TP+FP)
R = float(TP)/float(TP+FN)
outputty.write('\n\nAccuracy(TP+TN)/(TP+TN+FP+FN) : '+str(float(TP+TN)/float(TP+TN+FP+FN)))
outputty.write('\nPrecision(TP/(TP+FP)) : '+str(P))
outputty.write('\nRecall(TP/(TP+FN)) : '+str(R))
outputty.write('\nF-Measure(2PR/(P+R)) : '+str(float(2*P*R)/float(P+R)))

outputty.close()
	
