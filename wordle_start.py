## Read in file and create a list of the top 2500 five letter words
## 

from os.path import exists
import urllib

# taken from http://corpus.leeds.ac.uk/frqc/internet-en.num
if not exists("internet-en.num.txt"):
    print ("Input file not found...downloading")
    with urllib.request.urlopen('http://corpus.leeds.ac.uk/frqc/internet-en.num') as urlfile:
        wl = urlfile.read().decode('utf-8')
    f = open ("internet-en.num.txt","w",encoding='UTF-8')
    f.write(wl)
    f.close

wl = open("internet-en.num.txt", encoding='UTF-8')
    
for i in range(4):
    temp = wl.readline()
words = []
eof = 0
while (len(words) < 2500) and not eof:
    wordline = wl.readline()
    if len(wordline) > 0:
        temp = wordline.rstrip().split(" ")
        if len(temp) == 3:
            word = temp[2]
            if len(word) == 5:
                words.append(word)
    else:
        eof = 1
wl.close()

## Score each word against all the other words in the list.
#     +1 point for each unique letter found in another word
#     +2 points for each letter matching in position 
##

numwords = len(words)
wordscore = []

for word in words:
    score = 0
    for cword in words:
        uniques = list(set(cword))
        for x in uniques:
            if word.find(x)>=0:
                score += 1
#             print (x, word, score)
        for i in range(5):
            if cword[i]==word[i]:
                score += 2
#             print (i, cword[i], word[i], score)
#         print (word, cword, score)
    wordscore.append(score/numwords)

## Sort the list and print to a file
##

scorelist = dict(zip(words, wordscore))
sorted_scorelist = {k: v for k, v in sorted(scorelist.items(), key=lambda item: item[1], reverse=True)}   

f = open ("output.txt","w",encoding='UTF-8')
output = ("\n".join("{}\t{:.4f}".format(k, v) for k, v in sorted_scorelist.items()))
# print(output)
f.write(output)
f.close()
