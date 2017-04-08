def extractMatrixFromFile(filename) :
    scaleInitialPattern = "*scale"
    maillageP = "MAILLAGE_P"
    hasScaleAppeared = False
    numberOfOutputs = 0
    matrixLines = []
    fileMatrixes = []
    with open(filename, "r") as matrixFile:
        for line in matrixFile:
            if (line.startswith(scaleInitialPattern)):
                hasScaleAppeared = True

            if (hasScaleAppeared):
                matrixLines.append(line)

            if (line.startswith(maillageP)):
                hasScaleAppeared = False
                numberOfOutputs += 1
                fileMatrixes.append(matrixLines[1:])
                print("New Matrix --------------" + str(len(fileMatrixes)))
                print(matrixLines)
                matrixLines = []

    return fileMatrixes

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

if __name__ == "__main__":
    # Run you code from here.
    # Define a filename in the following:
    inputFileName = "test.txt"
    outputFileName = "output.txt"

    textWithMatrixes = extractMatrixFromFile(inputFileName)
    #textWithMatrixes = textFromFile.split("\n")
    print ("Opened and Extracted the Text!")

    print(textWithMatrixes)

    for index, matrixSet in enumerate(textWithMatrixes):
        print(matrixSet)
        parseSingleMatrix(matrixSet, generateOutputFilenameWithIndex(
            outputFileName, index))

    print ("Success!")