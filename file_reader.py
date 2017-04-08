textFromFile = """
*FLICA
CODE: 'FLICA' ;
OPTION: 'ECHO' 0 ;
OPTION: 'STAT' 'OUI' ;
F4VERSION = VERSION_CODE_FLICA4 ;
WRITE: 6 F4VERSION ' ' ;
TITRE = 'fichier eau.10-210'   ;
FIC_NAM = 'Eau.10-210bar:200kJ' ;
FIC_NAM_XDR = 'Eau.10-210bar:200kJ.xdr' ;


*            ========
			 BLOC EAU   ;
*            ========
*
FONCTIONS_FLUIDE

*__________________________________________________________
*_____________________etats a saturation___________________

FONCTION_SAR   TSP   22

*scale___0___________0___________0___________0___________0___________012
5E5	15.E5	25.E5	35.E5	45.E5	55.E5	65.E5
75.E5	85.E5	95.E5	105.E5	115.E5	125.E5	135.E5
145.E5	155.E5	165.E5	175.E5	185.E5	195.E5	205.E5
215.E5

	0.1E2	0.2E2	0.3E2
	0.1E2	0.2E2	0.3E2
	0.1E2
	0.1E2	0.2E2	0.3E2
	0.1E2
	0.1E2	0.2E2	0.3E2
	0.1E2	0.2E2
	0.1E2	0.2E2	0.3E2
	0.1E2	0.2E2	0.3E2

MAILLAGE_P  85


FONCTIONS_FLUIDE

*__________________________________________________________
*_____________________etats a saturation___________________

FONCTION_BOI   TSP   22

*scale___0___________0___________0___________0___________0___________012
5E5	15.E5	25.E5	35.E5	45.E5	55.E5	65.E5
75.E5	85.E5	95.E5	105.E5	115.E5	125.E5	135.E5
145.E5	155.E5	165.E5	175.E5	185.E5	195.E5	205.E5
215.E5

	1.1E2	1.2E2	1.3E2
	1.1E2	1.2E2	1.3E2
	1.1E2	1       1
	1.1E2	1.2E2	1.3E2
	1.1E2	1       1
	1.1E2	1.2E2	1.3E2
	1.1E2	1.2E2	1
	1.1E2	1.2E2	1.3E2
	1.1E2	1.2E2	1.3E2

MAILLAGE_P  85
"""

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
        parseSingleMatrix(matrixSet, "output-" + str(index) + ".txt")

    print ("Success!")