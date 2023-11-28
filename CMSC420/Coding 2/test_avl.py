# This is provided to you so that you can test your bst.py file with a particular tracefile.

import argparse
import csv
import avl

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-tf', '--tracefile')
    args = parser.parse_args()
    tracefile = args.tracefile

    t = None
    with open(tracefile, "r") as f:
        reader = csv.reader(f)
        lines = [l for l in reader]
        for l in lines:
            if l[0] == 'insert':
                t = avl.insert(t,int(l[1]),str(l[2]))
            if l[0] == 'bulkInsert':
                bl = l[1:]
                words = []
                for i in range(0,len(bl),2):
                    words.append(bl[i:i+2])
                t = avl.bulkInsert(t,words)
            if l[0] == 'bulkDelete':
                t = avl.bulkDelete(t,[int(i) for i in l[1:]])
            if l[0] == 'search':
                print(avl.search(t,int(l[1])))
            if l[0] == 'replace':
                t = avl.replace(t,int(l[1]),l[2])
            if l[0] == 'dump':
                print(avl.dump(t))