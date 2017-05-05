from EnthalpyCoefficient import EnthalpyCoefficient
from PressionEnthalpy import PressionEnthalpy
from fonction import Fonction

pressionString = "*__Pression"
enthalpyString = "*__Enthalpie"
scaleInitialPattern = "*scale"
maillageP = "MAILLAGE_P"
fonctionString = "FONCTION"
grillePartialleString = "GRILLE_PARTIELLE"
finCFETAT = "FIN_CFETAT"

def extractMatrixFromFile(filename) :
    hasScaleAppeared = False
    hasPressionAppeared = False
    hasEnthalpyAppeared = False

    numberOfOutputs = 0
    matrixLines = []
    fileMatrixes = []
    with open(filename, "r") as matrixFile:
        for line in matrixFile:
            if (line.startswith(scaleInitialPattern)):
                hasScaleAppeared = True

            if (line.startswith(pressionString)) :
                hasPressionAppeared = True

            if (line.startswith(enthalpyString)) :
                hasEnthalpyAppeared = True

            if (hasScaleAppeared):
                matrixLines.append(line)

            if (line.strip().startswith(maillageP) or line.strip().startswith(fonctionString) or line.strip().startswith(finCFETAT)):
                hasScaleAppeared = hasEnthalpyAppeared = hasPressionAppeared = False
                numberOfOutputs += 1
                fileMatrixes.append(matrixLines[1:])
                print("New Matrix --------------" + str(len(fileMatrixes)))
                print(matrixLines)
                matrixLines = []

    return cleanUpMatrixList(fileMatrixes)

def cleanUpMatrixList(fileMatrixes) :
    cleanedFileMatrix = []
    for matrix in fileMatrixes:
        if (not len(matrix) == 0) :
            cleanedFileMatrix.append(matrix)

    return cleanedFileMatrix

def getMatrixAfterSplit(matrixAfterSplit) :
    resultingMatrix = []
    hasScaleAppeared = False
    for line in matrixAfterSplit :
        if hasScaleAppeared:
            resultingMatrix.append(line)

        if line.strip().startswith(scaleInitialPattern):
            hasScaleAppeared = True

    return resultingMatrix

def checkIfFunctionsGotMixed(singleFileMatrix) :
    for lineNumber in range(len(singleFileMatrix)):
        if (singleFileMatrix[lineNumber].strip().startswith(grillePartialleString)):
            return lineNumber

    return -1

def separateMatrixes(listOfLines):
    firstMatrix = []
    secondMatrix = []

    firstMatrixLines = getNumberOfValuesInMatrixText(listOfLines)
    firstMatrix = listOfLines[0:firstMatrixLines]

    secondMatrixLines = getNumberOfValuesInMatrixText(listOfLines[
                                                      firstMatrixLines+1:])
    secondMatrix = listOfLines[firstMatrixLines+1:firstMatrixLines + 1 +
                                secondMatrixLines]
    return firstMatrix, secondMatrix

"""
Splits all the lines into values, this separates a line into a list of all of
its values.
"""
def getStringValuesFromMatrix(listOfMatrixLines):
    resultingList = []
    for line in listOfMatrixLines:
        resultingList += line.split()

    return resultingList

"""
Grabs both lists and simply makes a new list with mixed pairs from both lists.
Note: The length will be of the firstMatrix and the default values for the
second is 0.0
"""
def pairLinesBySeparator(firstMatrix, secondMatrix, delimiter=","):
    resultingList = []
    elementFromFirst = ""
    elementFromSecond = ""

    for indexOfFirstMatrix in range(len(firstMatrix)):
        elementFromFirst = firstMatrix[indexOfFirstMatrix]
        if indexOfFirstMatrix > len(secondMatrix):
            elementFromSecond = "0.0"
        else:
            elementFromSecond = secondMatrix[indexOfFirstMatrix]
        resultingList.append(elementFromFirst + delimiter + elementFromSecond)

    return resultingList

"""
Function to get how many lines are from the beginning of a list until it
reaches the index of an empty line.
"""
def getNumberOfValuesInMatrixText(listOfLines):
    for index, line in enumerate(listOfLines):
        if (line.strip() == ""):
            return index

def inputDataIntoFile(listOfData, outputFileName):
    with open(outputFileName, "w") as outputFile:
        for lineOfData in listOfData:
            outputFile.write(lineOfData + "\n")


def interateThroughFileList(listOfFilenames):
    listOfDataStrings = []
    for filename in listOfFilenames:
        listOfDataStrings += extractMatrixFromFile(filename)

    return listOfDataStrings

def parsePressionEnthalpyWithoutCoefficients(matrixStringList, outputFileName) :
    pressionValues = []
    enthalpyValues = []
    nonCoefficientValues = []

    hasEnthalpyAppeared = hasPressionAppeared = hasPostEnthalpyNewLineAppeared = False

    for line in matrixStringList:
        if line.startswith(enthalpyString) :
            hasEnthalpyAppeared = True

        if line.startswith(pressionString):
            hasPressionAppeared = True

        if (hasEnthalpyAppeared and line == '\r\n'):
            hasPostEnthalpyNewLineAppeared = True

        if (hasPressionAppeared):
            if (hasEnthalpyAppeared and not hasPostEnthalpyNewLineAppeared):
                enthalpyValues.append(line)
            elif (hasPostEnthalpyNewLineAppeared) :
                nonCoefficientValues.append(line)
            else:
                pressionValues.append(line)

    return pressionValues, enthalpyValues, nonCoefficientValues

def cleanupSortedMatrixes(listOfSortedLines):
    cleanedUpList = []
    for element in listOfSortedLines:
        if not element.startswith(fonctionString) or element.strip() != "" :
            cleanedUpList.append(element)

    return cleanedUpList

