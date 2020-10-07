# scan the grid for matching letters
def scan(grid, word):
    #the legal variable stores an error code string if theres an error or 
    # a list of the row, column, and letter_index if it passes the checkLegal function
    legal = 'no matching letter' 

    for letter_index in range(len(word)):
        # for each letter in the given word check each space of every row and column for a matching letter
        for row in range(20):
            for column in range(20):
                if grid[row][column] == word[letter_index]:
                    # if a matching letter is found get the orientation needed for the word to fit the spot found
                    orientation = getOrientation(grid, (row,column,letter_index))
                    if orientation != None:
                        # if a valid orientation is found check if the word placement violates any crossword rules
                        legal = checkLegal(grid, word, orientation, row, column, letter_index)
                        if type(legal) != str:
                            # if checkLegal doesnt return an error return the row, column, letter_index of the valid spot 
                            # and the orientation needed to place the word
                            return((row,column,letter_index), orientation)
    # if the word placement violates a law return the error code
    return legal

# check if the word placement violates any laws of the game
def checkLegal(grid, word, orientation,row,column,letter_index):
    # check if the word makes any new words
    for h in range(0, len(word)):
        if orientation == 'vertical':
            new_row = row - letter_index + h #new_row is the index of where the first letter will go if this word is to be placed here
            # check if the word goes out of the grid vertically
            if new_row >= 20 or new_row <= -1 or new_row >=20 or new_row <= -1:
                    return 'reaches outside grid'
            # check where the word will go for another word in that place, if the letter found in this place is the same as the letter being placed here ignore it
            elif grid[new_row][column] != word[h]:
                # check if the column goes out of grid then start at the top of the word shift 1 to the left and check downwards
                if column - 1 > -1:
                    if grid[new_row][column-1] != ' ' and new_row != row:
                        return 'illegal adjacencies'
                # check if the column goes out of grid then shift 1 to the right and check down
                if column + 1 < 20:
                    if grid[new_row][column+1] != ' ' and new_row != row:
                        return 'illegal adjacencies'
                # check one below the bottom and one above the top to see if the word touches another word
                if row-letter_index-1 > -1:
                    if grid[(row-letter_index)-1][column] != ' ':
                        return 'illegal adjacencies'
                if row-letter_index+len(word)+1 < 20:
                    if grid[(row-letter_index+len(word))][column] != ' ':
                        return 'illegal adjacencies'
                
        else:
            new_column = column - letter_index+h #new_column is the index of the biegining of the first letter of where this word will go
            # check if the word goes out of the grid horizontally
            if column- letter_index+h >= 20 or column- letter_index+h <= -1:
                return 'reaches outside grid'
                # check where the word will go to see if its replacing another word with this spot
            elif grid[row][new_column] != word[h]:
                # shift 1 row up and check for a letter thats not in the connecting word
                if row - 1 > -1:
                    if grid[row-1][new_column] != ' ' and new_column != column:
                        return 'illegal adjacencies'
                # shift 1 row down and check for a letter thats not in the connecting word(i.e: a letter that has a column value thats not the connecting word's column)
                if row + 1 < 20:
                    if grid[row+1][new_column] != ' ' and new_column != column:
                        return 'illegal adjacencies'
                # check one to the right and one to the left of this words placement to check if it touches another word
                if (column-letter_index)-1 > -1:
                    if grid[row][(column-letter_index)-1] != ' ':
                        return 'illegal adjacencies'
                if column-letter_index+len(word) < 20:
                    if grid[row][(column-letter_index+len(word))] != ' ':
                        return 'illegal adjacencies'

    # if the placement satisfies every law return true
    return True

# place a word on the grid with a determined orientation
def placeWord(grid, word, freeSpot, orientation):
    row = freeSpot[0]
    column = freeSpot[1]
    letter_index = freeSpot[2]
    if orientation == 'horizontal':
        for i in range(len(word)):
            # if the orientation is horizontal subtract the index of the letter from column of the free spot to start at the begining of the word
            # then place each letter of the word while increasing the column by one until all letters have been placed
            grid[row][column - letter_index+i] = (word[i])
    else:
        for i in range(len(word)):
            # for vertical plcement do the same as horizontal but for the rows not the columns
            grid[row - letter_index+i][column] = (word[i])

