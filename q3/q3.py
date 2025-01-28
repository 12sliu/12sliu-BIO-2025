import copy
import time
import timeit
from functools import lru_cache

f = int(input())
farr = input().split(" ")

farr = [int(i) for i in farr]

# f = 4
# farr = [4999, 434, 483, 4920]

start = time.time()
total = 0

# # print(farr)

# time = timeit.timeit()

class State:
    fuses = []
    time = 0
    fusesLit = []

    # def __eq__(self, other):
    #     if self.fuses == other.fuses and self.time == other.time and self.fusesLit == other.fusesLit:
    #         return True

    def __init__(self, time, fuses, fusesLit):
        self.fuses = fuses
        self.time = time
        self.fusesLit = fusesLit

    def update(self):
        timeLeft = copy.deepcopy(self.fuses)

        for i in range(len(self.fusesLit)):
            if self.fusesLit[i] == 0:
#                 # print(i, timeLeft)
                timeLeft[i] = 9999
            if self.fusesLit[i] == 2:
                timeLeft[i] = timeLeft[i] / 2
            if timeLeft[i] <= 0:
                timeLeft[i] = None

        j = 0
        for i in range(len(timeLeft)):

            if timeLeft[i-j] is None:
                timeLeft.pop(i-j)
                j += 1

        timePassed = min(timeLeft)
        # print("IMPORTANT", self.time, timePassed, timeLeft)

        newFuses = []
        for i in range(len(self.fuses)):
            val = timePassed
            if self.fusesLit[i] == 0:
                val = 0
            if self.fusesLit[i] == 2:
                val = timePassed * 2
            newFuses.append(self.fuses[i] - val)
            newFuses[-1] = max(newFuses[-1], 0)

#         # print(newFuses)
        #
        if max(newFuses) <= 0:
#             print(f"TIME IS {self.time}")
            return self.time + timePassed, None

        return (State(
            self.time + timePassed,
            newFuses,
            self.fusesLit
        ),
            State(
                self.time,
                newFuses,
                self.fusesLit
            )
        )

count = 0


# @lru_cache(maxsize = None)
def tree(state, depth):
    global total
    global t2
    # total += time.time() - t2
    # t = time.time()

#     print(f"depth is {depth}")
    ans = set()
    if depth is False:
        newstate1, newstate2 = state, 1
    else:
        # t = time.time()
        newstate1, newstate2 = state.update()
        # total += time.time() - t
        if newstate2 is None:
            return {newstate1}
#         print(f"info is {newstate1.fuses, newstate2.fuses, newstate1.fusesLit, newstate2.fusesLit}")

#     print(f"states are {newstate1, newstate2}")
    global count
    count += 1

    def possLit(arr, ans):
        if len(arr) == 0:
            return [ans]
        sumarr = []
        while True:
            sumarr = sumarr + possLit(arr[1:], ans + [arr[0]])
            arr[0] += 1
            if arr[0] > 2:
                break
        return sumarr


# t = time.time()
    possArr = possLit(newstate1.fusesLit, [])
    # total += time.time() - t
    if depth is False:
        possArr.pop(0)
#     print(f"possArr is {possArr}")
#     total += time.time() - t
    # if depth is False:
    for poss in possArr:
        # t = time.time()
        newstate = State(newstate1.time, newstate1.fuses, newstate1.fusesLit)
        newstate.fusesLit = poss
        # total += time.time() - t

        t = time.time()
        tf = newstate.update()[1] is not None
        total += time.time() - t
        if tf:
            useless = True
            for i, thing in enumerate(poss):
                if thing > 0 and newstate1.fuses[i] > 0:
                    useless = False
            if not useless:
                # t2 = time.time()
                ans.update(tree(newstate, True))
        else:
            # t2 = time.time()
            ans.update(tree(newstate, True))

        # val = tree(newstate)
        # ans.update(tree(newstate, depth + 1))
        if newstate2 != 1:
            # t = time.time()
            newstate = State(newstate2.time, newstate2.fuses, newstate2.fusesLit)
            newstate.fusesLit = poss
            # total += time.time() - t
            t = time.time()
            tf = newstate.update()[1] is not None
            total += time.time() - t
            if tf:
                # t = time.time()
                useless = True
                for i, thing in enumerate(poss):
                    if thing > 0 and newstate1.fuses[i] > 0:
                        useless = False
                # total += time.time() - t
                if not useless:
                    # t2 = time.time()
                    ans.update(tree(newstate, True))
            else:
                # t2 = time.time()
                ans.update(tree(newstate, True))

    # total += time.time() - t
    return ans

# t2 = time.time()
ans = tree(State(0, farr, [0 for i in range(len(farr))]), 0)
ans.add(0)

# print(count)
print(len(ans))
# print(total)EE
# print(timeit.timeit("""ans = tree(State(0, farr, [0 for i in range(len(farr))]), 0)
# ans.add(0)
#
# print(count)EE
# print(len(ans))"""))

# print(time.time() - start)  EE

# # print(possLit([0, 0, 0, 0], []))





