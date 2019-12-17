from ColorsManager import ColorsManager


class ColorsMatrix:

    def __init__(self):
        """
           1  2  3  4  5+
        W
        U
        B
        R
        G
        """
        self.matrix = [[0 for i in range(5)] for j in range(5)]
        self.result1 = [0 for i in range(5)]
        self.result2 = [0 for i in range(5)]
        self.result3 = [0 for i in range(5)]

    def set(self, color, cmc, value):
        self.matrix[ColorsManager.getIndex(color)][cmc - 1] = value

    def get(self, color, cmc):
        return self.matrix[ColorsManager.getIndex(color)][cmc - 1]

    def printMatrix(self):
        msg = ""
        for x in range(5):
            msg += "\n"
            for y in range(5):
                msg += "  " + str(self.matrix[x][y])
        print(msg)

    def compute(self, settings):  # settings = [5, 4, 3, 2, 1]
        self.result1 = [0 for i in range(5)]
        for colorI in range(5):
            sum = 0
            for cmc in range(1, 6):
                sum += self.matrix[colorI][cmc - 1] * settings[cmc - 1]
            self.result1[colorI] = sum

    def compute2(self):
        for i in range(5):
            self.result2[i] = self.result1[i] / sum(self.result1)

    def printProportions(self):
        msg = "Color proportions : "
        for i, x in enumerate(self.result2):
            if x > 0.001:
                colorName = ColorsManager.getNameFromIndex(i)
                msg += str(int(x * 100)) + "% " + colorName + ", "
        print(msg[:-2])
