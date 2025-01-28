import copy
from functools import lru_cache
import time

# f = int(input())
# farr = input().split(" ")
# farr = [int(i) for i in farr]

f = 4
farr = [1483., 1801., 3407., 4999.]
# farr = [1., 1., 1., 1.]

# f = 3
# farr = [7., 14., 14.]
# farr = [100., 100., 100.]

# f = 2
# farr = [1, 3]

errorcheck = set()

truetotal = time.time()
total = 0


class State:
    fuses = []
    time = 0
    fusesLit = []

    def __init__(self, time, fuses, fusesLit, record):
        self.fuses = fuses
        self.time = time

        # 0 = unlit, 1 = lit one end, 2 = lit both
        self.fusesLit = fusesLit

        # debug statement, ignore
        self.record = record

    def update(self):
        start = time.time()

        # copy.deepcopy avoids bugs with passing by reference
        # yes I know python is bad
        timeLeft = copy.deepcopy(self.fuses)

        for i in range(len(self.fusesLit)):
            if self.fusesLit[i] == 0:
                # makes it unpickable
                timeLeft[i] = 99999
            if self.fusesLit[i] == 2:
                timeLeft[i] = timeLeft[i] / 2
            if timeLeft[i] <= 0:
                timeLeft[i] = None


        # convoluted way to remove all None from timeLeft without indexing issues
        j = 0
        for i in range(len(timeLeft)):
            if timeLeft[i - j] is None:
                timeLeft.pop(i - j)
                j += 1

        # picks shortest time until next fuse burns out
        timePassed = min(timeLeft)

        newFuses = []
        for i in range(len(self.fuses)):
            val = timePassed
            if self.fusesLit[i] == 0:
                val = 0
            if self.fusesLit[i] == 2:
                val = timePassed * 2
            newFuses.append(self.fuses[i] - val)
            newFuses[-1] = max(newFuses[-1], 0)

        self.record.append(
            [timePassed, self.time, self.fusesLit, self.fuses]
        )

        global total
        total += time.time() - start

        if max(newFuses) <= 0:
            # I'm keeping this in case I need to examine the breakdown of a time

            # print(f"TIME IS {self.time}")
            # if self.time + timePassed not in errorcheck:
            #     print()
            #     print(self.time + timePassed)
            #     for i in self.record:
            #         print(i, len(self.record))
            #     errorcheck.add(self.time + timePassed)
            return self.time + timePassed, None

        # If the timer has started, then the timer cannot be stopped - it only stops at the end.
        # Remember, no adding together non-consective time periods!
        if self.time > 0:
            return (State(
                self.time + timePassed,
                newFuses,
                self.fusesLit,
                self.record
            ), None
            )

        # Two possible ways for this to go - timer is started or not
        return (State(
            self.time + timePassed,
            newFuses,
            self.fusesLit,
            self.record
        ),
                State(
                    self.time,
                    newFuses,
                    self.fusesLit,
                    self.record
                )
        )


count = 0


def tree(state, depth):
    if state is None:
        return {0.}
    if isinstance(state, float) or isinstance(state, int):
        return {state}
    ans = set()

    global count
    count += 1

    # Neat little recursive thing that gens all possible combinations of fuses lit
    # Please don't investigate how this actually works
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

    possArr = possLit(copy.deepcopy(state.fusesLit), [])

    if depth == 0:
        possArr.pop(0)

    for poss in possArr:
        newstate = copy.deepcopy(state)
        newstate.fusesLit = poss
        updatedstate = newstate.update()

        # This is going to earn me an insane amount of mockery, and I fully accept it: this is garbage.
        # If the returned tuple is (State, State), two tree calls.
        # If returned tuple is (int, None), all fuses have burnt out, call tree with the int so tree saves it to ans.
        # If returned tuple is (State, None), one tree call.
        # Yes it's mind-bendingly stupid
        if isinstance(updatedstate[0], State):
            # Checks if any fuses actually burn in an update - if not, ignore
            useless = True
            for i, fuseLit in enumerate(poss):
                if fuseLit > 0 and state.fuses[i] > 0:
                    useless = False
            if not useless:
                if isinstance(updatedstate[1], State):
                    ans.update(tree(updatedstate[0], depth + 1))
                    ans.update(tree(updatedstate[1], depth + 1))
                else:
                    ans.update(tree(updatedstate[0], depth + 1))
        else:
            ans.update(tree(updatedstate[0], depth + 1))
    return ans


ans = tree(State(0., farr, [0 for i in range(len(farr))], []), 0)
ans.add(0.)

print(time.time() - truetotal)
print(total)

print(len(ans))




