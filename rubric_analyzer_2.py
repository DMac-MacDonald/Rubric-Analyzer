import csv
from PIL import Image

infile = "test_card_2.jpg" #change this for testing
out = open("output.txt", "w")#output file
lineBox = [(225,50,499,80),(225,90,499,120),(225,130,499,160),(225,170,499,200),(225,210,499,240),(225,255,499,295),(225,295,499,335),(225,335,499,375),(225,380,499,416),(225,415,499,456),(225,460,499,490)]
bubbleBox = [(16,5,40,30),(70,5,95,30),(124,5,149,30),(175,5,210,30),(235,5,260,30)]
scoreList = []
imageSize = (500,500)
scoreDetect = 0
print("running....")#start of program

image = Image.open(infile)
image = image.resize(imageSize)
image = image.convert("RGB")

for idxJ, j in enumerate(lineBox):

    currentLine = image.crop(j)#crops the image to each line

    for idxI, i in enumerate(bubbleBox):
        if idxJ == 8:
             currentLine.save("output1.jpg")
        scoreDetect = 0 #sets detect variable to false
        currentBubble = currentLine.crop(i) #crops line iamge to each bubble

        for x in range(currentBubble.width): #checks if there is a black pixel in the bubble image, if there is, sets detect variable to true
                for y in range(currentBubble.height):
                    pixel_color = currentBubble.getpixel((x, y))
                    if pixel_color == (0,0,0):
                        scoreDetect = 1
                
        if scoreDetect == 1: #If black was detected in the bubble image
            print("Bubble:",idxI+1, ", Line:", idxJ+1)
            if idxI == 0:#write scores to the txt file
                scoreList.append(str(idxI))
            else:
                scoreList.append(str(idxI+1))
            

with open('scores.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(scoreList)

out.close()#close output file
print("done!")#end of program