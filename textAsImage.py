
'''

Convert text-input (i.e. "Hello World!") 
into coordinates for drawing

'''

import turtle

'''
(1) start @ [0,0]
(2) execute 'A' instruction
(2) shift all x-coords rightwards by charSpace*numCharsDrawn
'''

def generateCoordinates(inputText, scale=5):

	# LUT
	charLUT = {
		' ': [[0,0]], #space
		'A': [[0,0], 'D', [0,10], [10,10], [10,5], [0,5], [10,5], [10,0], 'L'],
		'B': [[0,0], 'D', [0,10], [10,10], [10,5], [0,5], [10,5], [10,0], [0,0], 'L'],
		'C': [[0,0], 'D', [0,10], [10,10], [0,10], [0,0], [10,0], 'L'],
		'D': [[0,0], 'D', [0,10], [10,10], [10,0], [0,0], 'L'],
		'E': [[0,0], 'D', [0,10], [10,10], [0,10], [0,5], [10,5], [0,5], [0,0], [10,0], 'L']
	}

	# return coordinates for drawing inputText
	drawingSequence = []		# append coordinate-data here
	incrementPerChar = 10+2		# space between char-origins
	numCharsDrawn = 0			# counter
	for char in inputText:
		for coord in charLUT[char.upper()]:
			if coord in ['D','L']:	# element is a lift/drop flag
				drawingSequence.append(coord)
				continue
			else: # element is coord
				x = scale * (coord[0] + numCharsDrawn*incrementPerChar)
				y = scale * coord[1]
				drawingSequence.append([x,y])
		numCharsDrawn += 1

	return drawingSequence


# Test Generated Coordinates
def turtleTest(coordSequence):

	# create drawing tools
	window = turtle.Screen()
	pencil = turtle.Turtle()

	for coord in coordSequence:
		if coord == 'D': pencil.pendown()	# put pen on canvas @ start of char
		elif coord == 'L': pencil.penup()	# lift pen off canvas @ end of char
		else:
			pencil.goto(coord[0], coord[1])
	window.exitonclick()

# Write sequence to Text-File
def writeCoordinateFile(coordSequence):
	

turtleTest(generateCoordinates("A BCD ABC"))