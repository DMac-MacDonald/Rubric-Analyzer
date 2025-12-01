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
lineBox = [(225,50,499,80),(225,90,499,120),(225,130,499,160),(225,170,499,200),(225,210,499,240),(225,255,499,295),(225,295,499,335),(225,335,499,375),(225,380,499,416),(225,415,499,456),(225,460,499,490)]
bubbleBox = [(16,5,40,30),(70,5,95,30),(124,5,149,30),(175,5,210,30),(235,5,260,30)]
scoreList = [] 
imageSize = (500,500)
scoreDetect = 0
print("running....")#start of program


for idxF, filename in enumerate(os.listdir(cardDirectory)): #Loop to allow for checking every card image in the cards folder
    scoreIndvList = []
    file_path = os.path.join(cardDirectory, filename)
    infile = file_path
    image = Image.open(infile)
    image = image.resize(imageSize)

    image = image.convert("L") #convert image to greyscale (to avoid off colors from irl pictures)
    image.save("output1.jpg") #testing image
    image = image.convert("RGB")#converts image to rgb image for easy color detection, retains greyscale change

    for idxJ, j in enumerate(lineBox):#Line for loop

        currentLine = image.crop(j)#crops the image to each line

        for idxI, i in enumerate(bubbleBox):#Bubble for loop

            scoreDetect = 0 #sets detect variable to false
            currentBubble = currentLine.crop(i) #crops line iamge to each bubble

            for x in range(currentBubble.width): #checks if there is a black pixel in the bubble image, if there is, sets detect variable to true
                    for y in range(currentBubble.height):
                        pixel_color = currentBubble.getpixel((x, y))
                        if pixel_color == (0,0,0):
                            scoreDetect = 1
                    
            if scoreDetect == 1: #If black was detected in the bubble image
                print("Bubble:",idxI+1, ", Line:", idxJ+1)
                if idxI == 0:#appends scores to individual list if detected
                    scoreIndvList.append(str(idxI))
                else:
                    scoreIndvList.append(str(idxI+1))


    scoreList.append(scoreIndvList)#appends the batch score list with the individual list of scores

    with open('scores.csv', 'w', newline='') as csvfile: #updates .csv file with collected scores
        writer = csv.writer(csvfile)
        writer.writerows(scoreList)

print("done!")#end of program