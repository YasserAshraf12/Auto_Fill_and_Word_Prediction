#
# Author: Aya Mahmoud (20170071)
#         Nour Atef (20170325)
#         Yasser Ashraf (20170331)
# Date: 10-5-2021
# Version: 1.0
# Description: GUI Autofill Search (NLP Trigram )
#

# Import Libraries #
import nltk
import numpy as np
from tkinter import *
# ---------------- #

# Uni-gram Function #
def unigram(uniqueWords, words):

    counters = {}
    for i in range(len(uniqueWords)):
        counters[words[i]] = words.count(uniqueWords[i])

    return counters
# --------------------------------------------------------- #

# Bi-gram Function #
def bigram(words):
    wordsDict = {}
    for i in range(len(words) - 1):
        if((words[i] + " " + words[ i + 1]) in wordsDict):
            wordsDict[words[i] + " " + words[ i + 1]] += 1
        else:
            wordsDict[words[i] + " " + words[ i + 1]] = 1
    return wordsDict
# --------------------------------------------------------- #

#Tri-gram Function #
def trigram (words):
    wordsDict = {}
    for i in range(len(words) - 2):
        if ((words[i] + " " + words[i + 1] + " " + words[i + 2]) in wordsDict):
            wordsDict[words[i] + " " + words[i + 1] + " " + words[i + 2]] += 1
        else:
            wordsDict[words[i] + " " + words[i + 1] + " " + words[i + 2]] = 1
    return wordsDict
# --------------------------------------------------------- #

# Probabilities Calculation #
def calculateProb(inputstr, uniqueWords, words):

    triCounterList = trigram(words)
    biCounterList = bigram(words)

    countTri = 0
    countBi = 0

    arr = {}
    dict = []
    li = []

    for sub in triCounterList:
        countTri = triCounterList.get(sub)
        str = sub.split(" ")
        sub2 = str[0] + " " + str[1]
        prob = 0
        if (inputstr == sub2):
            countBi = biCounterList.get(sub2)

            if(countBi == 0 or countTri == 0):
                prob = 0
            else:
                prob = countTri / countBi
                arr[str[2]] = prob
                li.append(prob)

    keys_list = list(arr)

    if(len(li) != 0):
        counterItr = 5
        if(len(li) >=5):
            while(len(li) != 0 and counterItr > 0):

                max_value = max(li)
                max_index = li.index(max_value)
                dict.append(inputstr + " " + keys_list[max_index])
                keys_list.pop(max_index)
                li.pop(max_index)
                counterItr -= 1
        else:
            while (len(li) != 0):
                max_value = max(li)
                max_index = li.index(max_value)
                dict.append(inputstr + " " + keys_list[max_index])
                keys_list.pop(max_index)
                li.pop(max_index)
                counterItr -= 1
    else:
        print("No Search Results...")
    return dict
# --------------------------------------------------------- #

def calculateProbBi(inputstr, uniqueWords, words):


    biCounterList = bigram(words)
    uniCounterList = unigram(uniqueWords, words)

    countBi = 0
    countUni = 0
    arr = {}
    dict = []
    li = []

    for sub in biCounterList:
        countBi = biCounterList.get(sub)
        str = sub.split(" ")
        sub2 = str[0]
        prob = 0
        if (inputstr == sub2):
            countUni = uniCounterList.get(sub2)

            if(countBi == 0 or countUni == 0):
                prob = 0
            else:
                prob = countBi / countUni
                arr[str[1]] = prob
                li.append(prob)

    keys_list = list(arr)
    max_value = max(li)
    max_index = li.index(max_value)
    maxStr = inputstr + " " + keys_list[max_index]

    return (calculateProb(maxStr, uniqueWords, words))
# --------------------------------------------------------- #

# Main Function #
def main():

    file = open("data.txt", "r", encoding="utf8")
    data = file.read()
    file.close()

    words = nltk.word_tokenize(data)

    unique_list = np.unique(words)

    root = Tk()
    root.title('Natural language processing')
    root.geometry("800x800")
    my_label = Label(root, text="Start Typing", font=("Helvetica", 14), fg="grey")
    my_label.pack(pady=20)
    var = StringVar()
    my_entry = Entry(root, font=("Helvetica", 20), textvariable=var)
    my_entry.pack()

    my_list = Listbox(root, width=50)
    my_list.pack(pady=40)

    def update(words_list):
        my_list.delete(0, END)
        for item in words_list:
            my_list.insert(END, item)

    def calculateProbability():
        entry = var.get()
        arr1 = entry.split(" ")
        if(len(arr1) > 1):
            update(calculateProb(entry, unique_list, words))
        else:
            update(calculateProbBi(entry, unique_list, words))

    button = Button(root, text="Search", command=calculateProbability)
    button.pack()

    root.mainloop()

# --------------------------------------------------------- #

# Run #
if __name__ == "__main__":
    main()
# --------------------------------------------------------- #

