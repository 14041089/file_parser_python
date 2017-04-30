

class EnthalpyCoefficient:
    _FONCTION = "FONCTION"

    def __init__(self, enthalpyValue, coefficientStringList):
        self.enthalpyValue = enthalpyValue
        self.coefficientsList = []

        for line in coefficientStringList:
            self.coefficientsList += self.getCoefficientsFromLine(line)

        return

    def getCoefficientsFromLine(self, coefficientsLine):
        if (not coefficientsLine.startswith(self._FONCTION)):
            return coefficientsLine.split()

        return []

    def exportCoefficientsAsSingleLine(self, delimiter=" "):
        print("Export Coefficients As Single Line: " + str(self.coefficientsList))
        return delimiter.join(self.coefficientsList)