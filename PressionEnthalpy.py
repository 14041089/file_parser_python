from EnthalpyCoefficient import EnthalpyCoefficient


class PressionEnthalpy:
    _PRESSION_STRING = "*__Pression"
    _ENTHALPY_STRING = "*__Enthalpie"
    _GRILLE_PARTIELE = "GRILLE_PARTIELLE"
    _FONCTION = "FONCTION"
    _NEW_LINE = "\r\n"

    def __init__(self, listOfValues):
        self.lines = listOfValues
        self.pressionValues = []
        self.enthalpyValues = []
        self.coefficientValues = []

        # initialize all the values
        self._extractAllInfoFromStringList(listOfValues)
        self._cleanUpListValues()
        self._generateCoefficientValues()
        self.cleanCoefficients = self._generateCoefficientValues()

    def _generateCoefficientValues(self):
        resultingCoefficients = []
        coefficientAuxiliaries = []
        enthalpyValue = ""

        for line in self.coefficientValues:
            if (line.startswith("* ")):
                if (enthalpyValue != "") :
                    resultingCoefficients.append(EnthalpyCoefficient(enthalpyValue, coefficientAuxiliaries))
                    enthalpyValue = ""
                    coefficientAuxiliaries = []

                enthalpyValue = line[2:]
            else:
                coefficientAuxiliaries.append(line)

        return resultingCoefficients

    """
    Private function to check how many Partial Grids in the contents.
    """
    def _getPartialGridPositions(self, contentLines):
        partialGridPositions = []

        for index,line in enumerate(contentLines):
            if (line.startswith(self._GRILLE_PARTIELE)):
                partialGridPositions.append(index)

        return partialGridPositions

    def _parseCoefficientLines(self, postEnthalpyLines):
        partialGridPositions = self._getPartialGridPositions(postEnthalpyLines)

        if (len(partialGridPositions) == 0):
            return self._extractCoefficientsWithEnthalpy(postEnthalpyLines)

        partialGrids = []

        # for index, separator in enumerate(partialGridPositions):


    def _extractCoefficientsWithEnthalpy(self, coefficientStringList):
        _ENTHALPY_COEFFICIENT = "* "
        _ENTHALPY_LEN = len(_ENTHALPY_COEFFICIENT)
        enthalpyValue = ""
        coefficients = []
        coefficientList = []

        for line in coefficientStringList:
            if (line.startswith(_ENTHALPY_COEFFICIENT)):
                if (coefficients != []):
                    coefficientList.append(EnthalpyCoefficient(enthalpyValue, coefficients))
                    enthalpyValue = ""
                    coefficients = []

                enthalpyValue = line[_ENTHALPY_LEN:]
            else:
                coefficients.append(line)

        print("Coefficient extraction was a success, extracted " + str(len(coefficients)) + " from our lines.")
        return coefficientList

    def _extractAllInfoFromStringList(self, stringList):
        hasPressionAppeared = hasEnthalpyAppeared = hasPostEnthalpyNewLineAppeared = False

        for line in stringList:
            if (hasEnthalpyAppeared and line.strip() == ""):
                hasPostEnthalpyNewLineAppeared = True

            if hasPressionAppeared:
                if (hasEnthalpyAppeared):
                    if (hasPostEnthalpyNewLineAppeared):
                        self.coefficientValues.append(line)
                    else:
                        self.enthalpyValues.append(line)
                else:
                    self.pressionValues.append(line)

            if line.startswith(self._PRESSION_STRING):
                hasPressionAppeared = True

            if line.startswith(self._ENTHALPY_STRING):
                hasEnthalpyAppeared = True



    def _cleanUpListValues(self):
        cleanedPressionLines = []
        for pressionLine in self.pressionValues:
            if pressionLine.strip() != "" and self._PRESSION_STRING not in pressionLine \
                    and self._ENTHALPY_STRING not in pressionLine:
                cleanedPressionLines.append(pressionLine)

        self.pressionValues = cleanedPressionLines

        cleanedEnthalpyLines = []
        for enthalpyLine in self.enthalpyValues:
            if enthalpyLine.strip() != "" and self._PRESSION_STRING not in enthalpyLine \
                    and self._ENTHALPY_STRING not in enthalpyLine:
                cleanedEnthalpyLines.append(enthalpyLine)

        self.enthalpyValues = cleanedEnthalpyLines

        cleanedCoefficientLines = []
        for coefficientLine in self.coefficientValues:
            if coefficientLine.strip() != "" and self._PRESSION_STRING not in coefficientLine \
                    and self._ENTHALPY_STRING not in coefficientLine and self._FONCTION not in coefficientLine:
                cleanedCoefficientLines.append(coefficientLine)

        self.coefficientValues = cleanedCoefficientLines

    def exportPressionAndEnthalpyColumns(self):
        exportedString = " ".join(self.pressionValues) \
            + "\n" + " ".join(self.enthalpyValues)

        return exportedString

    def exportCoefficients(self, delimiter=" "):
        coefficientListOfStrings = []
        for coefficientValue in self.cleanCoefficients:
            coefficientListOfStrings.append(coefficientValue.exportCoefficientsAsSingleLine(delimiter))

        return coefficientListOfStrings