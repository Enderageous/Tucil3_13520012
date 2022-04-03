import BnB
import os.path

loop = True

while (loop):
    puzzle = []

    option = input("Read File or Randomized?\n(1) Read File\n(2) Randomized\nInput: ")
    print("")
    while (option != "1" and option != "2"):
        option = input("Input error, Read File or Randomized?\n(1) Read File\n(2) Randomized\nInput: ")
        print("")
        
    if (int(option) == 1):
        puzzle = BnB.readFile()

        BnB.printPuzzleKurang(puzzle)
    
    elif (int(option) == 2):
        repeat = True
        puzzle = BnB.randomPuzzle()
        BnB.printPuzzleKurang(puzzle)

        while (repeat):
            option2 = input("Is this okay? (Y/N): ")
            if (option2 == "Y" or option2 == "y"):
                repeat = False
            elif (option2 == "N" or option2 == "n"):
                puzzle = BnB.randomPuzzle()
                BnB.printPuzzleKurang(puzzle)
            else:
                print("\nInput error")
                

    kurang = BnB.kurang(puzzle)
    if (kurang%2 == 0):
        print("Loading...\n")
        BnB.solve(puzzle)
    else:
        print("\nPuzzle cannot be solved\n")

    option3 = input("Want to do another? (Y/N): ")
    repeat = True
    while (repeat):
        if (option3 == "Y" or option3 == "y"):
            repeat = False
        elif (option3 == "N" or option3 == "n"):
            loop = False
            repeat = False
        else:
            option3 = input("Input error. Want to do another? (Y/N): ")
    print("")
