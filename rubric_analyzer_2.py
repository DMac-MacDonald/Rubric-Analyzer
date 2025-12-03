#csv: used to write and read from csv files
#os: used for batch processing
#PIL: main library, used for image processing and pixel detection
import csv
import os
from PIL import Image 



#lineBox[]: hard coded list of 4-tuple box locations/sizes for each line of bubbles (will be dynamic later)
#bubbleBox[]: hard coded list of 4-tuple box locations/sizes for each bubble on a line (will be dynamic later)
#scoreList[]: list to be written to the .csv file at the end of the program
#cardDirectory: string local folder name for card images
#imageSize: tuple variable for setting the image size for reliability 
#scoreDetect: bool variable for checking if a score has been found
cardDirectory = "Cards" 
configDirectory = "configFiles"

lineboxes=[]
bubbleBoxes = []

startLineBox = (0,0,250,40)
startBubbleBox = (5,5,50,40)
imageSize = (250,500)



scoreList = [] 
#headers = ["Project Motivation", "Constraints", "Evaluation Metrics", "State of the art", "Design Concepts", "Concepts Selection", "Budget", "Schedule", "Citations","Questions", "Presentation Effective?"]

scoreDetect = int
def readConfig(filename):
        confList=[]
        confReadPath = os.path.join("configfiles", filename)
        with open(confReadPath, 'r') as file:
            for idx, line in enumerate(file):
                match idx:
                    case 0:
                        confList.append(int(line))
                    case 1:
                        confList.append(int(line))
                    case 2:
                        confList.append(line.split(','))
        return confList

    

def main():
    print("[1] Batch Process")
    print("[2] Create Rubric Config")
    print("[3] Help")
    print("[4] Quit")
    choice = input("Choose from the options above:")

    match choice:
        case "1":
            batchProcess()
        case "2":
            createConfig()
        case "3":
            print("To use the tool, take a picture of the filled out score card containing only the bubbles. Then place the picture into the folder labeled as cards. Then select batch process and the program will analyze any images in the folder. The final scores are output into a .csv file which can be opened with excel or google sheets")
            print("[1] Quit")
            print("[2] Return")
            choice2 = input("Choice:")
            match choice2:
                case "1":
                    quit
                case "2":
                    main()
        
        case "4":
            quit
        case _:
            print("INVALID CHOICE")
            main()


def createConfig():
    lNum = input("Number of lines:")
    bNum = input("Number of bubbles per line:")
    hList = input(f"Input {lNum} header names for each score metric, seperated by commas:")
    rName = input("Config file name (conf[name].txt):")
    choice = input("Create File?(y/n):")

    match choice:
        case "y" | "Y":
            confPath = os.path.join("configFiles", f"conf{rName}.txt")
            with open(confPath, "w") as file:
                file.write(f"{lNum}\n")
                file.write(f"{bNum}\n")
                file.write(f"{hList}")
                
            main()
        case "n" | "N":
            main()



def batchProcess():
    headers = [] 
    lineNumber = 11
    bubbleNumber = 5
    
    def defineLineBoxes():
        lineboxes.append(startLineBox)
        tupleList = list(startLineBox)
        for i in range(lineNumber-1):
            tupleList[1] += (500/lineNumber)
            tupleList[3] += (500/lineNumber)
            tupledtuple = tuple(tupleList)
            lineboxes.append(tupledtuple)

    def defineBubbleBoxes():
        bubbleBoxes.append(startBubbleBox)
        tupleList = list(startBubbleBox)
        for i in range(bubbleNumber-1):
            tupleList[0] += (250/bubbleNumber)
            tupleList[2] += (250/bubbleNumber)
            tupledtuple = tuple(tupleList)
            bubbleBoxes.append(tupledtuple)
    for idxC, filename in enumerate(os.listdir(configDirectory)):
        print(f"[{idxC}]{filename}")
    config = input("Choose config file:")
    confList = readConfig(config)
    lineNumber = confList[0]
    bubbleNumber = confList[1]
    headers = confList[2]

    


    defineLineBoxes()
    defineBubbleBoxes()
    print("running....")#start of program


    for idxF, filename in enumerate(os.listdir(cardDirectory)): #Loop to allow for checking every card image in the cards folder
        scoreIndvList = []
        file_path = os.path.join(cardDirectory, filename)
        infile = file_path
        image = Image.open(infile)
        image = image.resize(imageSize)

        image = image.convert("L") #convert image to greyscale (to avoid off colors from irl pictures)
        image = image.convert("RGB")#converts image to rgb image for easy color detection, retains greyscale change
        image.save("uncropped.jpg")
        for idxJ, j in enumerate(lineboxes):#Line for loop
            lineScoreNum = 0
            currentLine = image.crop(j)#crops the image to each line
            outputPath1 = os.path.join("lineImages", f"line{idxJ}.jpg")
            currentLine.save(outputPath1)

            for idxI, i in enumerate(bubbleBoxes):#Bubble for loop
                scoreDetect = 0
                currentBubble = currentLine.crop(i) #crops line image to each bubble
                outputPath2 = os.path.join("bubbleImages", f"{idxJ}Bubble{idxI}.jpg")
                currentBubble.save(outputPath2)
                for x in range(currentBubble.width): #checks if there is a black pixel in the bubble image, if there is, sets detect variable to true
                        for y in range(currentBubble.height):
                            pixel_color = currentBubble.getpixel((x, y))
                            if pixel_color == (0,0,0):
                                scoreDetect = 1
                        
                if scoreDetect == 1: #If black was detected in the bubble image
                    
                    print(f"[{filename},Bubble:{idxI+1},Line:{idxJ+1}]")#terminal output
                    if idxI == 0:#appends scores to individual list if detected
                        scoreIndvList.append(str(idxI))
                    else:
                        scoreIndvList.append(str(idxI+1))
                else:
                    lineScoreNum += 1
            if lineScoreNum == bubbleNumber or lineScoreNum < bubbleNumber-1:
                scoreIndvList.append("N/A")
        scoreList.append(scoreIndvList)#appends the batch score list with the individual list of scores
        with open('scores.csv', 'w', newline='') as csvfile: #updates .csv file with collected scores
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(scoreList)
            

    print("done!")#end of program



                    

main()