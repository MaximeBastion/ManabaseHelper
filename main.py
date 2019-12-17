from Deck import Deck
from NonBasicLand import *
from Settings import Settings
import os

appRunning = True

deck = Deck()

nLandsChosen = 0
nNonBasics = 0
nBasicsChosen = 0

# Save/Load
dirName = "Fetch Guides"


def main():
    print(ConsoleColors.OKGREEN + "\nWelcome to the Manabase Helper !")
    print("The code for entering colors follows : WUBRG -> [White, blUe, Black, Red, Green].")
    print("Example : to add a White/Blue land, type \'WU\' or \'wu\' and press enter.")

    if int(input(
            ConsoleColors.ENDC + "\nDo you want me to help you figure out how many lands you should play? (1/0) : ")) == 1:
        askAvgCmc()

    nLandsChosen = int(input(ConsoleColors.ENDC + "How many lands will you play? : "))
    nNonBasics = int(input("How many nonbasics do you play? : "))
    nBasicsChosen = nLandsChosen - nNonBasics
    print(ConsoleColors.OKBLUE + "Then you should play " + str(nBasicsChosen) + " basics.")

    printHeader("Color Symbols")
    cmd = input("Relevant colors: ").upper()
    deck.relevantColors = cmd
    print(ConsoleColors.OKBLUE + "Your color combination is : " + ColorsManager.getColorCombinationName(cmd))
    deck.nBasics = int(nBasicsChosen)
    askColorsCount()
    deck.colorsMatrix.compute(Settings.default)
    print(ConsoleColors.OKBLUE + "\nColors score : " + str(deck.colorsMatrix.result1))
    deck.colorsMatrix.compute2()
    # print(ConsoleColors.OKBLUE + "Colors proportion (%) : " + str(deck.colorsMatrix.result2 * 100))
    deck.colorsMatrix.printProportions()

    printHeader("Nonbasic Lands")
    landTypes = ["True Duals", "Shocklands", "Fetchlands", "Trilands"]
    inputSizes = [2, 2, 2, 3]
    for i, landType in enumerate(landTypes):
        inputSize: int = inputSizes[i]
        print(ConsoleColors.ENDC + "List " + landType)
        cmd: str = "N"
        while not cmdIsStop(cmd) and len(deck.nonBasics) < nNonBasics:
            cmd = "N"
            msg: str = str(len(deck.nonBasics) + 1) + "/" + str(nNonBasics) + " : "
            while not cmdIsStop(cmd) and len(cmd) != inputSize:
                cmd = input(msg)
            cmd = cmd.upper()
            if not cmdIsStop(cmd):
                if landType == "True Duals":
                    deck.nonBasics.append(NonBasicLand(cmd.upper()))
                elif landType == "Shocklands":
                    deck.nonBasics.append(NonBasicLand(cmd, False, True))
                elif landType == "Fetchlands":
                    deck.nonBasics.append(NonBasicLand(cmd, True))
                elif landType == "Trilands":
                    deck.nonBasics.append(NonBasicLand(cmd))

    if len(deck.nonBasics) < nNonBasics:
        print(ConsoleColors.ENDC + "How many rainbows do you have? (Mana Confluence, Evolving Wilds) : ")
        amount = int(input(str(len(deck.nonBasics) + 1) + "/" + str(nNonBasics) + " : "))
        for i in range(amount):
            deck.nonBasics.append(NonBasicLand("WUBRG"))

    printHeader("Mana Sources")
    print(ConsoleColors.OKBLUE + "Sources total : " + str(deck.getNManaSources()))
    print(ConsoleColors.OKBLUE + "Sources per color I have with nonbasics only : " + str(
        deck.getSourcesOfAllColorsNonbasics()))
    print(ConsoleColors.OKBLUE + "Sources per color I should have in total : " + str(deck.getNSourcesPerColor()))
    deck.checkExcessiveSources()

    printHeader("Basics to Use")
    print(ConsoleColors.OKBLUE + "Float : " + str(deck.getBasics()))
    print(ConsoleColors.OKBLUE + "\nInt :")
    ColorsManager.displayBasicsArray(deck.getBasicsInt())

    fetchGuide = deck.getFetchGuide()
    if len(fetchGuide) != 0:
        printHeader("Fetch Guide")
        print(fetchGuide)
        if int(input(ConsoleColors.ENDC + "Do you want to save it? (1/0) : ")) == 1:
            fileName = input("File name : ")
            saveTxt(fetchGuide, fileName)


