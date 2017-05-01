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

        self.pressionListOfValues = []
        self.enthalpyListOfValues = []
        self.coefficientListOfValues = []

        # Check if it has partial Grids or Not.
        self.hasPartialGrids = (self._getFirstPositionFor(self.lines, self._GRILLE_PARTIELE) != -1 or \
                                self._getFirstPositionFor(self.lines, "* ") != -1)

        # initialize all the values
        self._extractAllInfoFromStringList(listOfValues)

        # Extract Pression Vaues
        self.pressionValues = self._getIndividualValuesFromListOfLines(self.pressionValues)

        # Extract and Trim Enthalpie Values
        self.enthalpyValues = self._getIndividualValuesFromListOfLines(self.enthalpyValues)

        # Check if there are multiple grids or not.
        if (self.hasPartialGrids):
            self.enthalpyListOfValues.append(self.enthalpyValues)
            self.pressionListOfValues.append(self.pressionValues)
            self.coefficientValues = self._rearrangePartialGrids(self.coefficientValues)

        else:
            # Clean up the Coefficient Values when there is no Partial Grids.
            self.coefficientValues = self._getCoefficientsOfNonPartialGridFunction(self.coefficientValues)

    def _isStringNotStartingWithConstOrWhiteSpace(self, stringOfText):
        return stringOfText.strip() != "" and not stringOfText.startswith(self._FONCTION) \
               and not stringOfText.startswith(self._PRESSION_STRING) and not stringOfText.startswith(self._ENTHALPY_STRING) \
               and not stringOfText.startswith(self._GRILLE_PARTIELE)

    def _getIndividualValuesFromListOfLines(self, listOfLines):
        resultingList = []
        for line in listOfLines:
            if (self._isStringNotStartingWithConstOrWhiteSpace(line)):
                resultingList += line.strip().split()

        return resultingList

    # def _getEnthalpyCoefficients(self, linesOfCoefficients):
    #     coefficientObjList = []
    #     coefficientEnthalpyCorrespondingValue = ""
    #     coefficientValues = []
    #
    #     for line in linesOfCoefficients:
    #         if (coefficientEnthalpyCorrespondingValue != "" and)

    def _getCoefficientsOfNonPartialGridFunction(self, listOfCoefficientLines):
        resultingCoefficientValueList = []
        for coefficientLine in listOfCoefficientLines:
            if (coefficientLine.strip() != "" and not coefficientLine.startswith(self._FONCTION) \
                        and not coefficientLine.startswith(self._ENTHALPY_STRING) \
                        and not coefficientLine.startswith(self._PRESSION_STRING)):
                resultingCoefficientValueList += coefficientLine.strip().split()

        return resultingCoefficientValueList

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

        compensation = self._getFirstPositionFor(coefficientStringList, _ENTHALPY_COEFFICIENT)
        if compensation == -1:
            compensation = 0

        for line in coefficientStringList[compensation:]:
            if ((line.startswith(_ENTHALPY_COEFFICIENT) and line != _ENTHALPY_COEFFICIENT + enthalpyValue) or \
                line.startswith(self._FONCTION) or line.strip() == ""):
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

    # def _getIndividualValuesFromString(self, listOfValues):
    #     resultingList = []
    #     for el in listOfValues:
    #         resultingList += el.split()
    #
    #     return resultingList

    def _rearrangePartialGrids(self, coefficientValues):
        partialGrids = self._getPartialGridPositions(coefficientValues)

        coeffiecientsList = []

        if (len(partialGrids) == 0):
            coefficientList = self._extractCoefficientsWithEnthalpy(coefficientValues)
            self.coefficientListOfValues.append(coefficientList)
            return coefficientList

        pressionList = []
        enthalpyList = []
        temporaryEnthalpyValues = []
        temporaryPressionValues = []
        temporaryCoefficientValues = []

        pressionValuePosition = 0
        enthalpyValuePosition = 0
        postEnthalpyValuePosition = 0
        endOfCoefValuesPosition = 0

        # Extract the first line
        self.cleanCoefficientValueList = self._extractCoefficientsWithEnthalpy(coefficientValues[:partialGrids[0]])
        temporaryCoefficientValues = self.cleanCoefficientValueList

        self.cleanCoefficientValueList = self.cleanCoefficientValueList[-1 * len(self.pressionValues):]

        # self.pressionListOfValues.append(self.pressionValues)
        # self.enthalpyListOfValues.append(self.enthalpyListOfValues)
        self.coefficientListOfValues.append(temporaryCoefficientValues)

        temporaryCoefficientValues = []

        auxiliaryCompensation = 0
        # Extract Subsequent Lines
        for grilleStartingIndex in partialGrids:
            pressionValuePosition = self._getFirstPositionFor(coefficientValues[grilleStartingIndex:], self._PRESSION_STRING) + grilleStartingIndex
            enthalpyValuePosition = self._getFirstPositionFor(coefficientValues[grilleStartingIndex:], self._ENTHALPY_STRING) + grilleStartingIndex
            postEnthalpyValuePosition = self._getFirstPositionFor(coefficientValues[enthalpyValuePosition:], "* ") \
                + enthalpyValuePosition
            endOfCoefValuesPosition = self._getFirstPositionFor(coefficientValues[postEnthalpyValuePosition:], \
                                                                self._NEW_LINE) + postEnthalpyValuePosition

            pressionList = coefficientValues[pressionValuePosition:enthalpyValuePosition]
            enthalpyList = coefficientValues[enthalpyValuePosition:postEnthalpyValuePosition]
            coeffiecientsList = coefficientValues[postEnthalpyValuePosition:endOfCoefValuesPosition]

            temporaryPressionValues = self._getIndividualValuesFromListOfLines(pressionList)
            temporaryEnthalpyValues = self._getIndividualValuesFromListOfLines(enthalpyList)

            if len(temporaryEnthalpyValues) > len(temporaryPressionValues):
                auxiliaryCompensation = -1 * len(temporaryPressionValues)
                self.enthalpyValues += temporaryEnthalpyValues[auxiliaryCompensation:]
            else:
                self.enthalpyValues += temporaryEnthalpyValues
                auxiliaryCompensation = 0

            self.pressionValues += temporaryPressionValues

            temporaryCoefficientValues = self._extractCoefficientsWithEnthalpy(coeffiecientsList)
            self.cleanCoefficientValueList += temporaryCoefficientValues[auxiliaryCompensation:]

            self.pressionListOfValues.append(temporaryPressionValues)
            self.enthalpyListOfValues.append(temporaryEnthalpyValues)
            self.coefficientListOfValues.append(temporaryCoefficientValues)

        return self.cleanCoefficientValueList


    def _getFirstPositionFor(self, listOfContents, startingConstString):
        for index, line in enumerate(listOfContents):
            if line.startswith(startingConstString):
                return index

        return -1

    # def _cleanUpListValues(self):
    #     cleanedPressionLines = []
    #
    #     for pressionLine in self.pressionValues:
    #         if pressionLine.strip() != "" and self._PRESSION_STRING not in pressionLine \
    #                 and self._ENTHALPY_STRING not in pressionLine:
    #             cleanedPressionLines.append(pressionLine)
    #
    #     self.pressionValues = cleanedPressionLines
    #     self.pressionValues = self._getIndividualValuesFromString(self.pressionValues)
    #
    #     cleanedEnthalpyLines = []
    #     for enthalpyLine in self.enthalpyValues:
    #         if enthalpyLine.strip() != "" and self._PRESSION_STRING not in enthalpyLine \
    #                 and self._ENTHALPY_STRING not in enthalpyLine:
    #             cleanedEnthalpyLines.append(enthalpyLine)
    #
    #     self.enthalpyValues = cleanedEnthalpyLines
    #     self.enthalpyValues = self._getIndividualValuesFromString(self.enthalpyValues)
    #
    #     cleanedCoefficientLines = []
    #     for coefficientLine in self.coefficientValues:
    #         if coefficientLine.strip() != "" and self._PRESSION_STRING not in coefficientLine \
    #                 and self._ENTHALPY_STRING not in coefficientLine and self._FONCTION not in coefficientLine:
    #             cleanedCoefficientLines.append(coefficientLine)
    #
    #     self.coefficientValues = cleanedCoefficientLines
    #     #self.coefficientValues = self._getIndividualValuesFromString(self.coefficientValues)

    def exportPressionAndEnthalpyColumns(self):
        exportedString = " ".join(self.pressionValues) \
            + "\n" + " ".join(self.enthalpyValues)

        return exportedString

    def exportCoefficients(self, delimiter=" "):
        coefficientListOfStrings = []
        if (self.hasPartialGrids):
            for coefficientValue in self.coefficientValues:
                coefficientListOfStrings.append(coefficientValue.exportCoefficientsAsSingleLine(delimiter))
        else:
            coefficientListOfStrings.append(delimiter.join(self.coefficientValues))

        return coefficientListOfStrings

    def exportDistinctValuesBasedOnPression(self, delimiter=" "):
        distinctPressionList = []
        distinctEnthalpyList = []
        distinctCoefficientList = []

        if (not self.hasPartialGrids):
            return self.exportPressionAndEnthalpyColumns(), self.exportCoefficients(delimiter)

        for index, pressionValue in enumerate(self.pressionValues):
            if not pressionValue in distinctPressionList:
                distinctPressionList.append(pressionValue)
                distinctEnthalpyList.append(self.enthalpyValues[index])
                distinctCoefficientList.append(self.coefficientValues[index])

        exportedPressionEnthalpyMultilineString = delimiter.join(distinctPressionList) + "\n" + \
            delimiter.join(distinctEnthalpyList)
        resultingCoefficientList = self.getExportReadyCoefficientList(distinctCoefficientList, delimiter)

        return exportedPressionEnthalpyMultilineString, resultingCoefficientList

    def getExportReadyCoefficientList(self, coefficientValues, delimiter=" "):
        coefficientListOfStrings = []
        if (self.hasPartialGrids):
            for coefficientValue in coefficientValues:
                coefficientListOfStrings.append(coefficientValue.exportCoefficientsAsSingleLine(delimiter))
        else:
            coefficientListOfStrings.append(delimiter.join(coefficientValues))

        return coefficientListOfStrings

    def toStringOfListTrio(self, pressionValues, enthalpyValues, coefficientValues, delimiter=" ", assumeListsOfLists=True):
        resultingCoefficientLines = []
        stringForPressionAndEnthalpy = delimiter.join(pressionValues) + "\n" + \
            delimiter.join(enthalpyValues)

        if (assumeListsOfLists):
            for coefficient in coefficientValues:
                resultingCoefficientLines.append(coefficient.exportCoefficientsAsSingleLine(delimiter))
        else:
            resultingCoefficientLines.append(delimiter.join(coefficientValues))

        return stringForPressionAndEnthalpy, resultingCoefficientLines