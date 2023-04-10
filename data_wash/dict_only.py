import typing
import csv
import string

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

file = csv.reader(open("stardict.csv", "r", encoding="utf-8"))
new_csv = open("longdict.csv", "w+", encoding="utf-8")
maxs = [0,0,0,0]
index = [0,0,0,0]
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

def trim(definition: str) -> str:
    if definition == "":
        return definition

    chars = definition[:]
    while chars[0] in '." “”‘’\'':
        chars = chars[1:]

    while chars[-1] in '." “”‘’\'':
        chars = chars[:-1]

    return chars.replace("\\n", "||")

def cutoff(words: str, lang: str) -> str:
    if lang == "en":
        index = 250
    elif lang == "cn":
        index = 120

    for n in ["||", "; ", "；"]:
        if n in words:
            lcut = words.find(n, index)
            rcut = words.rfind(n, index)

            if lcut != -1:
                return words[:lcut]
            else:
                return words[:rcut]
    
    return words

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
    temp_line = line[0:2]+[trim(line[2])]+[trim(line[3])]
    
    if len(temp_line[2]) > 250:
        temp_line[2] = cutoff(temp_line[2], "en")
    if len(temp_line[3]) > 120:
        temp_line[3] = cutoff(temp_line[3], "cn")

    # if len(temp_line[2]) > 300:
    #     print("en:", temp_line, file=cache_file)
    # if len(temp_line[3]) > 150:
    #     print("cn:", temp_line, file=cache_file)

    print(",".join([f'"{n}"' for n in temp_line]), file=new_csv)

    idx = 0
    for n in temp_line:
        if len(n) > maxs[idx]:
            maxs[idx] = len(n)
        idx += 1
    
print(maxs)

# [58, 79, 596, 375]