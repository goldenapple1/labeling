import typing
import csv
import string
import pymysql
import time

db = pymysql.connect(
    host="localhost", 
    user="root", 
    password="Jdldda235393", 
    database="dict"
)

cursor = db.cursor()

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

file = csv.reader(open("stardict.csv", "r", encoding="utf-8"))
new_csv = open("words.csv", "w+", encoding="utf-8")
maxs = [0,0,0,0,0]
index = [0,0,0,0,0]
out_range_en = []
out_range_cn = []
cache_file = open("file.txt", "w+", encoding="utf-8")
log = open("log.txt", "w+", encoding="utf-8")

def unexpected_chars(word: str) -> bool:
    if word[0] in ".\"'-":
        return True

    for i in word:
        if i not in string.ascii_letters and i not in "-":
            return True

    for n in word[1:]:
        if n in string.ascii_uppercase:
            return True
        
    return False

def exchange(ex: str, word: str) -> str:
    lemma = ""
    id: list[int] = []

    if ex != "":
        for n in ex.split("/"):
            if n[:2] == "0:":
                lemma = n[2:]
                break
        
    cursor.execute(f"SELECT * FROM lemma WHERE word='{word}';")
    start = time.time() # 阻止程序困在while循环
    word_data = cursor.fetchone()

    while word_data != None:
        if word_data[0] in id:
            return ""
        
        id.append(word_data[0])
        lemma = word_data[2]
        cursor.execute(f"SELECT * FROM lemma WHERE word='{lemma}';")
        word_data = cursor.fetchone()

        if time.time() - start >= 1: # 阻止程序困在while循环
            print(word_data)
            print(lemma)
            exit()

    return lemma

line_num = 0
for line in file:
    if "'" in line[0] or " " in line[0]:
        continue
    if "abbr." in line[2]:
        continue
    if "abbr." in line[3]:
        continue
    if line[3] == "":
        continue
    if line[0].isalpha() == False:
        continue
    if unexpected_chars(line[0]):
        continue
    if line[3][:4] == "[网络]" or line[3][:4] == "[地名]":
        continue
    
    line_num += 1
    temp_line = [line[0]]+line[5:8]+[exchange(line[10], line[0])]

    # print(line)
    # if line_num == 10:
    #     break
    
    print(",".join([f'"{n}"' for n in temp_line]), file=new_csv)
    idx = 0
    for n in temp_line:
        if n == None:
            continue
        if len(n) > maxs[idx]:
            maxs[idx] = len(n)
        idx += 1

# [58, 7, 6, 34, 31]
print(maxs)