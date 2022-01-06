## Read in file and create a list of the top 2500 five letter words
## 

from os.path import exists
import urllib

def all_a2z(word):
    a2z = ['a' <= c <= 'z' for c in word]
    return all(a2z)

source_url = ["http://corpus.leeds.ac.uk/frqc/internet-en.num","https://github.com/IlyaSemenov/wikipedia-word-frequency/blob/master/results/enwiki-20190320-words-frequency.txt","https://github.com/dwyl/english-words/blob/master/words_alpha.txt?raw=true"]
source_filename = ["internet-en.num.txt","enwiki-20190320-words-frequency.txt","words_alpha.txt"]
source_delimiter = [" "," "," "]
source_column_number = [3,1,1]
source_header_lines = [4,0,0]

# Choose source!
# 0. University of Leeds English Corpora (20k words includes frequency)
# 1. Scrape of wikipedia (2.1 M words, includes frequency)
# 2. Huge word list (466k words, no frequency) - if you use this list, increase the number of words > 16k
source = 1
# Number of words to analyze
max_number_of_words = 2500

# taken from http://corpus.leeds.ac.uk/frqc/internet-en.num
if not exists(source_filename[source]):
    print ("Input file not found...downloading")
    with urllib.request.urlopen(source_url[source]) as urlfile:
        wl = urlfile.read().decode('utf-8')
    f = open (source_filename[source],"w",encoding='UTF-8')
    f.write(wl)
    f.close

wl = open(source_filename[source], encoding='UTF-8')
    
for i in range(source_header_lines[source]):
    temp = wl.readline()
words = []
eof = 0
while (len(words) < max_number_of_words) and not eof:
    wordline = wl.readline()
    if len(wordline) > 0:
        temp = wordline.rstrip().split(source_delimiter[source])
        if len(temp) >= source_column_number[source]:
            word = temp[source_column_number[source]-1].lower()
            if not all_a2z(word):
                continue
            if len(word) == 5:
                words.append(word)
    else:
        eof = 1
wl.close()

print ("List has " + str(len(words)) + " words.")

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
    if len(wordscore) % int(numwords/10) == 0:
        print (str(len(wordscore)) + " words completed.")
    
## Sort the list and print to a file
##

scorelist = dict(zip(words, wordscore))
sorted_scorelist = {k: v for k, v in sorted(scorelist.items(), key=lambda item: item[1], reverse=True)}   

f = open ("output.txt","w",encoding='UTF-8')
output = ("\n".join("{}\t{:.4f}".format(k, v) for k, v in sorted_scorelist.items()))
# print(output)
f.write(output)
f.close()
