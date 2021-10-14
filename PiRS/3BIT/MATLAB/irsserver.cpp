// IRS Pi server
// compile with:
// g++ irsserver.cpp -o irsserver -lpthread -lwiringPi

#include <wiringPi.h>
#include<stdio.h>
#include<string.h>	//strlen
#include<stdlib.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>	//write

#include<pthread.h> //for threading , link with lpthread

#define DATA 9
#define SCLK 3
#define RW 7
#define FB 16
#define DUMMY 28
#define NBITS 576

int map[] =  {201,    241,    136,    537,    481,    376,    473,    169,    8,
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
205,	  245,	132,	541,	485,	372,	477,	173,	4,
197,	  100,	140,	533,	340,	380,	469,	165,	12,
52, 	  108,	285,	388,	348,	525,	461,	157,	20,
60,  	  116,	277,	396,	356,	517,	316,	149,	28,
68, 	  237,	269,	404,	573,	509,	308,	292,	36,
76,  	  229,	124,	412,	565,	364,	453,	300,	44,
84,	    221,	261,	420,	557,	501,	445,	324,	189,
92, 	  213,	253,	428,	549,	493,	437,	332,	181,
206,	  246,	131,	542,	486,	371,	478,	174,	3,
198,	  99,	    139,	534,	339,	379,	470,	166,	11,
51,  	  107,	286,	387,	347,	526,	462,	158,	19,
59,	    115,	278,	395,	355,	518,	315,	150,	27,
67, 	  238,	270,	403,	574,	510,	307,	291,	35,
75, 	  230,	123,	411,	566,	363,	454,	299,	43,
83, 	  222,	262,	419,	558,    502,	446,	323,	190,
91,	    214,	254,	427,	550,	494,	438,	331,	182,
207,	  247,	130,	543,	487,	370,	479,	175,	2,
199,	  98,	    138,	535,	338,	378,	471,	167,	10,
50,	    106,	287,	386,	346,	527,	463,	159,	18,
58,	    114,	279,	394,	354,	519,	314,	151,	26,
66,	    239,	271,	402,	575,	511,	306,	290,	34,
74,	    231,	122,	410,	567,	362,	455,	298,	42,
82,	    223,	263,	418,	559,	503,	447,	322,	191,
90,	    215,	255,	426,	551,	495,	439,	330,	183,
208,	  248,	129,	544,	488,	369,	480,	176,	1,
200,	  97,	  137,	536,	337,	377,	472,	168,	9,
49,	    105,	288,	385,	345,	528,	464,	160,	17,
57,	    113,	280,	393,	353,	520,	313,	152,	25,
65,	    240,	272,	401,	576,	512,	305,	289,	33,
73,	    232,	121,	409,	568,	361,	456,	297,	41,
81,	    224,	264,	417,	560,	504,	448,	321,	192,
89,	    216,	256,	425,	552,	496,	440,	329,	184};

void *connection_handler(void *);

int sendBits(int * bit_array)
{
  for(int i = 0; i < 9; i++)
  {
    digitalWrite(SCLK, 0);
    digitalWrite(DATA, bit_array[i]);
    digitalWrite(SCLK, 1);
  }
  digitalWrite(SCLK, 0);
  return 0;
}

int applyConfig(int mapped_bits[NBITS])
{
  int bits_loaded;
  digitalWrite(RW, 1);
  int res[9];
  for(int i = 0; i < 64; i++)
  {
    for(int k = 0; k < 9; k++)
    {
      res[k] = mapped_bits[i*9 + k];
    }
    sendBits(res);
  }
  digitalWrite(RW, 0);
  digitalWrite(SCLK, 1);
  digitalWrite(SCLK, 0);
  int timeout_count = 0;
  while(1)
  {
    bits_loaded = digitalRead(FB);
    if(bits_loaded == 1){ printf(" :: Configuration set \n"); break; }
    timeout_count = timeout_count + 1;
    if(timeout_count == 10000){ printf(" :: Timeout \n"); break;}
  }
  return 0;
}

// Enable GPIO  to interface with FPGA
int initGPIO()
{
  wiringPiSetup();      // Board:
  pinMode(DATA, OUTPUT);   // 5 - DATA
  pinMode(SCLK, OUTPUT);   // 15 - SCLK
  pinMode(RW, OUTPUT);   // 7  - RW
  pinMode(FB, INPUT);  // 10 - FB
  pinMode(DUMMY, OUTPUT);  // Force short delay
  return 0;
}

// String of bits to array of binary integers
int * stringToArray(char * bitstream)
{
 static int unmapped_bits[NBITS];
 for(int i = 0; i < NBITS; i++)
 {
   unmapped_bits[i] = bitstream[i] - '0';
 }
 return unmapped_bits;
}


// Reorganise bits to match physical shift register outputs
int * mapBits(int * bit_array)
{
 static int sequence[NBITS];

 for (int q = 0; q < NBITS; q++)
 {
   sequence[q] = bit_array[map[q]-1];
 }
 return sequence;
}


int main(int argc , char *argv[]){
	// IRS control
  initGPIO();


	int socket_desc , new_socket , c , *new_sock;
	struct sockaddr_in server , client;
	char *message;

	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1) printf("Could not create socket");

	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons( 8888 );

	//Bind
	if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0){
		puts("bind failed");
		return 1;
	}
	puts("bind done");

	//Listen
	listen(socket_desc , 3);

	//Accept and incoming connection
	puts(" :: Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while ((new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c))){
		puts(" :: Connection accepted");


		pthread_t sniffer_thread;
		new_sock = (int*)malloc(1);
		*new_sock = new_socket;

		if( pthread_create( &sniffer_thread , NULL ,  connection_handler , (void*) new_sock) < 0){
			perror("could not create thread");
			return 1;
		}

		//Now join the thread , so that we dont terminate before the thread
		pthread_join( sniffer_thread , NULL);
		puts(" :: Handler assigned");
	}

	if (new_socket<0){
		perror("accept failed");
		return 1;
	}

	return 0;
}

/*
 * This will handle connection for each client
 * */
 /*
  * This will handle connection for each client
  * */
 void *connection_handler(void *socket_desc)
 {
  // IRS control:
	// When connection established, connection handler is run
	// 1. Send ACK to user 'a'
	// 2. Wait for config
	// 3. Apply config and reply with ACK


 	//Get the socket descriptor
 	int sock = *(int*)socket_desc;
 	int read_size;
 	char *message , client_message[2000];
  char config[577] = {0};

  // IRS control
	int * unmapped_bits;
	int * mapped_bits;



  // send initial ACK
  write(sock, "a", strlen("a"));

 	//Receive a message from client
 	while ((read_size = recv(sock,client_message, 2000 , 0)) > 0){
 		//Send the message back to client
    puts("Received message");
		if (strlen(client_message) >= 576){
		//puts(client_message);
		memcpy(config, client_message, 576);
		config[576] = 0;
		puts(config);

		unmapped_bits = stringToArray(config);
		mapped_bits = mapBits(unmapped_bits);
		applyConfig(mapped_bits);

		write(sock, "a", strlen("a"));
	}

 		//write(sock , client_message , strlen(client_message));
 	}

 	if(read_size == 0){
 		puts("Client disconnected");
 		fflush(stdout);
 	}
 	else if(read_size == -1){
 		perror("recv failed");
 	}

 	//Free the socket pointer
 	free(socket_desc);

 	return 0;
 }
