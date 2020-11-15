def compare(twoNum):
    if twoNum[0] > twoNum[1]:
        return [twoNum[1], twoNum[0]]
    else:
        return [twoNum[0], twoNum[1]]


def mergeSort(data):
    sort = []
    if len(data) % 2 == 0:
        for i in range(0, int(len(data)/2)):
            sort.append(compare([data[2*i], data[2*i + 1]]))
    else:
        for i in range(0, int(len(data)/2) + 1):
            if i == int(len(data)/2):
                sort.append(data[2 * i])
            else:
                sort.append(compare([data[2 * i], data[2 * i + 1]]))



    print(sort)


if __name__ == '__main__':
    user = str(input("numbers: "))
    inter = user.split()
    data = []
    for i in inter:
        data.append(int(i))

    mergeSort(data)