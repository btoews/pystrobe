# file: pystrobe.py
# (c) mastahyeti 2012
# MIT license
# YAY CURSES... just kidding

from time import sleep
from sys import argv
from math import sin,pi
from multiprocessing import Process, Pipe
import curses
import pyaudio
import struct

def play_binaural(left_freq=440, right_freq=460):
    #set some vars
    sampwidth   = 2
    frate       = 44100.0
    amp         = 8000.0
    channels    = 2
    periods     = 20
    data_size = int((frate/left_freq)*(frate/right_freq)) * periods
    audio_string = ""

    #setup pyaudio and stream
    PyAudio = pyaudio.PyAudio
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(sampwidth),rate=int(frate),output=True,channels=channels)

    #generate audio data
    for x in range(data_size):
        left = sin(2*pi*left_freq*(x/frate))
        right = sin(2*pi*right_freq*(x/frate))
        audio_string += struct.pack("hh",left*amp/2,right*amp/2)

    print "playing"

    while True:
	    stream.write(audio_string)

    #cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

def strobe(screen,frequency,cp_1,cp_2):
	#this is a generator (don't care about what it generates) that
	#oscilates between cp_1 and cp_2. We yeild with each oscilation
	#so preferably (for the sake of true frequency) quick things
	#can be done simultaniously without implementing concurency
	sleep_time = 1/frequency
	cps = [cp_1,cp_2]
	i = 0

	try:
		child = Process(target=play_binaural,args=(200,frequency+200))
		child.start()

		while 1:
			c = screen.getch()
			if c != -1:

				if c == curses.KEY_UP:
					frequency += frequency/20
					sleep_time = 1/frequency
				if c == curses.KEY_DOWN:
					frequency -= frequency/20
					sleep_time = 1/frequency
				child.terminate()
				child = Process(target=play_binaural,args=(200,frequency+200))
				child.start()
			screen.bkgd(' ',curses.color_pair(cps[i%2]))
			screen.move(0,0)
			screen.clrtoeol()
			screen.addstr("frequency: %f hz\t\t\tuse keyboad arrows to adjust frequency(5 percent at a time)" % frequency)
			screen.refresh()
			i ^= 1
			sleep(sleep_time)
			yield 1	
	except:
		child.terminate()
		raise

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
