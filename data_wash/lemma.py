file = open("lemma.en.txt", "r", encoding="utf-8")
write_to = open("lemma.csv", "w+", encoding="utf-8")

for n in file.readlines():
    split = n.split(" -> ")
    if "/" in split[0]:
        origin = split[0].split("/")[0]
    else:
        origin = split[0]
    words = split[1][:-1].split(',')
    for m in words:
        print(f'{m},{origin}', file=write_to)