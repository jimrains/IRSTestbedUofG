#!~!~!#
##############################
##############################
##############################
import threading
from threading import Thread
import time
import socket
import select
import random
import numpy as np

from xmlrpc import client
import sys
import os
import datetime

##############################
##############################
##############################
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: rusty
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import qtgui

class sweep(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "sweep")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e6
        self.freq = freq = 3e9

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0_0.set_gain(15, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        # No synchronization enforced.
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Relative magnitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_probe_signal_x_0_0 = blocks.probe_signal_f()
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(samp_rate/1000), 1, 4000, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_probe_signal_x_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_complex_to_mag_squared_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "sweep")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.samp_rate/1000), 1)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0_0.set_center_freq(self.freq, 0)



def main(top_block_cls=sweep, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()
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

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
