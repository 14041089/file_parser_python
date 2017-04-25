import csv

class PressureEnthalpyMatrix:

    coefficientStartingString = "* "

    def __init__(self, pressureLines, enthalpyLines, coefficientsLines):
        self.pressureLines = pressureLines
        self.enthalpyLines = enthalpyLines
        self.coefficientLines = coefficientLines

        self.pressureValueList = self.extractPressureValues(pressureLines)
        self.enthalpyValueList = self.extractEnthalpyValues(enthalpyLines)
        self.coefficienValuesDic = self.extractCoefficients(
                self.enthalpyValueList, coefficientsLines)
        return

    def extractPressureValues(self, pressureLines):
        if ( not (pressureLines == None) and len(pressureLines) <= 0) :
            print ("The pressure list is either empty or null!")
            return []
        pressureList = []

        for line in pressureLines :
            pressureList = pressureList + line.strip(' \t\n\r')

        return pressureList

    def extractEnthalpyValues(self, enthalpyLines) :
        if ( not (pressureLines == None) and len(enthalpyLines) <= 0) :
            print ("The enthalpy is either empty or null!")

        enthalpyList = []

        for line in enthalpyLines:
            enthalpyList = enthalpyList + line.strip(" \t\n\r")

            return enthalpyList

    def getCoefficientDictionary(self, coefficientLines):
        compositeLine = ""
        coefficientEnthalpyValue = ""
        coefficientDic = {}

        for coefficientLine in coefficientLines :
            if coefficientLine.startswith( coefficientStartingString ) :
                if not coefficientEnthalpyValue == "": # Saving Information
                    coefficientDic[coefficientEnthalpyValue] = compositeLine

                coefficientEnthalpyValue =
                    coefficientLine[len(coefficientStartingString):]

                compositeLine = ""
            else :
                coefficientLine = compositeLine + coefficientLine

        return coefficientDic

    def exportDataIntoFiles(self, outputfilename, outputExtension=".csv",
            outputDelimiter=" ") :
        outputPressureFilename = outputFilename + "-a" + outputExtension
        outputCoefficientFilename = outputFilename + "-b" + outputExtension

        with open(outputPressureFilename, "w") as pressureFile:
            pressureWriter = csv.writer(pressureFile, delimiter=outputDelimiter)
            pressureWriter.writerow(self.pressureValueList)
            pressureWriter.writerow(self.enthalpyValueList)

        with open(outputCoefficientFilename, "w") as coefficientsFile:
            pressureWriter.writerow(self.enthalpyValueList)
            coefficientWriter = csv.writer(coefficientWriter,
                    delimiter=outputDelimiter)
            for enthalpyValue in self.enthalpyValueList:
                coefficientWriter.writerow(self.coefficientValueDic[enthalpyValue])

