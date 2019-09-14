
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
		'A': [[0,0], 'P1', [0,10], [10,10], [10,5], [0,5], [10,5], [10,0], 'P0'],					# P0 :: turn off laser
		'B': [[0,0], 'P1', [0,10], [10,10], [10,5], [0,5], [10,5], [10,0], [0,0], 'P0'],			# P1 :: turn ON laser
		'C': [[0,0], 'P1', [0,10], [10,10], [0,10], [0,0], [10,0], 'P0'],
		'D': [[0,0], 'P1', [0,10], [10,10], [10,0], [0,0], 'P0'],
		'E': [[0,0], 'P1', [0,10], [10,10], [0,10], [0,5], [10,5], [0,5], [0,0], [10,0], 'P0']
	}

	# return coordinates for drawing inputText
	drawingSequence = []		# append coordinate-data here
	incrementPerChar = 10+2		# space between char-origins
	numCharsDrawn = 0			# counter
	for char in inputText:
		for coord in charLUT[char.upper()]:
			if coord in ['P0','P1']:	# element is a lift/drop flag
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
		if coord == 'P1': pencil.pendown()	# put pen on canvas @ start of char
		elif coord == 'P0': pencil.penup()	# lift pen off canvas @ end of char
		else:
			pencil.goto(coord[0], coord[1])
	window.exitonclick()


# Generate file for serial-transmission to Microcontroller
def writeCoordsToFile(coordSequence):

	# write coords + newline
	f = open('textCoordinates.txt', 'w+')
	for coord in coordSequence:
		command = coord
		if coord not in ['P0', 'P1']: 
			command = 'X'+str(coord[0]) + ' Y'+str(coord[1])
		f.write(command+'\n')

	# append 'D' to ensure file is deleted off uC
	f.write('D\n')


textCoordinates = generateCoordinates("A BCD ABC")
writeCoordsToFile(textCoordinates)