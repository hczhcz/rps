class RPSlib:
    member = ()
    __lib = {}

    def __feedonce(self, data):
        if data in self.__lib:
            self.__lib[data] += 1
        else:
            self.__lib[data] = 1

    def feed(self, data):
        for i in range(len(data)):
            self.__feedonce(data[i:])

    def __getonce(self, data):
        return {
            i: self.__lib[data + i]
            if (data + i) in self.__lib else 0
            for i in self.member
        }

    def get(self, data):
        return [
            self.__getonce(data[i:])
            for i in range(len(data) + 1)
        ]

    def __init__(self, tomember=('r', 'p', 's')):
        self.member = tomember


class RPSholder(RPSlib):
    current = ''

    def step(self, stepdata):
        self.current += stepdata
        self.feed(self.current)

    def parse(self, data):
        for i in data:
            self.step(i)


class RPSbot(RPSlib):
    def __rate(self, pos, total):
        return (3 ** pos) / ((total + 1.0) ** 0.5)

    def guess(self, data):
        result = {
            i: 0 for i in self.member
        }
        d = self.get(data)

        for j in range(len(d)):
            s = sum(d[j].values())
            for i in self.member:
                result[i] += float(d[j][i]) * self.__rate(len(d) - j - 1, s)

        return result

    def choose(self, data):
        g = self.guess(data)
        return max(g, key=g.get)


class RPSbotholder(RPSholder, RPSbot):
    def input(self, stepdata):
        self.step(stepdata)
        return self.choose(self.current)

    def multiinput(self, data):
        return ''.join([
            self.input(i) for i in data
        ])


class RPSgame(RPSbotholder):
    lastguess = 'r'
    membermap = {'r': 'p', 'p': 's', 's': 'r'}
    exitchar = 'x'
    played = 0
    botwin = 0

    def play(self, domap=True):
        import sys
        c = sys.stdin.read(1)
        if c in self.member:
            self.played += 1
            if c == self.lastguess:
                self.botwin += 1
            print self.membermap[self.lastguess] if domap else self.lastguess,
            print ' (', self.botwin, '/', self.played, ')'
            self.lastguess = self.input(c)
        return c != self.exitchar

    def __init__(self):
        RPSlib.__init__(self)


r = RPSgame()

while r.play():
    pass
