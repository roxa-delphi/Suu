import sys

class Suudoku_tile :
	number = ''
	available = []
	lock = False
	
	def __init__(self, maxnum) :
		self.number = ''
		self.clear_available(maxnum)
		lock = False

	def clear_available(self, maxnum) :
		self.available = [str(x) for x in range(1, maxnum+1)]
		
class Suudoku :
	maxNumber= 0
	numX = 0
	numY = 0
	__tile = []
	__remain = 0
	message = ''
		
	def clear(self) :
		self.maxNumber = 0
		self.numX      = 0
		self.numY      = 0
		self.__tile    = []
		self.__remain  = 0

	def __init__(self, nx, ny, maxnumber) :
		
		self.maxNumber = maxnumber
		self.numX = nx
		self.numY = ny
		self.__tile = []
		self.__remain = nx * ny

		for j in range(self.numY) :
			line = []
			for i in range(self.numX) :
				t = Suudoku_tile(self.maxNumber)
				line.append(t)
			
			self.__tile.append(line)
		
	def print_number(self) :
		print('tile = %s, %s' %(self.numX, self.numY))
		for j in range(self.numY) :
			for i in range(self.numX) :
				if self.__tile[j][i].number == '' :
					print(' ,', end='')
				else :
					print('%s,' %(self.__tile[j][i].number), end='')
			print('')
		print('')
	
	def getAvailable(self, x, y) :
		return self.__tile[y][x].available
	
	def getNumber(self, x, y) :
		return self.__tile[y][x].number

	def getLock(self, x, y) :
		return self.__tile[y][x].lock

	def getRemain(self) :
		return self.__remain

	def set_available(self, x, y, number) :
		for i in range(self.numY) :
			if number in self.__tile[i][x].available :
				self.__tile[i][x].available.remove(number)
		
		for i in range(self.numX) :
			if number in self.__tile[y][i].available :
				self.__tile[y][i].available.remove(number)

		px = int(x / 3) * 3
		py = int(y / 3) * 3
		#print('x,y = %d,%d px,py=%d,%d' %(x,y,px,py))
		for j in range(py, py+3) :
			for i in range(px, px+3) :
				if number in self.__tile[j][i].available :
					self.__tile[j][i].available.remove(number)		

	def fix_availables(self) :
		for j in range(self.numY) :
			for i in range(self.numX) :
				self.__tile[j][i].clear_available(self.maxNumber)

		for j in range(self.numY) :
			for i in range(self.numX) :
				self.set_available(i, j, self.__tile[j][i].number)																																				
	def setNumber_withLock(self, x, y, number, lock) :
		fix = False
		if number == '' :
			fix = True
		elif number < '1' :
			self.message = 'number is less than "1"'
			return False
		elif number > '9' :
			self.message = 'numer is larger than "9"'
			return False
		
		if self.__tile[y][x].lock :
			self.message = 'tile was locked'
			return False
		
		if self.__tile[y][x].number != '' :
			self.message = 'tile does not ""'
			fix = True
			#return False
			
		#print('%d,%d,"%s" : "%s" %s' %(x, y, number, self.tile[y][x].number, self.tile[y][x].available))

		if number == '' :
			self.__tile[y][x].number = ''
			self.__tile[y][x].lock   = lock
			self.__remain += 1
		else :
			if number not in self.__tile[y][x].available :
				self.message = 'tile does not available(' + str(x) + ',' + str(y) + ')'
				return False
			
			self.__tile[y][x].number = number
			self.__tile[y][x].lock   = lock
			self.__remain -= 1
		
		if fix :
			self.message = 'fix_availables'
			self.fix_availables()
		else :
			self.set_available(x, y, number)

		return True

	def setNumber(self, x, y, number) :
		return self.setNumber_withLock(x, y, number, False)

	def get1available_pos(self) :
		ret = []
		
		for j in range(self.numY) :
			for i in range(self.numX) :
				if self.__tile[j][i].number == '' :
					if len(self.__tile[j][i].available) == 1 :
						ret.append([i, j])
		return ret
		

	def load(self, filename) :
		self.clear()

		with open(filename) as f :
			line = f.readline()
			para = line.split(',')
			#print("para = %s" %(para))
			self.__init__(int(para[0]), int(para[1]), int(para[2]))

			for j in range(self.numY) :

				line = f.readline()
				#print("line = %s" %(line))
				para = line.split(',')
								
				for i in range(self.numX) :
					if para[i] == ' ' :
						continue
					if not self.setNumber_withLock(i,j,para[i],True) :
						return False
																				
		return True


def input_cmd() :
	while True :
		su.print_number()
		print('1 availables = %s' %(su.get1available_pos()))
		
		cmdstr = input('suu > ')
		cmd = cmdstr.split(',')
		
		if cmd[0] == 'e' :
			break
		if cmd[0] == 'set' :
			if not su.setNumber(int(cmd[1]),int(cmd[2]),cmd[3]) :
				print('error')
				print('')
				
if __name__ == "__main__":
	
	su = Suudoku(9, 9, 9)

	if not su.load("data/test2.csv") :
		print('Error : load()')
		exit(1)
	#su.print_number()
	#print('available[1][0] = %s' %(su.getAvailable(1, 0)))

	#print('1 availables = %s' %(su.get1available_pos()))

	input_cmd()
