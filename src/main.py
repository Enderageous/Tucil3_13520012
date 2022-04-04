import BnB
import os.path

loop = True

while (loop):
    puzzle = []
    kurang = 1

    option = input("Read File or Randomized?\n(1) Read File\n(2) Randomized\nInput: ")
    print("")
    while (option != "1" and option != "2"):
        option = input("Input error, Read File or Randomized?\n(1) Read File\n(2) Randomized\nInput: ")
        print("")
        
    if (int(option) == 1):
        puzzle = BnB.readFile()

        kurang = BnB.printPuzzleKurang(puzzle)
    
    elif (int(option) == 2):
        repeat = True
        puzzle = BnB.randomPuzzle()
        kurang = BnB.printPuzzleKurang(puzzle)

        while (repeat):
            option2 = input("Is this okay? (Y/N): ")
            if (option2 == "Y" or option2 == "y"):
                repeat = False
            elif (option2 == "N" or option2 == "n"):
                puzzle = BnB.randomPuzzle()
                kurang = BnB.printPuzzleKurang(puzzle)
            else:
                print("\nInput error")
        print("")

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