def askColorsCount():  # For each relevant color, asks the number of mana symbol for 1 drops, 2 drops, 3 drops, 4 drops, and 5+ drops
    print(ConsoleColors.ENDC + "Sum of mana symbols for :")
    for color in deck.relevantColors:
        lastCmc = min(Settings.currentMaxCmc, 5)
        for cmc in range(1, lastCmc + 1):
            msg = ColorsManager.getNameFromSymbol(color) + " cards you want to play on turn " + str(
                cmc) + " : " if cmc < 5 \
                else ColorsManager.getNameFromSymbol(color) + " cards you want to play on turn 5+ : "
            value = input(msg).upper()
            deck.colorsMatrix.set(color, cmc, int(value))


def cmdIsStop(cmd):
    cmd = cmd.lower()
    return cmd == "" or cmd == " " or cmd == "stop" or cmd == "exit"


def printHeader(msg):
    print(ConsoleColors.HEADER + "\n----------------------" + msg + "----------------------" + ConsoleColors.ENDC)


def askAvgCmc():
    printHeader("How many lands should you run?")
    nSpells = int(input("How many nonlands do you want to play? : "))
    nManaHelpersLands = float(input(
        "How many lands do you think your nonland mana helpers count as ? (like 1/3 per mana producer, result in "
        "float) : "))
    maxCmc = int(input("What is your max CMC? : "))
    Settings.currentMaxCmc = maxCmc
    cmcSum = 0
    for i in range(maxCmc):
        cmc = i + 1
        cmcSum += int(input("How many cards do you cast of CMC : " + str(cmc) + " ? : ")) * cmc
    print(ConsoleColors.OKBLUE + "You total CMC is " + str(cmcSum))
    avgCmc = cmcSum / nSpells
    print(ConsoleColors.OKBLUE + "You average cmc is " + str(avgCmc))
    if avgCmc <= 0.8:
        nLands = 18
    elif avgCmc <= 1.12:
        nLands = 19
    elif avgCmc <= 1.44:
        nLands = 20
    elif avgCmc <= 1.76:
        nLands = 21
    elif avgCmc <= 2.08:
        nLands = 22
    elif avgCmc <= 2.4:
        nLands = 23
    elif avgCmc <= 2.72:
        nLands = 24
    elif avgCmc <= 3.04:
        nLands = 25
    elif avgCmc <= 3.36:
        nLands = 26
    elif avgCmc <= 3.68:
        nLands = 27
    else:
        print(ConsoleColors.WARNING + "Your average CMC is really high")
        nLands = 28
    print(ConsoleColors.OKBLUE + "Lands for constructed : " + str(nLands))
    nLands = (40 / 60) * nLands
    print(ConsoleColors.OKBLUE + "Lands for limited : " + str(round(nLands, 2) - nManaHelpersLands))


def saveTxt(msg, fileName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)
    path = dirName + "/"
    fullPath = path + fileName + ".txt"
    file = open(fullPath, 'w')
    file.write(msg)
    file.close()
    print(ConsoleColors.OKBLUE + "File has been saved here : " + os.getcwd() + "/" + fullPath + ConsoleColors.ENDC)


def loadTxt(fileName):
    path = dirName + "/"
    if not os.path.isdir(dirName) or not os.path.isfile(path + fileName + ".txt"):
        print(ConsoleColors.FAIL + " error while loading txt : dir or file does not exists" + ConsoleColors.ENDC)
        return ""
    file = open(path + fileName + ".txt", 'r')
    content = file.read()
    file.close()
    return content


main()
