class ColorsManager:
    colorsSymbol = "WUBRG"
    colorNames = ["White", "Blue", "Black", "Red", "Green"]
    basicNames = ["Plains", "Island", "Swamp", "Mountain", "Forest"]

    @staticmethod
    def getOverap(color1, color2):
        output = ""
        for symbol in ColorsManager.colorsSymbol:
            if symbol in color1 and symbol in color2:
                output += symbol
        return output

    @staticmethod
    def getIndex(symbol):  # W = 0, U = 1 ...
        for i, color in enumerate(ColorsManager.colorsSymbol):
            if symbol.upper() == color.upper():
                return i

    @staticmethod
    def getNameFromSymbol(symbol):
        for i, s in enumerate(ColorsManager.colorsSymbol):
            if symbol.upper() == s:
                return ColorsManager.colorNames[i]
        return "SymbolUnknown"

    @staticmethod
    def getNameFromIndex(index):
        return ColorsManager.colorNames[index]

    @staticmethod
    def getBasicNameFromIndex(index, plural=True):
        singular = ColorsManager.basicNames[index]
        if plural and singular[-1] != "s":
            singular += "s"
        return singular

    @staticmethod
    def displayBasicsArray(arrayOfInt,
                           style=2):  # takes the list of basics in int like [1, 0, 6, 2, 0] and displays it in a
        # better way
        for i, amount in enumerate(arrayOfInt):
            if amount > 0:
                if style == 1:
                    print(ColorsManager.getBasicNameFromIndex(i, amount > 1) + " : " + str(amount))
                elif style == 2:
                    print(str(amount) + " " + ColorsManager.getBasicNameFromIndex(i, amount > 1))

    @staticmethod
    def getColorCombinationName(colors):
        nColors = len(colors)
        if nColors == 2:
            if "W" in colors:
                if "U" in colors:
                    return "Azorius"
                if "B" in colors:
                    return "Orzhov"
                if "R" in colors:
                    return "Boros"
                if "G" in colors:
                    return "Selesnya"
            if "U" in colors:
                if "B" in colors:
                    return "Dimir"
                if "R" in colors:
                    return "Izzet"
                if "G" in colors:
                    return "Simic"
            if "B" in colors:
                if "R" in colors:
                    return "Rakdos"
                if "G" in colors:
                    return "Golgari"
            if "R" in colors:
                return "Gruul"
        if nColors == 3:
            if "W" in colors:
                if "U" in colors:
                    if "B" in colors:
                        return "Esper"
                    if "R" in colors:
                        return "Jeskai"
                    return "Bant"
                if "B" in colors:
                    if "R" in colors:
                        return "Mardu"
                    return "Abzan"
                return "Naya"
            if "U" in colors:
                if "B" in colors:
                    if "R" in colors:
                        return "Grixis"
                    return "Sultai"
                return "Temur"
            return "Jund"
        if nColors == 4:
            if "W" not in colors:
                return "Glint"
            if "U" not in colors:
                return "Dune"
            if "B" not in colors:
                return "Ink"
            if "R" not in colors:
                return "Witch"
            return "Yore"
        return "Rainbow"


class ConsoleColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
