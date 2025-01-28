
# n = 3

def coord(num):
    return ((num - 1) // n, (num - 1) % n)

# print([coord(i) for i in range(1, 10)])

n, r, g = input().split(" ")

n = int(n)
r = int(r)
g = int(g)

grid = [[0 for i in range(n)] for j in range(n)]

count = 1
pos = 1
rcou, gcou = 0, 0
grid[0][0] = 1
while count < n ** 2:

    while count < n ** 2:
        # print("test")
        if grid[coord(pos)[0]][coord(pos)[1]] == 0:
            if gcou == g-1:
                grid[coord(pos)[0]][coord(pos)[1]] = 2
                count += 1
                gcou = 0
                print(coord(pos), pos)
                break
            else:
                gcou += 1
                pos += 1
                if pos > n ** 2:
                    pos = 1
        else:
            pos += 1
            if pos > n ** 2:
                pos = 1

    while count < n ** 2:
        if grid[coord(pos)[0]][coord(pos)[1]] == 0:
            if rcou == r-1:
                grid[coord(pos)[0]][coord(pos)[1]] = 1
                count += 1
                rcou = 0
                print(coord(pos), pos)
                break
            else:
                rcou += 1
                pos += 1
                if pos > n ** 2:
                    pos = 1
        else:
            pos += 1
            if pos > n ** 2:
                pos = 1

isRed = True

listposset = []

while True:

    def superhavenchecker(pos):
        posset = set()

        def havenchecker(pos):
            if pos > n ** 2 or pos < 1:
                return 0
            if grid[coord(pos)[0]][coord(pos)[1]] == 0:
                return 0
            posset.add(pos)
            if pos-1 not in posset:
                havenchecker(pos-1)
            if pos + 1 not in posset:
                havenchecker(pos+1)
            if pos - n not in posset:
                havenchecker(pos-n)
            if pos + n not in posset:
                havenchecker(pos+n)

        havenchecker(pos)
        return posset

    bigposset = set()

    listposset = []

    for row in grid:
        for pos in row:
            if pos not in bigposset:
                listposset.append(superhavenchecker(pos))
                bigposset.update(listposset[-1])

    listcount = []
    for posset in listposset:
        listcount.append([0, 0, 0])
        for pos in posset:
            if grid[coord(pos)[0]][coord(pos)[1]] == 2:
                listcount[-1][0] += 1
            if grid[coord(pos)[0]][coord(pos)[1]] == 3:
                listcount[-1][1] += 1
            if pos > listcount[-1][2]:
                listcount[-1][2] = pos

    if isRed:
        choice = set()
        choicecount = [99999999, 99999999, 0]
        for i, posset in enumerate(listposset):
            if listcount[i][1] < choicecount[1] and listcount[i][1] > 0:
                choice = posset
                choicecount = listcount[i]
            elif listcount[i][1] == choicecount[1]:
                if listcount[i][0] > choicecount[0]:
                    choice = posset
                    choicecount = listcount[i]
                elif listcount[i][0] == choicecount[0]:
                    if listcount[i][2] > choicecount[2]:
                        choice = posset
                        choicecount = listcount[i]

    else:
        choice = set()
        choicecount = [99999999, 99999999, 0]
        for i, posset in enumerate(listposset):
            if listcount[i][0] < choicecount[0]  and listcount[i][0] > 0:
                choice = posset
                choicecount = listcount[i]
            elif listcount[i][0] == choicecount[0]:
                if listcount[i][1] > choicecount[1]:
                    choice = posset
                    choicecount = listcount[i]
                elif listcount[i][1] == choicecount[1]:
                    if listcount[i][2] > choicecount[2]:
                        choice = posset
                        choicecount = listcount[i]

    if choice == [99999999, 99999999, 0]:
        break


    enemy = 0
    pos = 0
    if isRed:
        while True:
            val = min(choice)
            pos = val - 1
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 3:
                    enemy = pos
                    break
            pos = val - n
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 3:
                    enemy = pos
                    break
            pos = val + n
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 3:
                    enemy = pos
                    break
            pos = val + 1
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 3:
                    enemy = pos
                    break
            choice.remove(val)
    else:
        while True:
            val = min(choice)
            pos = val - 1
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 2:
                    enemy = pos
                    break
            pos = val - n
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 2:
                    enemy = pos
                    break
            pos = val + n
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 2:
                    enemy = pos
                    break
            pos = val + 1
            if not pos > n ** 2 and not pos < 1:
                if grid[coord(pos)[0]][coord(pos)[1]] == 2:
                    enemy = pos
                    break
            choice.remove(val)

    grid[coord(pos)[0]][coord(pos)[1]] = 2 if isRed else 3
    grid[coord(val)[0]][coord(val)[1]] = 0

    isRed = not isRed


red = 0
green = 0
for posset in listposset:
    if posset[0] > posset[1]:
        red += 1
    else:
        green += 1

print(red, green)






print(grid)

