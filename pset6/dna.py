import sys
import csv

#make sure argument is correct
def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    #prepare database
    file_csv = sys.argv[1]
    file_txt = sys.argv[2]

    database = []

    #load database as dict (better for search)
    with open(file_csv, "r") as data:
        info = csv.DictReader(data)
        for row in info:
            database.append(row)

    #list all the STR so we can read later in the txt
    strs = []

    for key in database[0]:
        strs.append(key)

    strs.pop(0)

    #compute the txt

    with open(file_txt, "r") as file:
        for row in file:
            s = row


    #count strs reppetitive
    count = {}

    #populate the dict and set 0
    for item in strs:
        count[item] = 0

    #compare and populate count

    for item in strs:
        for i in range(len(s)):
            counts = 0
            if s[i:i+len(item)] == item:
                counts = counts + 1
                if count[item] <= counts:
                    count[item] = counts
                for j in range(i+len(item), len(s), len(item)):
                    if s[j:j+len(item)] == item:
                        counts = counts + 1
                        if count[item] <= counts:
                             count[item] = counts
                    else:
                        break

    # check database and finding matchs
    count_matches = 0
    name = None

    for item in database:
        count_matches = 0
        for s in strs:
            if int(item[s]) == count[s]:
                count_matches = count_matches + 1
                if count_matches == len(strs):
                    name = item["name"]

    if name == None:
        print("No match")

    else:
        print(name)





main()


