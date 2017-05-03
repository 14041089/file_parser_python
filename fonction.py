from EnthalpyCoefficient import EnthalpyCoefficient


class Fonction:
    _FONCTION = "FONCTION"
    _GRILLE_PARTIELLE = "GRILLE_PARTIELLE"
    _PRESSION = "*__Pression"
    _ENTHALPIE = "*__Enthalpie"
    _SCALE = "*scale_"
    _ENTHALPY_COEFFICIENT = "* "

    def __init__(self, functionLines, outputFileName, functionNumber):
        self.FunctionNumber = functionNumber
        self.OutputFileName = outputFileName
        self.NumberOfGrids = self._getNumberOfGrids(functionLines) # Gets the number of partial grids.
        self.HasMultipleGrids = self.NumberOfGrids > 1 # Checks if there are more than one partial grid.
        self.HasCoefficients = False
        self.pressionList = []
        self.enthalpieList = []
        self.coefficientList = []

        if (self.HasMultipleGrids):
            self.HasCoefficients = True # Mark that the object has coefficients for enthalpie values
            self._parseMultipleGrids(functionLines)

        else:
            self._parseSingleGrid(functionLines)

    def _parseMultipleGrids(self, functionLines):
        # Extract Positions for "Pression", "Enthalpie" and Coefficients
        pressionConstPositions = self.getPositionsOfPattern(functionLines, self._PRESSION)
        enthalpieConstPositions = self.getPositionsOfPattern(functionLines, self._ENTHALPIE)
        # TODO: Get Coefficient Positions (Check if this method is good enough!!!)
        coefficientPositions = self._extractTuplesContainingCoefficientBeginAndEnd(functionLines)

        # Signal an uneveness of Pression, Enthalpie and Coefficient lengths they should be the same!
        if not (len(pressionConstPositions) == len(enthalpieConstPositions) and \
                    (len(enthalpieConstPositions) == len(coefficientPositions))):
            print("FONCTION No." + str(self.FunctionNumber) + \
                  " has different amounts of Pression, Enthalpie and Coefficients")
            print(" -> Pression length:     " + str(len(pressionConstPositions)))
            print(" -> Enthalpie length:    " + str(len(enthalpieConstPositions)))
            print(" -> Coefficients length: " + str(len(coefficientPositions)))

        # TODO: for every interval between pression and enthalpy position extract Pression List of Values
        # TODO: Add Pression List of Values to the general list of values
        for index, pressionPosition in pressionConstPositions:
            # TODO: Get pression values between *__Pression and *__Enthalpie
            # FIXME: Add a function to extract the individual values:
            functionLines[pressionPosition: enthalpieConstPositions[index]]

        # TODO: for every interval between enthalpy and coefficient position extract Enthalpie List of Values
        # TODO: Add Enthalpie List of Values to the general list of values
        for index, enthalpiePosition in enthalpieConstPositions:
            functionLines[enthalpiePosition:coefficientPositions[index][0]] # 0 because we want the start of the coefficients

        # TODO: for every interval between coefficient and the next empty line extract Coefficient List of Values
        # TODO: Add Coefficient List of Objects to the general list of values
        for coefficientStart, coefficientEnd in coefficientPositions:
            functionLines[coefficientStart:coefficientEnd]

        return

    """
    Method that extracts the coefficients which start with "* " and ends when there's a blank line.
    """
    def _extractTuplesContainingCoefficientBeginAndEnd(self, functionLines):
        resultingListOfTuples = []
        hasCoefficientBegan = False
        auxStartOfCoefficientsIndex = 0
        for index,line in enumerate(functionLines):
            if line.startswith(self._ENTHALPY_COEFFICIENT) and not hasCoefficientBegan:
                hasCoefficientBegan = True
                auxStartOfCoefficientsIndex = index

            if line.strip() == "" and hasCoefficientBegan:
                hasCoefficientBegan = False
                resultingListOfTuples.append((auxStartOfCoefficientsIndex, index))

        return resultingListOfTuples



    def _parseSingleGrid(self, functionLines):
        # TODO: Make methods to extract pression, enthalpie and coefficients
        pressionPositions = self.getPositionsOfPattern(functionLines, self._PRESSION)
        enthalpiePositions = self.getPositionsOfPattern(functionLines, self._ENTHALPIE)
        coefficientStartPositions = self.getPositionsOfPattern(functionLines, self._ENTHALPY_COEFFICIENT)

        # For the Case Where there are no Coefficients
        if coefficientStartPositions == []:
            coefficientStartPositions = self.getPositionsOfPattern(functionLines[enthalpiePositions[0]:], "\n")
            if coefficientStartPositions != []:
                for index,coeffPosition in enumerate(coefficientStartPositions):
                    coefficientStartPositions[index] += enthalpiePositions[0]

        pressionListOfLines = functionLines[pressionPositions[0]:enthalpiePositions[0]]
        enthalpyListOfLines = functionLines[enthalpiePositions[0]:coefficientStartPositions[0]]
        coefficientListOfLines = functionLines[coefficientStartPositions[0]:]

        self.pressionList.append(self._getPressionFromLines(pressionListOfLines))
        self.enthalpieList.append(self._getPressionFromLines(enthalpyListOfLines))
        if (self._getFirstOccurenceOf(coefficientListOfLines, self._ENTHALPY_COEFFICIENT) == -1):
            # This is a case where there is kind of no "Ro" but they will be printed in a single line
            self.coefficientList.append(self._getPressionFromLines(coefficientListOfLines))
        else:
            self.coefficientList.append(self._extractCoefficientsWithEnthalpy(coefficientListOfLines))
            self.HasCoefficients = True  # Mark that the object has coefficients for enthalpie values



    def _getPressionFromLines(self, pressionLines):
        resultingPressionList = []

        for line in pressionLines:
            if not (line.startswith(self._PRESSION) or line.startswith(self._ENTHALPIE) \
                            or line.startswith(self._FONCTION) or line.strip == ""):
                resultingPressionList += line.strip().split()

        return resultingPressionList

    def _getFirstOccurenceOf(self, stringLines, patternToMatch):

        for index, line in enumerate(stringLines):
            if (line.startswith(patternToMatch)):
                return index
        return -1

    def _extractCoefficientsWithEnthalpy(self, coefficientStringList):
        _ENTHALPY_LEN = len(self._ENTHALPY_COEFFICIENT)
        enthalpyValue = ""
        coefficients = []
        coefficientList = []

        # compensation = self._getFirstPositionFor(coefficientStringList, self._ENTHALPY_COEFFICIENT)
        # if compensation == -1:
        #     compensation = 0

        for line in coefficientStringList:
            if ((line.startswith(self._ENTHALPY_COEFFICIENT) and line != self._ENTHALPY_COEFFICIENT + enthalpyValue) or \
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

    """
    Retrives the number of GRILLE_PARTIELLE occurences in given list of strings.
    """
    def _getNumberOfGrids(self, functionLines):
        gridCount = 0

        for line in functionLines:
            if (line.startswith(self._GRILLE_PARTIELLE)):
                gridCount += 1

        return gridCount

    """
    Retrieves the position of all GRILLE_PARTIELLE occurences as well as the last line
    """
    def getGrillePositionsAndEndPosition(self, functionLines):
        resultingGrillePositions = []

        for index,line in enumerate(functionLines):
            if line.startswith(self._GRILLE_PARTIELLE):
                resultingGrillePositions.append(index)

        # Add the last line for closure.
        resultingGrillePositions.append(len(functionLines))
        return resultingGrillePositions

    """
    Retrieves the positions of lines, in functionLines list, that start with the matchingPattern
    """
    def getPositionsOfPattern(self, functionLines, matchingPattern):
        resultingPositions = []
        for index,line in enumerate(functionLines):
            if (line.startswith(matchingPattern) or line.strip().startswith(matchingPattern)):
                resultingPositions.append(index)
        return resultingPositions

    """
    Exports lisf of strings as a single string separated by a delimiter.
    """
    def exportListAsString(self, listOfValues, delimiter=" "):
        if listOfValues == None or len(listOfValues) == 0:
            return ""
        return delimiter.join(listOfValues)