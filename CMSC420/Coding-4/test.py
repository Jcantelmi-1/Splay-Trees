import random
file = open('test.txt', 'w')

List = []
for i in range(0,10):
    List.append(i)

random.shuffle(List)
for i in List:  
    string = str('insert,' + str(i) + '\n')
    file.write(string)
file.write('dump')
file.close()