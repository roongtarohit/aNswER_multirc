"""
Name: Rohit Roongta
"""

import json
import re
import os

OUTPUT_FILE = 'dev_v2.csv'
INPUT_FILE = 'dev.json'
DELIMITER = ','
IDX = 1
INTERNAL_TAG = 'I'

# Initializing the file
file = open(INPUT_FILE)

# Loading the data
data = json.load(file)

#print(data['data'])

paragraphList = data['data']

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

# HEADERS
with open(OUTPUT_FILE,'a+') as file:
    file.write("ID"+DELIMITER+"TOKEN"+DELIMITER+"TAG\n")

# to convert the sentence into CSV cell format (word,tag)
def generateCSVCell(idx, sentence, ch):
    words = list()
    cell = ''
    if ' ' in sentence:
        words = sentence.split(' ')
        wordIdx = 1
        for word in words:
            if len(word.strip()) is not 0:
                if wordIdx == 1:
                    if "." in word or "?" in word:
                        pos = word.find(".")
                        if pos == -1:
                            pos = word.find("?")
                        cell = cell + str(idx) + DELIMITER + word[0:pos] + DELIMITER + ch + '\n'
                        cell = cell + str(idx) + DELIMITER + word[pos:] + DELIMITER + INTERNAL_TAG + '\n'
                    else:
                        cell = cell + str(idx) + DELIMITER + word + DELIMITER + ch + '\n'
                else:
                    if "." in word or "?" in word:
                        pos = word.find(".")
                        if pos == -1:
                            pos = word.find("?")
                        cell = cell + str(idx) + DELIMITER + word[0:pos] + DELIMITER + INTERNAL_TAG + '\n'
                        cell = cell + str(idx) + DELIMITER + word[pos:] + DELIMITER + INTERNAL_TAG + '\n'
                    else:
                        cell = cell + str(idx) + DELIMITER + word + DELIMITER + INTERNAL_TAG + '\n'
                wordIdx+=1
        return cell
    
    if "." in sentence:
        temp = ''
        pos = sentence.find(".")
        temp = temp + str(idx) + DELIMITER + sentence[0:pos] + DELIMITER + ch + '\n'
        temp = temp + str(idx) + DELIMITER + sentence[pos:] + DELIMITER + INTERNAL_TAG + '\n'
        return temp
        
    return str(idx) + DELIMITER + sentence + DELIMITER + ch + '\n'

# to remove the redundant tag and data represent in the text
def sentenceFormat(sentence):
    """ Need to change this to remove """
    sentence = sentence.replace('</b>','').replace('<b>','').replace('<br>','').replace(',','').replace('\\','').replace('"','')
    sentence = re.sub('Sent\s[0-9]*:', '', sentence)
    sentence = sentence.strip()
    return sentence



for paragraphs in paragraphList:
    
    paraInfo = paragraphs['paragraph']
    sentences = paraInfo['text'].split('<br><b>')
    questionList = paraInfo['questions']
    
    
    
    for questions in questionList:
        questionText = questions['question']
        sentences_used = questions['sentences_used']
        
        if "?" not in questionText:
            questionText = questionText + "?"
        
        print(IDX, " --- ", questionText)
        
        paraData=''
        for idx in range(0,len(sentences)):
            paraData = paraData + generateCSVCell(IDX, sentenceFormat(sentences[idx]), 'P')
        
        quesData = generateCSVCell(IDX, sentenceFormat(questionText), 'Q')
        
        answersList = questions['answers']
        ansData = ''
        
        for answers in answersList:
            """ Adding dot at the end of answer """
            answerText = answers['text'] + "."
            isAnswer = answers['isAnswer']
            if isAnswer:
                ansData = ansData + generateCSVCell(IDX, sentenceFormat(answerText), 'C')
            else:
                ansData = ansData + generateCSVCell(IDX, sentenceFormat(answerText), 'W')
        
        IDX += 1

        with open(OUTPUT_FILE,'a+') as file:
            file.write(paraData+quesData+ansData)
            #file.write("*****************************,****,******\n")
