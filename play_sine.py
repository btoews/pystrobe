""" PyAudio Example: Play a wave file """

import pyaudio
import wave
import sys
from math import sin,pi


def mapper(x,o=(0.0,1.0),n=(0.0,255.0)):
	m = ((n[1]-n[0])/(o[1]-o[0]))
	b = n[0]-o[0]
	return m*x+b

def sin_list(samples,periods):
	pi_fraction = pi/(samples*periods)
	rvals = []
	for i in range(samples):
		rvals.append(sin(pi_fraction*i))
	return rvals

def sin_wav(samples=100,periods=1):
	origvals = sin_list(samples,periods)
	rvals = []
	for val in origvals:
		rvals.append(chr(int(mapper(val))))
	return ''.join(rvals)
	

if __name__=="__main__":
	data = sin_wav(441,1)
	PyAudio = pyaudio.PyAudio
	p = PyAudio()

	# open stream
	stream = p.open(format=8,rate=44100,output=True,channels=1)

	try:
		while True:
			stream.write(data)
	except:
		pass

	stream.stop_stream()
	stream.close()

	p.terminate()



