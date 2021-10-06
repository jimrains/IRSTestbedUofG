
import datetime
import os

def generate_filename(frequency, function):
    DT = datetime.datetime.now()
    fn1 = str(DT.year) + str(DT.month) + str(DT.day)
    fn2 = "_" + str(DT.hour) + str(DT.minute) + str(DT.second)
    fn3 = "_" + function + "_"
    fn4 = str(frequency) + ".dat"
    return fn1+fn2+fn3+fn4

#print(generate_filename(3000, "OPT"))
#print(generate_filename(2760, "SWEEP"))

def write_config_data(frequency, start_power, end_power, config, filename):
    datout = str(frequency) + " " + str(start_power) + " " + str(end_power)
    datout = datout + " " + ''.join(str(int(e)) for e in config)
    f = open(filename, "w")
    f.write(datout + "\n")

def format_sweep_data(opt_freq, cur_freq, power):
    return str(opt_freq) + " " + str(cur_freq) + " " + str(power)


opt_freq = 3300
cur_freq = 3600
power = -7
conf = ["1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0"]
s_power = 30
e_power = 50


DT = datetime.datetime.now()
dir_name = str(DT.year) + str(DT.month) + str(DT.day) + "/"
try:
    os.mkdir(dir_name)
except FileExistsError:
    print(" :: Directory exists - skipping ")
SF = open(dir_name + generate_filename(opt_freq, "SWEEP"), "w")
config_filename = dir_name + generate_filename(cur_freq, "OPT")

write_config_data(cur_freq, s_power, e_power, conf, config_filename)

for cur_freq in range(1000, 10000, 2):
    SF.write(format_sweep_data(opt_freq, cur_freq, power) + "\n")
