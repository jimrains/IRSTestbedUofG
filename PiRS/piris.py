import RPi.GPIO as GPIO
import random
import time
import sys

import socket
import json
import struct
import numpy as np

def initPIcom():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(DATA, GPIO.OUT)
	GPIO.setup(SCLK, GPIO.OUT)
	GPIO.setup(RW, GPIO.OUT)
        GPIO.setup(FB, GPIO.IN)

def sendbits(bitsx):
	for x in range(9):
		GPIO.output(SCLK,GPIO.LOW)
		if (bitsx[x]>0):
			GPIO.output(DATA,GPIO.HIGH)
		else:
			GPIO.output(DATA,GPIO.LOW)
		time.sleep(0.00000001)
		GPIO.output(SCLK,GPIO.HIGH)
		time.sleep(0.00000001)
	GPIO.output(SCLK,GPIO.LOW)

socketPort = int(sys.argv[1])

DATA = 5 # to pin 28 on FPGA
SCLK = 15# to pin 26 on FPGA
RW = 7   # to pin 30 on FPGA
FB = 10

mapping =  [201,    241,    136,    537,    481,    376,    473,    169,    8,
		    193,    104,    144,    529,    344,    384,    465,    161,    16,
		    56,     112,    281,    392,    352,	521,    457,    153,    24,
		    64,	    120,	273,	400,	360,	513,	320,	145,	32,
		    72,     233,	265,	408,	569,	505,	312,	296,	40,
		    80, 	225,	128,	416,	561,	368,	449,	304,	48,
            88, 	217,	257,	424,	553,	497,	441,	328,	185,
            96, 	209,	249,	432,	545,	489,	433,	336,	177,
            202,	242,	135,	538,	482,	375,	474,	170,	7,
            194,	103,	143,	530,	343,	383,	466,	162,	15,
            55, 	111,	282,	391,	351,	522,	458,	154,	23,
			63,	    119,	274,	399,	359,	514,	319,	146,	31,
			71,	    234,	266,	407,	570,	506,	311,	295,	39,
			79,	    226,	127,	415,	562,	367,	450,	303,	47,
			87, 	218,	258,	423,	554,	498,	442,	327,	186,
			95,  	210,	250,	431,	546,	490,	434,	335,	178,
			203,	243,	134,	539,	483,	374,	475,	171,	6,
			195,	102,	142,	531,	342,	382,	467,	163,	14,
			54,  	110,	283,	390,	350,	523,	459,	155,	22,
			62,  	118,	275,	398,	358,	515,	318,	147,	30,
			70, 	235,	267,	406,	571,	507,	310,	294,	38,
			78,	    227,	126,	414,	563,	366,	451,	302,	46,
			86, 	219,	259,	422,	555,	499,	443,	326,	187,
			94, 	211,	251,	430,	547,	491,	435,	334,	179,
			204,	244,	133,	540,	484,	373,	476,	172,	5,
			196,	101,	141,	532,	341,	381,	468,	164,	13,
			53,	    109,	284,	389,	349,	524,	460,	156,	21,
			61, 	117,	276,	397,	357,	516,	317,	148,	29,
			69, 	236,	268,	405,	572,	508,	309,	293,	37,
			77,	    228,	125,	413,	564,	365,	452,	301,	45,
			85, 	220,	260,	421,	556,	500,	444,	325,	188,
			93,	    212,	252,	429,	548,	492,	436,	333,	180,
			205,	245,	132,	541,	485,	372,	477,	173,	4,
			197,	100,	140,	533,	340,	380,	469,	165,	12,
			52, 	108,	285,	388,	348,	525,	461,	157,	20,
			60,  	116,	277,	396,	356,	517,	316,	149,	28,
			68, 	237,	269,	404,	573,	509,	308,	292,	36,
			76,  	229,	124,	412,	565,	364,	453,	300,	44,
			84,	    221,	261,	420,	557,	501,	445,	324,	189,
			92, 	213,	253,	428,	549,	493,	437,	332,	181,
			206,	246,	131,	542,	486,	371,	478,	174,	3,
			198,	99,	    139,	534,	339,	379,	470,	166,	11,
			51,  	107,	286,	387,	347,	526,	462,	158,	19,
			59,	    115,	278,	395,	355,	518,	315,	150,	27,
			67, 	238,	270,	403,	574,	510,	307,	291,	35,
			75, 	230,	123,	411,	566,	363,	454,	299,	43,
			83, 	222,	262,	419,	558,    502,	446,	323,	190,
			91,	    214,	254,	427,	550,	494,	438,	331,	182,
			207,	247,	130,	543,	487,	370,	479,	175,	2,
			199,	98,	    138,	535,	338,	378,	471,	167,	10,
			50,	    106,	287,	386,	346,	527,	463,	159,	18,
			58,	    114,	279,	394,	354,	519,	314,	151,	26,
			66,	    239,	271,	402,	575,	511,	306,	290,	34,
			74,	    231,	122,	410,	567,	362,	455,	298,	42,
			82,	    223,	263,	418,	559,	503,	447,	322,	191,
			90,	    215,	255,	426,	551,	495,	439,	330,	183,
			208,	248,	129,	544,	488,	369,	480,	176,	1,
			200,	97,	    137,	536,	337,	377,	472,	168,	9,
			49,	    105,	288,	385,	345,	528,	464,	160,	17,
			57,	    113,	280,	393,	353,	520,	313,	152,	25,
			65,	    240,	272,	401,	576,	512,	305,	289,	33,
			73,	    232,	121,	409,	568,	361,	456,	297,	41,
			81,	    224,	264,	417,	560,	504,	448,	321,	192,
			89,	    216,	256,	425,	552,	496,	440,	329,	184]



## Maps bits into packets of length 9 in correct order for shift registers
def createSequence(bitstream):
	seq = [""]*64
	for i in range(0,64):
		shift = ""
		for k in range(0,9):
			shift = shift + bitstream[mapping[i*9 + k] - 1]
		seq[i] = shift
	return seq

## Bit banging to interface with FPGA
def sendConfig(sequence):
	GPIO.output(RW,GPIO.HIGH)
	time.sleep(0.0000001)
	for i in range(0,64):
		res = [int(k) for k in sequence[i]]
		sendbits(res)
	time.sleep(0.00000001)
	GPIO.output(RW,GPIO.LOW)
	time.sleep(0.00000001)
	GPIO.output(SCLK,GPIO.HIGH)
	time.sleep(0.00000001)
	GPIO.output(SCLK,GPIO.LOW)



initPIcom()

#irs_bits_seq = list(bin(3)[2:].zfill(3))
#irs_bits_list = irs_bits_seq*192
#irs_bits = ''.join(str(e) for e in irs_bits_list)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.4.1',socketPort))
s.listen(5)
print('Waiting for connection...')
sock, addr = s.accept()

data = ''
print('connected.')
while 1:
	s = "a"
    s_l = s.encode()
	sock.send(s_l)
    data = sock.recv(20000)
    data = data.decode('utf-8')
    irs_bits = data
    fpga_seq = createSequence(irs_bits)
	sendConfig(fpga_seq)
    while 1:
        if GPIO.input(FB) == 1:
            break

print("Done")
