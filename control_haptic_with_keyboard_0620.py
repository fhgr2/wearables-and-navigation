#!usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import time
import gpiozero as io # using GPIO zero

# Output-Pin zuordnen und 'off' setzen
vm_lf = io.LED(5) # PIN 5 für VM left front 
vm_lb = io.LED(12) # PIN 5 für VM left back 
vm_m = io.LED(6) # PIN 6 für VM middle 
vm_rf = io.LED(13) # PIN 13 für VM right front 
vm_rb = io.LED(16) # PIN 16 für VM right back 
vm_lf.off()  ##############################################
vm_lb.off()
vm_rf.off()
vm_rb.off()
vm_m.off()


# Impulsdauer, Nachpause und Pausenlänge festlegen
impulsdauer = 0.65	# Länge eines Impulses
nachpause = 0.1	# Bause zwischen den einzelnen Impulsen
signalpause = 1 # Pausenlänge in der Signalisierung


#---------------------------------------
# haptic signaling functions
#---------------------------------------
	
def impuls_left_right():
	print('impuls left and right ')
#	print(datetime.datetime.now().time())
	vm_lf.on()
	vm_lb.on()
	vm_rf.on()
	vm_rb.on()
	time.sleep(impulsdauer)
	vm_lf.off()
	vm_lb.off()
	vm_rf.off()
	vm_rb.off()
#	print('impuls fertig')
#	print(datetime.datetime.now().time())
	time.sleep(nachpause)
#	print('nachpause fertig')
#	print(datetime.datetime.now().time())
	
	
def impuls_left_front():
	print('impuls left front')
	vm_lf.on()
	time.sleep(impulsdauer)
	vm_lf.off()
	time.sleep(nachpause)
	
def impuls_left():
	print('impuls left')
	vm_lf.on()
	vm_lb.on()
	time.sleep(impulsdauer)
	vm_lf.off()
	vm_lb.off()
	time.sleep(nachpause)
	
def impuls_left_back():
	print('impuls left back')
	vm_lb.on()
	time.sleep(impulsdauer)
	vm_lb.off()
	time.sleep(nachpause)


def impuls_right_front():
	print('impuls right front')
	vm_rf.on()
	time.sleep(impulsdauer)
	vm_rf.off()
	time.sleep(nachpause)

def impuls_right():
	print('impuls right')
	vm_rf.on()
	vm_rb.on()
	time.sleep(impulsdauer)
	vm_rf.off()
	vm_rb.off()
	time.sleep(nachpause)

def impuls_right_back():
	print('impuls right back')
	vm_rb.on()
	time.sleep(impulsdauer)
	vm_rb.off() ############################################
	time.sleep(nachpause)
	

def impuls_middle():
	print('impuls middle')
	vm_m.on()
	time.sleep(impulsdauer)
	vm_m.off()
	time.sleep(nachpause)
	

#---------------------------------------
# signaling command functions
#---------------------------------------
def ps():
	impuls_left_right()
	time.sleep(signalpause)
	impuls_left_right()
	
# end ps

#-----------------------------------------------------------
# left direction
def slf():
	impuls_left_front()
	impuls_left_front()
	time.sleep(signalpause)
	impuls_left_front()
	impuls_left_front()

# end 


def tl():
	impuls_left()
	impuls_left()
	time.sleep(signalpause)
	impuls_left()
	impuls_left()

# end


def slb():
	impuls_left_back()
	impuls_left_back()
	time.sleep(signalpause)
	impuls_left_back()
	impuls_left_back()

# end

#--------------------------------------------
# right direction
def srf():
	impuls_right_front()
	impuls_right_front()
	time.sleep(signalpause)
	impuls_right_front()
	impuls_right_front()

# end 


def tr():
	impuls_right()
	impuls_right()
	time.sleep(signalpause)
	impuls_right()
	impuls_right()

# end


def srb():
	impuls_right_back()
	impuls_right_back()
	time.sleep(signalpause)
	impuls_right_back()
	impuls_right_back()

# end


#---------------------------------------------
# roundabout
def ra1():
	impuls_middle()
	time.sleep(signalpause)
	impuls_middle()

# end

def ra2():
	impuls_middle()
	impuls_middle()
	time.sleep(signalpause)
	impuls_middle()
	impuls_middle()

# end

def ra3():
	impuls_middle()
	impuls_middle()
	impuls_middle()
	time.sleep(signalpause)
	impuls_middle()
	impuls_middle()
	impuls_middle()

# end

#------------------------------------
# U-turn
def ut():
	impuls_middle()
	impuls_middle()
	impuls_middle()
	time.sleep(signalpause)
	impuls_middle()
	impuls_middle()
	impuls_middle()
	time.sleep(signalpause)
	impuls_middle()
	impuls_middle()
	impuls_middle()

# end

# arrived
def arr():
	impuls_middle()
	impuls_middle()
	impuls_middle()
	impuls_middle()
	impuls_middle()
	impuls_middle()

# end



#------------------------------------
# main
#------------------------------------
print("control_haptic_with_keyboard")
print("Ctrl C zum Beenden")
print(" ")
print("Folgende Befehle sind als Eingabe möglich:")
print("ps, slf, tl, slb, srf, tr, srb, ra1, ra2, ra3, ut, arr")

while True:
	cmd = input('command: ')
	if cmd == 'ps':
		ps()
	elif cmd == 'slf':
		slf()
	elif cmd == 'tl':
		tl()
	elif cmd == 'slb':
		slb()
	elif cmd == 'srf':
		srf()
	elif cmd == 'tr':
		tr()
	elif cmd == 'srb':
		srb()
	elif cmd == 'ra1':
		ra1()
	elif cmd == 'ra2':
		ra2()
	elif cmd == 'ra3':
		ra3()
	elif cmd == 'ut':
		ut()
	elif cmd == 'arr':
		arr()
	else:
		print('This is not a command!')
	

