from enum import Enum

from ColorsManager import ColorsManager, ConsoleColors


class nonBasicLandType(Enum):
    Undefined = 1
    Dual = 2
    Triland = 3
    Rainbow = 4


class NonBasicLand():
    colorsSymbols = "WUBRG"

    def __init__(self, colors, isFetch=False, isShock=False):
        self.colors = colors
        self.isFetch = isFetch
        self.isShock = isShock
        print(ConsoleColors.OKBLUE + self.getStr() + ConsoleColors.ENDC)

    def getName(self):
        nColors = len(self.colors)
        if nColors == 2:
            if "W" in self.colors:
                if "U" in self.colors:
                    if self.isFetch:
                        return "Flooded Strand"
                    else:
                        return "Hallowed Fountain" if self.isShock else "Tundra"
                if "B" in self.colors:
                    if self.isFetch:
                        return "Marsh Flats"
                    else:
                        return "Godless Shrine" if self.isShock else "Scrubland"
                if "R" in self.colors:
                    if self.isFetch:
                        return "Aris Mesa"
                    else:
                        return "Sacred Foundry" if self.isShock else "Plateau"
                if "G" in self.colors:
                    if self.isFetch:
                        return "Windswept Heath"
                    else:
                        return "Temple Garden" if self.isShock else "Savannah"
            if "U" in self.colors:
                if "B" in self.colors:
                    if self.isFetch:
                        return "Polluted Delta"
                    else:
                        return "Watery Grave" if self.isShock else "Underground Sea"
                if "R" in self.colors:
                    if self.isFetch:
                        return "Scalding Tarn"
                    else:
                        return "Steam Vents" if self.isShock else "Volcanic Island"
                if "G" in self.colors:
                    if self.isFetch:
                        return "Misty Rainforest"
                    else:
                        return "Breeding Pool" if self.isShock else "Tropical Island"
            if "B" in self.colors:
                if "R" in self.colors:
                    if self.isFetch:
                        return "Bloodstained Mire"
                    else:
                        return "Blood Crypt" if self.isShock else "Badlands"
                if "G" in self.colors:
                    if self.isFetch:
                        return "Verdant Catacombs"
                    else:
                        return "Overgrown Tomb" if self.isShock else "Bayou"
            if "R" in self.colors:
                if self.isFetch:
                    return "Wooded Foothills"
                else:
                    return "Stomping Ground" if self.isShock else "Taiga"
        if nColors == 3:
            if "W" in self.colors:
                if "U" in self.colors:
                    if "B" in self.colors:
                        return "Arcane Sanctum"
                    if "R" in self.colors:
                        return "Mystic Monastery"
                    return "Seaside Citadel"
                if "B" in self.colors:
                    if "R" in self.colors:
                        return "Nomad Outpost"
                    return "Sandsteppe Citadel"
                return "Jungle Shrine"
            if "U" in self.colors:
                if "B" in self.colors:
                    if "R" in self.colors:
                        return "Crimbling Necropolis"
                    return "Opulent Palace"
                return "Frontier Bivouac"
            return "Savage Lands"
        return "Rainbow"

    def getType(self):
        nColors = len(self.colors)
        output = nonBasicLandType.Undefined

        if nColors == 2:
            output = nonBasicLandType.Dual
        elif nColors == 3:
            output = nonBasicLandType.Triland
        elif nColors == 5:
            output = nonBasicLandType.Rainbow
        return output

    def canBeFetchedBy(self, fetch):
        return not self.isFetch and fetch.isFetch

    def aColorOverlaps(self, otherColors):
        # can be optimized by stopping at first match
        return len(self.getOverlappedColors(otherColors)) > 0

    def getOverlappedColors(self, otherColors):
        output = ""
        for symbol in NonBasicLand.colorsSymbols:
            if symbol in self.colors and symbol in otherColors:
                output += symbol
        return output

    # If I'm a fetch, returns the list a the colors I can access via a list of non-fetches
    def getFetchableColors(self, nonFetchList):
        colors = ""
        for e in nonFetchList:
            if e.getType() != nonBasicLandType.Dual:  # making sure that trilands are not fetchable
                continue
            overlappedColors = ColorsManager.getOverap(self.colors, e.colors)
            if overlappedColors != "":
                # can fetch, so I get all of his colors
                for color in e.colors:
                    if color not in colors:
                        colors += color
        return colors

    # returns which basics/nonbasics this fetch can get in the form of a list of nonbasics and a string of basics
    # symbols
    def getFetchables(self, nonFetchList, basicsList):
        fetchableNonbasics = []
        fetchableBasics = ""
        if not self.isFetch:
            return
        for e in nonFetchList:
            if e.getType() != nonBasicLandType.Dual:  # making sure that trilands are not fetchable
                continue
            overlappedColors = ColorsManager.getOverap(self.colors, e.colors)
            if overlappedColors != "":
                # can fetch
                fetchableNonbasics.append(e)
        for i, amount in enumerate(basicsList):
            currentColorSymbol = ColorsManager.colorsSymbol[i]
            for colorSymbol in self.colors:
                if colorSymbol == currentColorSymbol and amount >= 1:
                    # fetchable
                    fetchableBasics += currentColorSymbol
        return fetchableNonbasics, fetchableBasics

    def getFetchablesStr(self, fetchableNonbasics, fetchableBasics):
        msgLine1 = self.getStr() + ": "
        fetchableColors = ""
        msg = "\n"
        for nB in fetchableNonbasics:
            msg += "  - " + nB.getName() + " = "
            for colorS in nB.colors:
                msg += ColorsManager.getNameFromSymbol(colorS) + "/"
                if colorS not in fetchableColors:
                    fetchableColors += colorS
            msg = msg[:-1] + "\n"
        for cS in fetchableBasics:
            msg += "  - " + ColorsManager.getBasicNameFromIndex(ColorsManager.getIndex(cS), False) + "\n"
            if cS not in fetchableColors:
                fetchableColors += cS
        for c in fetchableColors:
            msgLine1 += ColorsManager.getBasicNameFromIndex(ColorsManager.getIndex(c), False) + ", "
        msgLine1 = msgLine1[:-2] + " = " + ColorsManager.getColorCombinationName(fetchableColors)
        return msgLine1 + msg[:-1]

    def getStr(self):
        return self.getName() + " - " + ColorsManager.getColorCombinationName(self.colors)