def parseSingleMatrix(matrixStringList, outputFileName):
    firstMatrix, secondMatrix = separateMatrixes(matrixStringList)
    print ("Separated Both Matrixes!")
    print ("Number of lines (A,B): " + str(len(firstMatrix)) + "," + str(len(
        secondMatrix)))

    firstMatrixValueList = getStringValuesFromMatrix(firstMatrix)
    secondMatrixValueList = getStringValuesFromMatrix(secondMatrix)
    print ("Got Both Lists of Values!")
    print ("Number of Values (A,B): " + str(len(firstMatrixValueList)) + ","
           + str(len(secondMatrixValueList)))

    finalMatrixWithPairs = pairLinesBySeparator(firstMatrixValueList,
                                                secondMatrixValueList,
                                                delimiter=",")
    print ("Got Final Matrix!")
    print ("Total Number of Lines: " + str(len(finalMatrixWithPairs)))

    inputDataIntoFile(finalMatrixWithPairs, outputFileName)
    print(finalMatrixWithPairs)
    return

def generateOutputFilenameWithIndex(baseOutputFilename, index):
    return "{0}_{2}.{1}".format(*baseOutputFilename.rsplit('.',
                                                            1) + [index])

def _convertStringLinesIntoPressionEnthalpyObjs(pressionEnthalpyMatrixLines):
    resultingObjList = []
    for index,function in enumerate(pressionEnthalpyMatrixLines):
        resultingObjList.append(Fonction(function, "output_worthless_name", index))

    return resultingObjList

def savePressionEnthalpyToFile(pressionOutputname, pressionString, coefficientOutputname, coefficientsList):
    with open(pressionOutputname, "w") as pressionFile:
        pressionFile.write(pressionString)

    with open(coefficientOutputname, "w") as coefficientsFile:
        for coefficientLine in coefficientsList:
            coefficientsFile.write(coefficientLine + "\n")

if __name__ == "__main__":
    # Run you code from here.
    # Define a filename in the following:
    inputFileName = "tab.txt"
    outputFileName = "output.txt"
    outputFileNameWithVars = "output{0}.txt"

    textWithMatrixes = extractMatrixFromFile(inputFileName)
    print ("Opened and Extracted the Text!")

    binaryFunctionList = []
    trioFunctionList = []

    for function in textWithMatrixes:
        if len(function) > 0 and function[0].startswith(pressionString):
            trioFunctionList.append(function)
        else:
            binaryFunctionList.append(function)
    #textWithMatrixes = textFromFile.split("\n")
    # Separated the binary functions from the pack.
    # print(textWithMatrixes)

    print("Printing the Last Function which as a length of -> " + str(len(trioFunctionList[-1])))
    print(trioFunctionList[-1])

    print("Saving the binary functions in files!")
    for index, matrixSet in enumerate(binaryFunctionList):
        print(matrixSet)
        parseSingleMatrix(matrixSet, generateOutputFilenameWithIndex(
            outputFileName, index))

    pressionEnthalpyList = _convertStringLinesIntoPressionEnthalpyObjs(trioFunctionList)
    binaryFunctionCount = len(binaryFunctionList)

    stringPressionEnthalpy = ""
    coefficientList = []
    print("Saving the Presion - Enthalpy functions in files now!")
    for index, pressionEnthalpyFunction in enumerate(pressionEnthalpyList):
        roundedIndex = binaryFunctionCount + index

        if (pressionEnthalpyFunction.HasCoefficients):
            for index in range(len(pressionEnthalpyFunction.pressionList)):
                pressionOutputname = generateOutputFilenameWithIndex(outputFileNameWithVars.format("_a" + str(index)), roundedIndex)
                coefficientOutputname = generateOutputFilenameWithIndex(outputFileNameWithVars.format("_b" + str(index)), roundedIndex)

                stringPressionEnthalpy = pressionEnthalpyFunction.exportListAsString(pressionEnthalpyFunction.pressionList[index])
                stringPressionEnthalpy += "\n" + pressionEnthalpyFunction.exportListAsString(pressionEnthalpyFunction.enthalpieList[index])
                coefficientList = pressionEnthalpyFunction.exportCoefficientList(index)

                savePressionEnthalpyToFile(pressionOutputname, stringPressionEnthalpy, coefficientOutputname, coefficientList)

        else:
            pressionOutputname = generateOutputFilenameWithIndex(outputFileNameWithVars.format("_a"), roundedIndex)
            coefficientOutputname = generateOutputFilenameWithIndex(outputFileNameWithVars.format("_b"), roundedIndex)

            stringPressionEnthalpy = pressionEnthalpyFunction.exportListAsString(pressionEnthalpyFunction.pressionList[0])
            stringPressionEnthalpy += "\n" + pressionEnthalpyFunction.exportListAsString( \
                pressionEnthalpyFunction.enthalpieList[0])
            coefficientList = pressionEnthalpyFunction.exportCoefficientList(0)

            savePressionEnthalpyToFile(pressionOutputname, stringPressionEnthalpy, coefficientOutputname, coefficientList)

    # partialSingleGrille = "partial_single_grille_rlph.txt" # PASSED
    # partialNoCoeffGrille = "partial_no_coef_slph.txt" # PASSED
    # partialInput = "partial_input_ctlph.txt"
    #
    # testingFile = partialInput
    #
    # fileLines = []
    # with open(testingFile, "r") as fileHandler:
    #     for line in fileHandler:
    #         fileLines.append(line)
    #
    # functionObj = Fonction(fileLines, "output_name", 18)



    print ("Success!")
