# file: pystrobe.py
# (c) mastahyeti 2012
# MIT license
# YAY CURSES... just kidding

import curses
from time import sleep
from sys import argv

def strobe(screen,frequency,cp_1,cp_2):
	#this is a generator (don't care about what it generates) that
	#oscilates between cp_1 and cp_2. We yeild with each oscilation
	#so preferably (for the sake of true frequency) quick things
	#can be done simultaniously without implementing concurency
	sleep_time = 1/frequency
	cps = [cp_1,cp_2]
	i = 0
	while 1:
		c = screen.getch()
		if c != -1:
			if c == curses.KEY_UP:
				frequency += frequency/20
				sleep_time = 1/frequency
			if c == curses.KEY_DOWN:
				frequency -= frequency/20
				sleep_time = 1/frequency

		screen.bkgd(' ',curses.color_pair(cps[i%2]))
		screen.move(0,0)
		screen.clrtoeol()
		screen.addstr("frequency: %f hz\t\t\tuse keyboad arrows to adjust frequency(5 percent at a time)" % frequency)
		screen.refresh()
		i ^= 1
		sleep(sleep_time)
		yield 1	 

def main(screen):
	try:
		#frequency better be there, or else YOU are in big trouble mister!
		try:
			frequency = float(argv[-1])
		except:
			print "usage: python ./pystrobe.py <frequency>"
			die_nice(screen)
		#setup some color pairs
		curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
		curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_WHITE)
		#FREAK OUT!
		for i in strobe(screen,frequency,1,2):
			pass
	except KeyboardInterrupt:
		die_nice(screen)

def die_nice(stdscr):
	curses.curs_set(1)
	stdscr.keypad(0)
	stdscr.nodelay(0)
	curses.nocbreak()
	curses.echo()
	curses.endwin()

if __name__=="__main__":
	try:
		stdscr = curses.initscr()
		#invisible cursor
		curses.curs_set(0)
		#allow color setting
		curses.start_color()
		#enable keypad
		stdscr.keypad(1)
		#don't block on getch
		stdscr.nodelay(1)
		#don't let user input get printer
		curses.noecho()
		#don't wait for return to get user input
		curses.cbreak()
		#run our main loop
		main(stdscr)	
		#cleanup
		die_nice(stdscr)
	#if there is a problem, fix the terminal and die
	except:
		#if you want debugging, you probably shouldn't do this. VVVVV
		die_nice(stdscr)
