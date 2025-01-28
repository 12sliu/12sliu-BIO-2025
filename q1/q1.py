n = int(input())

pandNumbers = []

for i in range(1, 1000000):
    if str(i)[::-1] == str(i):
        pandNumbers.append(i)
        pandNumbers.append(i)

ansArr = []

# print(pandNumbers, len(pandNumbers))

def twosum(arr, sum):
    p1 = 0
    p2 = len(arr) - 1
    ansarr = []
    while True:
        if arr[p1] + arr[p2] > sum:
            p2 -= 1
            # print("p2", p2)
        elif arr[p1] + arr[p2] < sum:
            p1 += 1
#             print("p1", p2)
        elif arr[p1] + arr[p2] == sum:
            ansarr.append((arr[p1], arr[p2]))
#             print(arr[p1], arr[p2])
            p1 += 1
#         print(p1, p2)
#         # print("w")
        if p1 == p2:
            break
#     print(ansarr)
    # print("p2")

    return ansarr


def threesum(arr, sum):
    ansarr = []
    for i, first in enumerate(arr):
        newsum = sum - first
        newarr = arr
        newarr.pop(i)
        value= twosum(newarr, newsum)
        for j in value:
            test = (first,)
            # print(type(test))
            ansarr.append(test + j)
    return ansarr

def main():
    if str(n)[::-1] == str(n):
        print(n)
        return 0

    for i in range(len(pandNumbers)-1, 0, -1):
        if n < pandNumbers[i]:
            pandNumbers.remove(pandNumbers[i])

    val = twosum(pandNumbers, n)
    if len(val) > 0:
        print(val[0])
        return 0

    val = threesum(pandNumbers, n)
    # print(val)
    if len(val) > 0:
        lowestNum = val[0][0]
        fina = [0, 0, 0]
        for ans in val:
            if lowestNum == ans[0] and ans[2] > fina[2]:
                fina = ans
        print(fina)

main()



# twosum([1, 2, 3, 4], 5)



