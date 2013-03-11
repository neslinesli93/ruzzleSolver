import string,time


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
        validWords.append(wordToCheck)
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
    else:
        del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]
        return 
    del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]


def main():
    
    #Need to fix these global variables
    global dictionary,italianDictionary,validWords,gameToAnalyze,start

    dictionary={}
    italianDictionary={}
    validWords=[]

    f=open("ruzzleWordListWithCommas.txt","r")
    for line in f.read().split(','):
        italianDictionary[line]=True
        l=len(line)+1
        for i in xrange(1,l):
            dictionary[line[:i]]=True #The dictionary is filled with all the words, plus all the branches from len=1 to len=len-1
    f.close()

    gameToAnalyze=list()
    for x in range(4):
        gameToAnalyze.append(raw_input("Inserisci le lettere della riga "+str(x+1)+": ").split(","))
    start=time.time()
    for mainRow in range(4):
        for mainCol in range(4):
            cellsWithinBounds=checkCellsWithinBounds(mainRow,mainCol)
            cellsAlreadyProcessedAndToFormWord=[[mainRow,mainCol]]
            startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)
            
    validWords=list(set(validWords))
    end=time.time()-start
    print "In %f secondi, si e' trovato che:\n a)Il gioco ha %d soluzioni, le quali sono(ordinate secondo le piu' lunghe):"%(end,len(validWords))
    for x in sorted(validWords,key=len):
        print x+',',

main()
