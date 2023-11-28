import random
file = open('test.txt', 'w')
file.write('initialize,3\n')

List = []
for i in range(0,200):
    List.append(i)

random.shuffle(List)
for i in List:  
    string = str('insert,' + str(i) + ',V\n')
    file.write(string)
file.write('dump')
file.close()