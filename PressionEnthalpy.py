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
        self.cleanCoefficientValueList = []

        # initialize all the values
        self._extractAllInfoFromStringList(listOfValues)
        self._rearrangePartialGrids()
        self.coefficientValues = self.cleanCoefficientValueList
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

    def _getIndividualValuesFromString(self, listOfValues):
        resultingList = []
        for el in listOfValues:
            resultingList += el.split()

        return resultingList

    def _rearrangePartialGrids(self):
        partialGrids = self._getPartialGridPositions(self.coefficientValues)

        if (len(partialGrids) == 0):
            return self.coefficientValues

        coeffiecientsList = []
        pressionList = []
        enthalpyList = []

        pressionValuePosition = 0
        enthalpyValuePosition = 0
        postEnthalpyValuePosition = 0
        endOfCoefValuesPosition = 0

        for grilleStartingIndex in partialGrids:
            pressionValuePosition = self._getFirstPositionFor(self.coefficientValues, self._PRESSION_STRING)
            enthalpyValuePosition = self._getFirstPositionFor(self.coefficientValues, self._ENTHALPY_STRING)
            postEnthalpyValuePosition = self._getFirstPositionFor(self.coefficientValues[enthalpyValuePosition:], "* ") \
                + enthalpyValuePosition
            endOfCoefValuesPosition = self._getFirstPositionFor(self.coefficientValues[postEnthalpyValuePosition:], \
                                                                self._NEW_LINE) + postEnthalpyValuePosition

            pressionList = self.coefficientValues[pressionValuePosition:enthalpyValuePosition]
            enthalpyList = self.coefficientValues[enthalpyValuePosition:postEnthalpyValuePosition]
            coeffiecientsList = self.coefficientValues[postEnthalpyValuePosition:endOfCoefValuesPosition]

            self.pressionValues += pressionList
            self.enthalpyValues += enthalpyList
            self.cleanCoefficientValueList += coeffiecientsList


    def _getFirstPositionFor(self, listOfContents, startingConstString):
        for index, line in enumerate(listOfContents):
            if line.startswith(startingConstString):
                return index

        return -1

    def _cleanUpListValues(self):
        cleanedPressionLines = []

        for pressionLine in self.pressionValues:
            if pressionLine.strip() != "" and self._PRESSION_STRING not in pressionLine \
                    and self._ENTHALPY_STRING not in pressionLine:
                cleanedPressionLines.append(pressionLine)

        self.pressionValues = cleanedPressionLines
        self.pressionValues = self._getIndividualValuesFromString(self.pressionValues)

        cleanedEnthalpyLines = []
        for enthalpyLine in self.enthalpyValues:
            if enthalpyLine.strip() != "" and self._PRESSION_STRING not in enthalpyLine \
                    and self._ENTHALPY_STRING not in enthalpyLine:
                cleanedEnthalpyLines.append(enthalpyLine)

        self.enthalpyValues = cleanedEnthalpyLines
        self.enthalpyValues = self._getIndividualValuesFromString(self.enthalpyValues)

        cleanedCoefficientLines = []
        for coefficientLine in self.coefficientValues:
            if coefficientLine.strip() != "" and self._PRESSION_STRING not in coefficientLine \
                    and self._ENTHALPY_STRING not in coefficientLine and self._FONCTION not in coefficientLine:
                cleanedCoefficientLines.append(coefficientLine)

        self.coefficientValues = cleanedCoefficientLines
        #self.coefficientValues = self._getIndividualValuesFromString(self.coefficientValues)

    def exportPressionAndEnthalpyColumns(self):
        exportedString = " ".join(self.pressionValues) \
            + "\n" + " ".join(self.enthalpyValues)

        return exportedString

    def exportCoefficients(self, delimiter=" "):
        coefficientListOfStrings = []
        for coefficientValue in self.cleanCoefficients:
            coefficientListOfStrings.append(coefficientValue.exportCoefficientsAsSingleLine(delimiter))

        return coefficientListOfStrings