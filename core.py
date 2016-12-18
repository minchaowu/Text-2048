import random
import copy

class slot(object):
	"""
	A slot is represented by a pair of intergers
	indicating its position and an interger indicating
	its value.
	"""
	def __init__(self, x, y, value):
		self.coord = (x, y)
		self.value = value

	def __str__(self):
		return self.value

	def __repr__(self):
		return str(self.value)


class board(object):
	"""A 4*4 board."""
	def __init__(self):
		self.body = [[slot(0,0,0),slot(0,1,0),slot(0,2,0),slot(0,3,0)],
		 			 [slot(1,0,0),slot(1,1,0),slot(1,2,0),slot(1,3,0)],
		 			 [slot(2,0,0),slot(2,1,0),slot(2,2,0),slot(2,3,0)],
		 			 [slot(3,0,0),slot(3,1,0),slot(3,2,0),slot(3,3,0)]]

	def __str__(self):
		for i in self.body:
			print(i)
		return ''

	def __repr__(self):
		for i in self.body:
			print(i)
		return ''

	def valueList(self):
		value_list = []
		for row in self.body:
			vrow = []
			for e in row:
				vrow.append(e.value)
			value_list.append(vrow)
		return value_list

	def gatherColumns(self):
		columns = []
		for i in range(4):
			column = []
			for row in self.body:
				column.append(row[i])
			columns.append(column)
		return columns

	def update(self, coord, value):
		x, y = coord
		self.body[x][y].value = value

	def win(self):
		for row in self.body:
			for e in row:
				if e.value == 2048:
					return True
		return False

	def lose(self):
		value_list = self.valueList()
		bd_copy = board()
		bd_copy.body = copy.deepcopy(self.body)
		if rightMove(bd_copy).valueList() == value_list and\
		leftMove(bd_copy).valueList() == value_list and\
		upMove(bd_copy).valueList() == value_list and\
		downMove(bd_copy).valueList() == value_list:
			return True
		return False

def gatherEmptySlots(bd):
	empty_slots = []
	for row in bd.body:
		for e in row:
			if e.value == 0:
				empty_slots.append(e.coord)
	return empty_slots

def generateNew(bd):
	coord = random.choice(gatherEmptySlots(bd))
	value = random.choice([2,4])
	bd.update(coord, value)
	return bd

def rightMove(bd):
	def setNewValue(row, slot):
		for i in row[::-1]:
			if i.coord[1] < slot.coord[1] and\
			i.value != 0:
				slot.value = i.value
				i.value = 0
				break

	for row in bd.body:
		for e in row[::-1]:
			if e.value == 0: setNewValue(row, e)
			for k in row[::-1]: #merge slots
				if e.coord[1] > k.coord[1] and\
				k.value == e.value:
					e.value *= 2
					k.value = 0
					break
				if e.coord[1] > k.coord[1] and\
				k.value != 0: break #stop merging when meet the first nonzero slot.
	return bd

def leftMove(bd):
	def setNewValue(row, slot):
		for i in row:
			if i.coord[1] > slot.coord[1] and\
			i.value != 0:
				slot.value = i.value
				i.value = 0
				break

	for row in bd.body:
		for e in row:
			if e.value == 0: setNewValue(row, e)
			for k in row:
				if e.coord[1] < k.coord[1] and\
				k.value == e.value:
					e.value *= 2
					k.value = 0
					break
				if e.coord[1] < k.coord[1] and\
				k.value != 0: break
	return bd

def downMove(bd):
	columns = bd.gatherColumns()
	def setNewValue(column, slot): #fill up an empty slot in a column
		for e in column[::-1]:
			if e.coord[0] < slot.coord[0] and\
			e.value != 0:
				slot.value = e.value
				e.value = 0
				break

	for column in columns:
		for e in column[::-1]:
			if e.value == 0: setNewValue(column, e)
			for k in column[::-1]:
				if e.coord[0] > k.coord[0] and\
				k.value == e.value:
					e.value *= 2
					k.value = 0
					break
				if e.coord[0] > k.coord[0] and\
				k.value != 0: break
	return bd

def upMove(bd):
	columns = bd.gatherColumns()
	def setNewValue(column, slot):
		for e in column:
			if e.coord[0] > slot.coord[0] and\
			e.value != 0:
				slot.value = e.value
				e.value = 0
				break

	for column in columns:
		for e in column:
			if e.value == 0: setNewValue(column, e)
			for k in column:
				if e.coord[0] < k.coord[0] and\
				k.value == e.value:
					e.value *= 2
					k.value = 0
				if e.coord[0] < k.coord[0] and\
				k.value != 0: break
	return bd

def startGame():
	bd = board()
	print(generateNew(bd))
	while not bd.win():
		valid_input = False
		while not valid_input:
			valid_input = True
			d = input('Specify a direction: w/a/s/d, or type end to leave: ')
			if d == 'end':
				return 'Game Over.'
			if d not in ['w', 'a', 's', 'd']:
				valid_input = False
				print('Please specify a valid direction.')
		value_list = bd.valueList()
		if d == 'w': bd = upMove(bd)
		elif d == 'a': bd = leftMove(bd)
		elif d == 's': bd = downMove(bd)
		else: bd = rightMove(bd)
		if bd.valueList() != value_list:
			print(generateNew(bd))
		if bd.lose():
			return 'No available moves, game over.'
	print('You win the game!')

startGame()
