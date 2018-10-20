import ui
from Suudoku import *
from FilePicker import *

NumX = 9
NumY = 9
NumN = 9
sbx1 = 20
sby1 = 80
wbx1 = 40
wby1 = 40
sbx2 = 20
sby2 = 490
wbx2 = 40
wby2 = 40
pre_tile = ''
pre_one = []
tileButtons = []
numberButtons = []
l_remain = ''
tv_file = ''
pos_x = -1
pos_y = -1

def update_tile() :
	for j in range(NumY) :
		for i in range(NumX) :
			tileButtons[j*NumX+i].title = su.getNumber(i,j)
			if su.getLock(i,j) :
				tileButtons[j*NumX+i].tint_color = 'Black'
			else :
				tileButtons[j*NumX+i].tint_color = '8080ff'

	l_remain.text = str(su.getRemain())
	
def update_numberButtons() :
	for n in range(NumN) :
		if str(n+1) in su.getAvailable(pos_x,pos_y) :
			numberButtons[n].enabled = True
		else :
			numberButtons[n].enabled = False

def update_hint() :
	global pre_one
	for one in su.get1available_pos() :
		tileButtons[one[1]*NumY+one[0]].border_color = 'green'
		tileButtons[one[1]*NumY+one[0]].border_width = 3
	pre_one  = su.get1available_pos()

def update_hint2() :
	for j in range(NumY) :
		for i in range(NumX) :
			pos = j * NumX + i
			if su.getNumber(i,j) == '' :
				if len(su.getAvailable(i,j)) == 2 :
					tileButtons[pos].tint_color = '#ff80ff'
					tileButtons[pos].title = ','.join(su.getAvailable(i,j))
				elif su.getNumber(i,j) != tileButtons[pos].title :
					tileButtons[pos].title = ''
				
def clear_hint() :
	for one in pre_one :
		tileButtons[one[1]*NumY+one[0]].border_color = 'black'
		tileButtons[one[1]*NumY+one[0]].border_width = 1
			
def clear_all_hint() :
	for i in range(NumX * NumY) :
		tileButtons[i].border_color = 'black'
		tileButtons[i].border_width = 1

def b_clear_push(sender) :
	global su
	su = Suudoku(NumX,NumY,NumN)
	pre_one = []
	update_tile()
	clear_all_hint()

def sw_hint_click(sender) :
	if sender.value :
		update_hint()
	else :
		clear_all_hint()

def sw_hint2_click(sender) :
	if sender.value :
		update_hint2()
	else :
		update_tile()
	
@ui.in_background
def tile_push(sender) :
	global pre_tile
	global pre_one
	global pos_x
	global pos_y
	
	l_mess = sender.superview['l_message']
	
	if pre_tile != '' :
		pre_tile.border_color = 'black'
		pre_tile.border_width = 1
		
	sender.border_color = 'red'
	sender.border_width = 3
	
	pos_x = int((sender.center.x-sbx1)/wbx1)
	pos_y = int((sender.center.y-sby1)/wby1)
	
	update_numberButtons()
	if su.getNumber(pos_x,pos_y) == '' :
		numberButtons[9].enabled = False
	else :
		if su.getLock(pos_x,pos_y) :
			numberButtons[9].enabled = False
		else :
			numberButtons[9].enabled = True
	pre_tile = sender
	l_mess.text = '"' + su.getNumber(pos_x,pos_y) + '" ' + str(su.getLock(pos_x,pos_y))

@ui.in_background
def number_push(sender) :
	l_mess = sender.superview['l_message']
	if pos_x == -1 :
		l_mess.text = 'pos_x == -1'
		return
		
	num = int((sender.center.x-sbx2)/wbx2) + 1
	if not su.setNumber(pos_x, pos_y, str(num)) :
		l_mess.text = su.message
		return 
	
	clear_hint()

	pos = pos_y * NumX + pos_x
	if su.getLock(pos_x,pos_y) :
		tileButtons[pos].tint_color = 'black'
	else :
		tileButtons[pos].tint_color = '#8080ff'
	tileButtons[pos].title = str(num)
	
	update_numberButtons()
	sw_hint = sender.superview['sw_hint']
	if sw_hint.value :
		update_hint()
	sw_hint2 = sender.superview['sw_hint2']
	if sw_hint2.value :
		update_hint2()
	l_remain.text = str(su.getRemain())

def number_clear_push(sender) :
	l_mess = sender.superview['l_message']
	if pos_x == -1 :
		l_mess.text = 'pos_x == -1'
		return
	
	if not su.setNumber(pos_x, pos_y, '') :
		l_mess.text = su.message
		return 
		
	pos = pos_y * NumX + pos_x
	tileButtons[pos].title = ''
	clear_hint()
	update_numberButtons()
	sw_hint = sender.superview['sw_hint']
	if sw_hint.value :
		update_hint()
	sw_hint2 = sender.superview['sw_hint2']
	if sw_hint2.value :
		update_hint2()
	l_remain.text = str(su.getRemain())														
def b_load_push(sender) :
	fname = file_picker_dialog('Pick some .csv files', root_dir = './', multiple=False, select_dirs=False, file_pattern=r'^.*\.csv$', show_size = False)
	print('fname = %s' %(fname))
	#def file_picker_dialog(title=None, root_dir=None, multiple=False,
	#select_dirs=False, file_pattern=None, show_size=True):

def b_save_push(sender) :
	pass


#main
v = ui.load_view()

#make tileButton & numberButton
for j in range(NumY) :
	offy = int(j / 3) - 1
	for i in range(NumX) :
		offx = int(i / 3) - 1
		button = ui.Button(title=str(i*NumX+j))
		button.center = (sbx1+wbx1*i+offx, sby1+wby1*j+offy)
		button.width = wbx1+1
		button.height = wby1+1
		button.border_width = 1
		button.border_color = 'black'
		button.action = tile_push
		v.add_subview(button)
		tileButtons.append(button)

	button = ui.Button(title=str(j+1))
	button.center = (sbx2+wbx2*j, sby2)
	button.width = wbx2+1
	button.height = wby2+1
	button.tint_color = 'red'
	button.border_width = 1
	button.border_color = 'black'
	button.action = number_push
	v.add_subview(button)
	numberButtons.append(button)

button = ui.Button(title='clear')
button.center = (sbx2+2, sby2+wby2)
button.width = wbx2+1
button.height = wby2+1
button.tint_color = 'red'
button.border_width = 1
button.border_color = 'black'
button.action = number_clear_push
v.add_subview(button)
numberButtons.append(button)

l_remain = v['l_remain']


su = Suudoku(NumX, NumY, NumN)
if not su.load("data/test2.csv") :
	print('Error : load() : %s' %(su.message))
	exit(1)

update_tile()

v.present('sheet')

