list = [1,2,3,4,5,6,7,8,9,10]
stop = False

for i in list:
    print(i)
    if not stop:
        list.append(i+10)
    else:
        exit()
    if i == 20: stop = True  