### Frequency sweep with pi
### Sets frequency on Tx side, measures received power, and so on.
### Saves points in text file with unique name outlining frequency, magnitude, timestamp, date
###

# create filename from time stamp, date, and GPS
# Set tx Frequency
# Set rx Frequency
# wait a sec
# take averaged power measurements
# write to file

# args: freq_s, freq_f, step (MHz)


def format_sweep_data(opt_freq, cur_freq, power):
    return str(opt_freq) + " " + str(cur_freq) + " " + str(power)

def generate_filename(frequency, function):
    DT = datetime.datetime.now()
    fn1 = str(DT.year) + str(DT.month) + str(DT.day)
    fn2 = "_" + str(DT.hour) + str(DT.minute) + str(DT.second)
    fn3 = "_" + function + "_"
    fn4 = str(frequency) + ".dat"
    return fn1+fn2+fn3+fn4

def mainLoop():
    print(" :: Frequency sweep ")
    rpcs = client.Server('http://192.168.4.3:8080')

    if len(sys.argv) != 5:
        print(" :: Frequency sweep usage: sweep.py start_freq end_freq step_size opt_freq")
        sys.exit()
    start_freq = int(sys.argv[1])
    end_freq = int(sys.argv[2])
    step_size = int(sys.argv[3])
    opt_freq = int(sys.argv[4])
    ####### Set up file information for logging
    DT = datetime.datetime.now()
    dir_name = str(DT.year) + str(DT.month) + str(DT.day) + "/"
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print(" :: Directory exists - skipping ")
    SF = open(dir_name + generate_filename(opt_freq, "SWEEP"), "w")
    #######


    print(" :: IRS optimised at: ", opt_freq, " MHz ")
    print(" :: Range: ", start_freq, " MHz - ", end_freq, " MHz | Step size: ", step_size, " MHz")
    print(" :: Starting sweep: ")

    avg_length = 500

    for frequency in range(start_freq, end_freq + step_size, step_size):
        print(" :: Frequency: ", frequency, " MHz ")
        rpcs.set_txfreq(frequency)
        tb.set_freq(frequency*1000000)
        time.sleep(1)
        print(" :: Set: ", rpcs.get_txfreq())
        PWR = 0
        for i in range(1, avg_length + 1, 1):
            PWR = PWR + tb.blocks_probe_signal_x_0_0.level()
            time.sleep(1/avg_length)
        PWR = PWR/avg_length
        SF.write(format_sweep_data(opt_freq, frequency, 10*np.log10(PWR)) + "\n")
        print(" :: Relative power: ", 10*np.log10(PWR), " dB")

    print(" :: DONE ")
    os.system('play -nq -t alsa synth {} sine {}'.format(1, 400))
    SF.close()
    tb.stop()
    sys.exit()

uiThread = Thread(target=mainLoop, args=())
uiThread.start()
############################################
############################################
############################################
############################################
############################################
