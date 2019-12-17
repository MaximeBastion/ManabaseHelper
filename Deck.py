from ColorsMatrix import ColorsMatrix
from NonBasicLand import *


class Deck:

    def __init__(self):
        self.nonBasics = []
        self.settings = ""
        self.relevantColors = ""
        self.nBasics = 0
        self.nManaSources = 0
        self.colorsMatrix = ColorsMatrix()
        self.sourcesPerColor = []
        self.sourcesPerColorNonbasics = []
        self.basics = []
        self.basicsInt = [0 for i in range(5)]

    def getFetches(self):
        output = []
        for e in self.nonBasics:
            if e.isFetch:
                output.append(e)
        return output

    def getNonFetches(self):
        output = []
        for e in self.nonBasics:
            if not e.isFetch:
                output.append(e)
        return output

    def getNManaSources(self):
        fetches = self.getFetches()
        nonFetches = self.getNonFetches()
        count = 0

        for nF in nonFetches:
            count += len(self.getOverlappedColors(self.relevantColors, nF.colors))

        print(ConsoleColors.OKBLUE + "Sources with nonfetches : " + str(count))
        nSourcesFetches = count
        for f in fetches:
            fColors = f.getFetchableColors(nonFetches)
            count += len(self.getOverlappedColors(self.relevantColors, fColors))
        print(ConsoleColors.OKBLUE + "Sources with fetches : " + str(count - nSourcesFetches))
        self.nManaSources = count + self.nBasics
        return count + self.nBasics

    @staticmethod
    def getOverlappedColors(colors, otherColors):
        output = ""
        for symbol in NonBasicLand.colorsSymbols:
            if symbol in colors and symbol in otherColors:
                output += symbol
        return output

    def getNSourcesPerColor(self):
        output = [0 for i in range(5)]
        for i in range(5):
            output[i] = self.colorsMatrix.result2[i] * self.nManaSources
        self.sourcesPerColor = output
        return output

    def getBasics(self):
        output = [0 for i in range(5)]
        for i, color in enumerate(ColorsManager.colorsSymbol):
            if color in self.relevantColors:
                sourcesNeeded = self.sourcesPerColor[i] - self.getSourcesOfColor(color)
                if sourcesNeeded < 0:
                    sourcesNeeded = 0
                if sourcesNeeded > self.nBasics:
                    sourcesNeeded = self.nBasics
                output[i] = sourcesNeeded
        self.basics = output
        return output

    def getSourcesOfColor(self, color):  # with nonbasics exclusively
        fetches = self.getFetches()
        nonFetches = self.getNonFetches()
        count = 0

        for nF in nonFetches:
            if color in nF.colors:
                count += 1
        for f in fetches:
            fColors = f.getFetchableColors(nonFetches)
            if color in fColors:
                count += 1
        # print("Found " + str(count) + " sources for " + color)
        return count

    def getSourcesOfAllColorsNonbasics(self):
        output = [0 for i in range(5)]
        for i, color in enumerate(ColorsManager.colorsSymbol):
            if color not in self.relevantColors:
                output[i] = 0
            else:
                output[i] = self.getSourcesOfColor(color)
        self.sourcesPerColorNonbasics = output
        return output

    def checkExcessiveSources(
            self):  # displays a warning if nonbasics provide more sources than needed for certain colors
        for i in range(5):
            if ColorsManager.colorsSymbol[i] in self.relevantColors:
                excess = self.sourcesPerColorNonbasics[i] - self.sourcesPerColor[i]
                if excess > 0:
                    print(ConsoleColors.WARNING + "Nonbasics provide " + str(excess) + " more "
                          + ColorsManager.colorNames[i] + " sources than needed.")

    def getBasicsInt(self):
        self.basicsInt = [0 for i in range(5)]
        for i, x in enumerate(self.basics):
            self.basicsInt[i] = x
        while self.getSumOfIntParts(self.basicsInt) < self.nBasics:
            upIndex = self.getCloserToNextIntIndex(self.basicsInt)
            # print("Up index : " + str(upIndex))
            self.basicsInt[upIndex] = int(self.basicsInt[upIndex] + 1)
            # self.basicsInt[upIndex] = math.ceil(self.basicsInt[upIndex])
        for i, x in enumerate(self.basicsInt):
            self.basicsInt[i] = int(x)
        return self.basicsInt

    @staticmethod
    def getSumOfIntParts(arrayFloats):  # helps to get the mini n of basics of each color
        # print("getting sum on " + str(arrayFloats))
        sum = 0
        for x in arrayFloats:
            if int(x) > 0:
                sum += int(x)
        return sum

    @staticmethod
    def getCloserToNextIntIndex(arrayFloats):
        output = 0
        maxDecimal = 0.000000001
        for i, x in enumerate(arrayFloats):
            if x > 0 and x - int(x) > maxDecimal:
                output = i
                maxDecimal = x - int(x)
        if maxDecimal == 0.000000001:
            print(ConsoleColors.WARNING + "This basic is added in an arbitrary"
                                          " color as none of the colors need more "
                                          "mana than the other = all values are int")
        return output

    def getFetchGuide(self):
        msg = ""
        for fetch in self.getFetches():
            a, b = fetch.getFetchables(self.getNonFetches(), self.basicsInt)
            msg += fetch.getFetchablesStr(a, b) + "\n"
        return msg[:-1]
