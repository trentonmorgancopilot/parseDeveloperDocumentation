"""
Walk through the rsmGCX directory and parse XML from each custom object.
Extract the <DeveloperDocumentation> element from the XML tree, if it exists,
and get the text associated with the documentation labels.
"""
import os, sys
import json
from xml.etree import ElementTree as ET

outputFile = "C:\\Users\\Admin56a04fd4cc\\Desktop\\parseDeveloperDocumentation\\DeveloperDocumentationOutput.txt"

"""
Primary logic function for extracting documentation from XML files.
"""
def main():

    # Set which models to extract from
    models = [
        "K:\\AosService\\PackagesLocalDirectory\\rsmGCX\\rsmGCX",
        "K:\\AosService\\PackagesLocalDirectory\\ApplicationFoundation\\ApplicationFoundation",
        "K:\\AosService\\PackagesLocalDirectory\\ApplicationPlatform\\ApplicationPlatform",
        "K:\\AosService\\PackagesLocalDirectory\\ApplicationSuite\\Foundation"
        ]

    # Process documentation for each model
    for modelPath in models:

        # Populate the documentation dictionary keys with XML file paths
        # Each file path key has a dictionary value {<label>: <translation>} populated below
        # E.g., {"path1.xml" : {"label1" : "translation1", "label2" : "translation2"}, "path2.xml" : {...}}
        documentation = getXMLFilePaths(modelPath)
        
        # For each file path, attempt to find the <DeveloperDocumentation> tag and store its value
        # Remove any paths that do not have documentation
        pathsToRemove = []
        for filePath in documentation:
            label = parseXML(filePath)
            if label is not None:
                documentation[filePath] = {label: ""}
            else:
                pathsToRemove.append(filePath)
        
        for path in pathsToRemove:
            del documentation[path]
        
        # For all of the labels found above, get their corresponding text from the label file
        for filePath in documentation:
            for label in documentation[filePath]:
                text = translateLabel(label)
                if text is not None:
                    documentation[filePath][label] = str(text)
        
        print("DEVELOPER DOCUMENTATION")
        print("-----------------------")
        print(json.dumps(documentation, indent = 4))
        
        with open(outputFile, 'a') as file:
            json.dump(documentation, file, sort_keys = True, indent = 4, ensure_ascii = False)
            
"""
Get the complete file path for each XML file within the modelPath source directory.
Return a dictionary with the paths as keys.
"""
def getXMLFilePaths(modelPath):

    xmlFilePaths = {}
    
    for root, directoryNames, fileNames in os.walk(modelPath):    
        if fileNames:
            for file in fileNames:
                if file.endswith(".xml"):
                    fullPath = (root + "\\" + file)
                    print(fullPath)
                    xmlFilePaths[fullPath] = {}
            
    return(xmlFilePaths)

"""
Parse the XML script in the given file and extract the value of the <DeveloperDocumentation> element.
Returns a string of the element text if it exists, otherwise returns None.
"""
def parseXML(filePath):

    tree = ET.parse(filePath)
    root = tree.getroot()

    # for child in root:
        # print(child.tag, child.attrib)

    value = tree.find('DeveloperDocumentation')
    if value is not None:
        print(value.text)
        return value.text
    else:
        return None
        
"""
Given a label (e.g. "@GCX0010", "@SYS1492", etc.), open the corresponding label file and extract
the text associated with the label.
Returns a string of the label text if it exists, otherwise returns None.
"""
def translateLabel(label):

    labelFilePath = ""
    if label.startswith("@GCX"):
        labelFilePath = "K:\\AosService\\PackagesLocalDirectory\\rsmGCX\\rsmGCX\\AxLabelFile\\LabelResources\\en-us\\GCX.en-us.label.txt"
    elif label.startswith("@SYS"):
        labelFilePath = "K:\\AosService\\PackagesLocalDirectory\\ApplicationPlatform\\ApplicationPlatform\\AxLabelFile\\LabelResources\\en-Us\\SYS.en-us.label.txt"
    elif label.startswith("@DMF"):
        labelFilePath = "K:\\AosService\\PackagesLocalDirectory\\ApplicationFoundation\\ApplicationFoundation\\AxLabelFile\\LabelResources\\en-Us\\DMF.en-us.label.txt"
    
    # Some labels are referred to by file name, then label name (e.g. @DMF:StagingDeveloperDocumentation),
    # so we need to remove the prefix
    if label.find(':') != -1:
        label = label.split(':', 1)[1]
    
    if labelFilePath:
        with open(labelFilePath, 'r', encoding = "utf-8") as labelFilePath:
            lines = labelFilePath.readlines()
            for line in lines:
                if line.find(label) != -1:
                    # Text is located immediately after '=' and we only want to split 1 time at most
                    text = line.split('=', 1)[1]
                    print(text)
                    return(text)

    # If we get here, the label was not found
    return None

"""
Startup
"""    
if __name__ == "__main__":
    main()
    