# get the orientation of the word being placed
def getOrientation(grid, freeSpot):
    #the row and column of the spot found for the word
    row = freeSpot[0]
    column = freeSpot[1]
    # before checking the grid for empty spaces check if the columns go out of bounds
    if column+1 < 20 and column-1 > -1:
        # if both are in bounds check both sides for empty spaces
        if grid[row][column+1] == ' ' and grid[row][column-1] == ' ':
            return 'horizontal'
    elif column+1 < 20 or column-1 > -1:
        # of one goes out of bounds check for which is in bounds then check for a spot
        # this is to account for words at the edge of the grid
        if column+1 < 20:
            if grid[row][column+1] == ' ':
                return 'horizontal'
        elif column-1 > -1:
            if grid[row][column-1] == ' ':
                return 'horizontal'
    if row+1 < 20 and row-1 > -1:
        # if both are in bounds check both sides for empty spaces
        if grid[row+1][column] == ' ' and grid[row-1][column] == ' ':
            return 'vertical'
    elif row+1 < 20 or row-1 > -1:
        # of one goes out of bounds check for which is in bounds then check for a spot
        # this is to account for words at the edge of the grid
        if row+1 < 20:
            if grid[row+1][column] == ' ':
                return 'vertical'
        elif row-1 > -1:
            if grid[row-1][column] == ' ':
                return 'vertical'

    # if all spaces around the spot are taken by letters then return none
    return None


# main function
def crossword(L):
     # sort the inputted list from longest to shortest. 
     # this makes more spots for other words faster and stops smaller words from getting in the way of larger words
    L.sort(key=len, reverse=True)
    #if a word is skipped early on because there is no spot for it, but later another added word makes a spot, runAgain
    # will make the program check the list again to see if the skipped words have spots now
    runAgain = True 
    # 20x20 grid array
    grid = []
    # list of words that are placed on the gird
    onGrid = {}
    # dictionary of words and their error
    errors = {}
    # output document and line
    f = open('output.txt', 'a')
    line = ''
    # create 20x20 grid
    for row in range(20):
        temp = [] #make a temp array to store each column in the row
        for column in range(20):
            temp.append(' ') #add a space to the list to act as a column
        grid.append(temp) #add the row to the grid and repeat

    # place frist word at middle horizontally
    firstWordLen = len(L[0])
    fLen = int(firstWordLen/2)#find half the length of the word
    for column in range(len(L[0])):
        grid[9][(10-fLen)+column] = (L[0][column]) #the first word is placed at the middle of the grid

    # scan the grid and find a place for the next word in the list
    while runAgain == True: #keep scanning for places until no words are placed in a scan
        placedWords = 0
        for word in range(1, len(L)):
            repeats = L.count(L[word])
            if L[word] not in onGrid: #if a word isnt on the grid scan for a spot to place it
                onGrid[L[word]] = 0
            # if the word in the dict has been checked less times then it appears in the list then check it again
            if onGrid[L[word]] < repeats:
                # scan for a place for the word
                placement = scan(grid, L[word])
                if type(placement) != str: #if placement == str then it returned an error
                    #if theres a spot for the word get the row, column and orientation the word needs and place it on the grid
                    freeSpot = placement[0]
                    orientation = placement[1]
                    placeWord(grid, L[word], freeSpot, orientation)
                    onGrid[L[word]] += 1 #if the word was succefully placed add one to the word in the dict
                    placedWords+=1 #increase placedWords so that the loop will run again since now there are new spots for the earlier skipped words to be placed
                    if L[word] in errors: 
                        # if this word produced an error before but has a spot now remove it from errors
                        del errors[L[word]]
                    break #stop checking for places for this word since now it has a place
                
                #if the word produced an error and isnt already on the grid add the error report to errors 
                if type(placement) == str:
                    errors[L[word]] = placement
        if placedWords == 0: #if this set of scans didnt place any new words stop scanning. all the placeable words have been placed
            runAgain = False

    # display grid
    for row in range(20):
        for column in range(20):
            line += (' '+grid[row][column]+' ') #run through the grid array and add every row to the line string
        line += '\n'
        f.write(line) #write the line string into the output txt doc
        line = '' #reset line
    for key,val in errors.items(): #after the grid has been displayed output the errors
        line = str(key+': '+val+'\n')
        f.write(line)
    f.write('\n\n')
    f.close()

def testing():
    # clear output before each test
    f = open('output.txt', 'w')
    f.write('')
    f.close()
    #test cases
    crossword(['hat','doctor','slap','goo','dump','sink'])
    crossword(['unicorn','cream','horse','rihno','diamond','pencil','running','capitalism'])
    crossword(['rat','hare','crocodile','painter','snake', 'gumbo', 'electricity', 'toe', 'bogus', 'deer', 'boom', 'tesla', 'construction'])
    crossword(['apologe', 'virgil', 'pascalian', 'bitter', 'gods', 'tetnus'])
    crossword(["abcdefghijklmnopqrst","fffffggg","tttttttttuuuuuuuuuz","yzzz","qqqqqqqqqqqqqqy","xxxxxxxxxaaaaaaa","aaaaggg","xxwwww","wwwwvvvvve","vvvvvvvvvvvvq","mat","mat","make","make","maker","remake","hat",])
    crossword(['addle','paddle','apple','plan', 'incline','clowning','plane','loon'])
    crossword(['cat','rot','tar','rar', 'moor', 'lure', 'tear', 'maximum', 'clog'])
testing()