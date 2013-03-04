import string,time,pdb,itertools,time
import Tkinter as tk
   
#Need to fix these global variables
global dictionary,italianDictionary,validWords,validCoordinates,gameToAnalyze
    
#gameToAnalyze=[['c','o','c','p'],['i','n','i','a'],['a','e','g','v'],['f','c','s','i']] #TESTING PURPOSE
#357 words(original Ruzzle dictionary) vs 291 word (ruzzleSolver) #TESTING PURPOSE

gameToAnalyze=[['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]
dictionary={}
italianDictionary={}
validWords=[]
validCoordinates=[]


#Function that searches for the correct cells next to the given one, and discards the non valid ones
#i.e the cells with x and/or y lower than 0 and/or bigger than 3

def checkCellsWithinBounds(row,col):
    tempCellsWithinBounds=list()
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            tempCellsWithinBounds.append([row+x,col+y])
    tempCellsWithinBounds.remove([row,col]) #Remove the cell with the same coordinates as the given one, so that loops are not made
    
    #Discard the cells out of the table's bonds
    correctCellsWithinBounds=list()
    for cell in tempCellsWithinBounds:
        if (0<=cell[0]<=3) and (0<=cell[1]<=3):
            correctCellsWithinBounds.append(cell)
    correctCellsWithinBounds.sort()
    return correctCellsWithinBounds


#Function that discards the cells i have already processed (emptyList are allowed as values to be returned)

def checkCellsWithinBoundsFromWhomIDidNotPass(cellsWithinBounds, cellsAlreadyProcessed):
    cellsToProcess=list()
    for cell in cellsWithinBounds:
        if not (cell in cellsAlreadyProcessed):
            cellsToProcess.append(cell)
    return cellsToProcess


#Function that searches for word matches in the dictionary. It creates a list of valid words as well as one with their coordinates

def dictionaryCheck(cellIAmNowAnalyzing,cellsToFormWord):
    
    #wordToCheck is built by merging all of the coordinates inside cellsToFormWord
    #and by matching them with the table's letters (contained in  gameToAnalyze)
    wordToCheck=''.join([gameToAnalyze[x[0]][x[1]] for x in cellsToFormWord])
    
    if wordToCheck in italianDictionary:
        if not (wordToCheck in validWords):
            validWords.append(wordToCheck)
            validCoordinates.append([entryList[couple[0]][couple[1]] for couple in cellsToFormWord])
                        
    if wordToCheck in dictionary:
        return 1
    elif not wordToCheck in dictionary:
        return 0


#Function that deals with recursion. Also it is the only one called by main()

def startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord):
    evaluableCells=checkCellsWithinBoundsFromWhomIDidNotPass(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)
    if len(evaluableCells)!=0:
        for cellToProcess in evaluableCells:
            cellsAlreadyProcessedAndToFormWord.append(cellToProcess)
            
            #After this I know if there are other words that start with my branch or if i have to do backtrack
            dictionaryMatch=dictionaryCheck(cellToProcess,cellsAlreadyProcessedAndToFormWord)
            if dictionaryMatch>0: #equal to if dictionaryMatch and dictionaryMatch!=-1
                cellsWithinBounds=checkCellsWithinBounds(cellToProcess[0],cellToProcess[1])
                startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)     
            elif dictionaryMatch==0:
                #Delete the last item (alias letter), because no word starts with it
                del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]
    else: #No more cells to evaluate: dead-end
        del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]
        return 
    del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]


def main():
    global validCoordinates,validWords    
    f=open("ruzzleFinalWordListWithCommas.txt","r")
    for line in f.read().split(','):
        italianDictionary[line]=True
        l=len(line)+1
        for i in range(1,l):
            dictionary[line[:i]]=True #The dictionary is filled with all the words, plus all the branches from len=1 to len=len-1
    f.close()
    
    for mainRow in range(4):
        for mainCol in range(4):
            cellsWithinBounds=checkCellsWithinBounds(mainRow,mainCol)
            cellsAlreadyProcessedAndToFormWord=[[mainRow,mainCol]]
            startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)

    #Invert validWords (validCoordinates is inverted in place in the return)
    validWords=sorted(validWords,key=len,reverse=True)
    return sorted(validCoordinates,key=len,reverse=True)


#Here we start with the Tkinter section of the code#

def solveGame():
    for x in range(4):
        for y in range(4):
            gameToAnalyze[x][y]=(entryList[x][y].get().lower())
            #entryList[x][y].insert(0,gameToAnalyze[x][y]) #TESTING PURPOSE
    entriesToColour=main()
        
    allEntries=itertools.chain(entriesToColour)
    divideListToColour(allEntries)


def changebg(listOfAllEntries):
    listOfAllEntries = iter(listOfAllEntries) #Allow a list to be passed as argument to changebg
    entry = next(listOfAllEntries,None)
    if entry is not None:
        entry['bg']='yellow'
        root.after(500,changebg,listOfAllEntries)
        return

    #The flow reaches this points only when all the listOfAllEntries cells background colour has been changed to yellow
    for entryToDecolour in listToSplit:
        entryToDecolour['bg']='white'


def divideListToColour(setOfAllEntries,result=1):
    #global listToSplit is needed inside changebg(). global ids is needed inside newgame()
    global listToSplit,ids
    listToSplit=next(setOfAllEntries,None)
    if listToSplit is not None:
        changebg(listToSplit)
        ids=root.after(500*(len(listToSplit)+1),divideListToColour,setOfAllEntries)
        
def newgame():
    gameToAnalyze=[['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]
    try:root.after_cancel(ids)
    except NameError: pass
    
    for x in range(4):
        for y in range(4):
            entryList[x][y].delete(0)
            entryList[x][y]['bg']='white'
    entryList[0][0].focus_set() 
    


def validate(string):
    try:root.focus_get().insert(0,string.upper())
    except: root.focus_get().insert(0,'')
    nextBox()


def nextBox():
    for row in range(4):
        #Search for tk.Entry through all the four rows.
        #It always returns 3 ValueError; in the other case it finds the right row and set the focus on the right cell
        try:
            column=entryList[row].index(root.focus_get())
            entryList[row][column+1].focus_set()
        except ValueError: pass
        except IndexError:
            if row<3:
                #Go to the next row, starting from the first cell (column=0)
                entryList[row+1][0].focus_set()
                return


root = tk.Tk()
root.option_add("*Entry.Font","Arial 32 bold")

emptyLabel=tk.Label()
emptyLabel.grid(row=4)
entryList=[]

vcmd=(root.register(validate),'%S') #Now it is implented only the validation of the first letter ('%S') put inside each cell 
for x in range(4):
    entryList.append([])
    for y in range(4):
        entryList[x].append('')
        entryList[x][y]=tk.Entry(root, bg="white",width=2,justify="center",
                                 takefocus=True,insertofftime=True,
                                 validate="key",validatecommand=vcmd)
        entryList[x][y].grid(row=x,column=y)

solvebt=tk.Button(root,text='Solve',command=solveGame).grid(row=5,column=2)
newgamebt=tk.Button(root,text='New',command=newgame).grid(row=5,column=1)

entryList[0][0].focus_set()

root.mainloop()
