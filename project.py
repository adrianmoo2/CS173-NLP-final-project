import json
import re
#from nltk.corpus import stopwords
import string

instructionsList = []

instructionsWordList = []

titlesList = []

tools = []#["chef's", "knife", "soup", "spoon", "bowl", "spoon"]

toolsMaster = []#["chef's knife", "soup spoon", "bowl", "spoon"]


def getTools():

    toolsMasterFile = open('newTools.txt','r')
    
    for line in toolsMasterFile:
        line = re.sub('\n','',line)
        toolsMaster.append(line)
    
    tokenTools = open('tokenizedTools.txt','r')

    for line in tokenTools:
        line = re.sub('\n','',line)
        tools.append(line)
    
#    print(toolsMaster)
##    print("\n")
#    print(tools)




def getInstructions():
    with open('recipes_raw_nosource_epi.json') as f:
        data = json.load(f)
    for recipe in data.values():
        instructionsList.append(recipe["instructions"])

    return instructionsList

def getTitles():
    with open('recipes_raw_nosource_epi.json') as f:
        data = json.load(f)
    for recipe in data.values():
        titlesList.append(recipe["title"])

    return titlesList

def cleanInstructions(instructionsList):
    stopWords = ['a','about','an','and','are','as','at','be','but','by','for','from','has','have','he','his','in','is','it','its','more','new','of','on','one','or','said','say','that','the','their','they','this','to','was','which','who','will','with','you']
    for instruction in instructionsList:
        instruction = re.sub('[!@#:;"{}<>,.()\/^\_%$1234567890]', '', instruction)
        instructionWords = instruction.lower().split()
        instructionWords = [x for x in instructionWords if x not in stopWords]
        instructionsWordList.append(instructionWords)
    return instructionsWordList

def findTools(recipeNum, instructionsWordList):
    
#    masterTools = [word in recipeWords for word in tools]
    masterTools = []
    buffer = ""
    for word in instructionsWordList[recipeNum]:
        if word in tools:
            buffer += word + " "
        else:
            if(len(buffer) > 0):
                buffer = buffer[0:len(buffer)-1]
                masterTools.append(buffer)
            buffer = ""

    for i in range(0, len(masterTools)):
        if masterTools[i] not in toolsMaster:
            masterTools[i] = ''
    masterTools = list(filter(None, masterTools)) # fastest

    masterTools = list(set(masterTools))

    return masterTools


getTools()
getInstructions()
getTitles()

#print(len(instructionsList))
#print(len(cleanInstructions(instructionsList)))

cleanInstructions(instructionsList)

#og
#print(findTools(1,instructionsWordList))

#duplicates removed
#print (titlesList[0])
#print (instructionsList[0])
#print(list(dict.fromkeys(findTools(1,instructionsWordList))))
#u suck so im taking over...watch and learn bimch hehe...blehblahblooey 

prompt = ""
numRecipe = 1

deleteWordsList = ["meat", "sugar", "bread", "slice", "hot milk", "salt pepper", "butter", "cheese", 
"pepper", "milk", "egg egg", "nutmeg salt", "grill cooking", "vegetable", "hot", "garlic", "pastry", 
"water", "cutting", "dough", "baking", "rolling", "press", "saucespan whisk", "peel", "browning", "egg", 
"salt", "pepper", "fish", "cooking", "kitchen", "torch", "lemon", "flour", "spoon cup", "bread slice butter",
"salt pepper grill", "whisk milk", "salt pepper spoon cup", "turkey baking sheet", "gravy", "turkey",
"flour baking", "corn", "bowl whisk", "whisk flour sugar", "hot pie", "dough flour", "biscuit", "sugar water",
"deep", "sugar salt", "serving", "garlic salt butter", "spoon tomato", "fat", "press dough", "cherry",
"garlic salt", "butter skillet","fruit", "cup sugar", "spoon lemon", "cake", "butter flour",
"pie", "salt baking", "flour sugar baking", "egg whisk wet", "sugar lemon"]


def deleteBadWords(inputList, badList, outputList):
    for i in range(len(inputList)):
        if inputList[i] not in badList:
            outputList.append(inputList[i])
    return outputList

def deleteBadWordsToolsVersion(inputList, badList, outputList):
    tempOutput = []
    for i in range(len(inputList)):
        if inputList[i] not in badList:
            tempOutput.append(inputList[i])
    outputList.append(tempOutput)
    return outputList
            

while (prompt != "quit"):
    prompt = str(input("Hi! If you would like to look up a recipe number, please type \"num\". If you would like to search for recipes by inputting tools, type \"tools\". If you would like to look up the instructions for a recipe, type \"instructions\"\n"))
    if (prompt == "num"):
        finalToolsList = []
        
        numRecipe = int(input("Please enter the number of the recipe you would like to search (0-25322). \"quit\" to exit.\n"))
        toolsList = list(dict.fromkeys(findTools(numRecipe, instructionsWordList)))

        deleteBadWords(toolsList, deleteWordsList, finalToolsList)

        print (list(dict.fromkeys(finalToolsList)))
    elif (prompt == "tools"):
        toolsQuery = (input("\nPlease input the tools you would like to search for, separated by a colon and a space (i.e. \"spoon: baking sheet: sieve\")\n")).lower()
        userToolsList = (toolsQuery.split(': '))

        aggToolsList = []

        finalAggToolsList = []

        finalTitlesList = []

        for i in range(len(instructionsList)):
            aggToolsList.append(list(dict.fromkeys(findTools(i, instructionsWordList))))
            deleteBadWordsToolsVersion(aggToolsList[i], deleteWordsList, finalAggToolsList)

        for i in range(len(instructionsList)):
            for j in range(len(userToolsList)):
                if all(elem in finalAggToolsList[i] for elem in userToolsList):
                    finalTitlesList.append(titlesList[i])
        
        print (list(dict.fromkeys(finalTitlesList)))

    elif prompt == "instructions":
        instructionsQuery = input("\nPlease input the name of the recipe you would like to search for\n").lower()
        print (instructionsQuery)

        for i in range(len(titlesList)):
            if (instructionsQuery in titlesList[i].lower()):
                print (instructionsList[i])