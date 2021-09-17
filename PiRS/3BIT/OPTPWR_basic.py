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

host = '192.168.4.1'
port = 8080
##############################
##############################
##############################

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Optchannelgainoneusrp
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
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import qtgui


class OPTchannelGainONEUSRP(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Optchannelgainoneusrp")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Optchannelgainoneusrp")
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

        self.settings = Qt.QSettings("GNU Radio", "OPTchannelGainONEUSRP")

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
        self.samp_rate = samp_rate = 500e3
        self.cfreq = cfreq = 3.5e9

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("addr=192.168.11.2", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(cfreq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
            int(samp_rate), #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.001)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-100, -65)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
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
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            cfreq, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-100, -65)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                12e3,
                500,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(2500, 0.00001, 4000, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "OPTchannelGainONEUSRP")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 12e3, 500, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.cfreq, self.samp_rate)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_cfreq(self):
        return self.cfreq

    def set_cfreq(self, cfreq):
        self.cfreq = cfreq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.cfreq, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.cfreq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.cfreq, 1)



def main(top_block_cls=OPTchannelGainONEUSRP, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()
    ############################################
    ############################################
    ############################################
    ############################################
    ############################################
    ############################################
    ############################################

    def socketSetup():
        print('Creating socket...')
        # SOCK_STREAM is TCP
        try:
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
          print('failed.')
          sys.exit()

        print('Getting remote IP address')
        try:
            remote_ip = socket.gethostbyname(host)
        except socket.gaierror:
            print('Hostname could not be resolved')
            sys.exit()


        print('Connecting to server ' + host + ' (' + str(port) + ')')
        sock.connect((remote_ip, port))
        return sock

    def waitForAck(sock):
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            data = sock.recv(4096)
            if data.decode('utf-8') == 'a':
                return 0;
            else:
                return 1;

    def sendConfig(config, sock):
        rstr = ''.join(str(int(e)) for e in config)
        R = rstr.encode()
        try:
            sock.send(R)
        except socket.error:
            print('failed.')
            sys.exit()


    def mainLoop():
        #RXpower = tb.analog_probe_avg_mag_sqrd_x_0.level()
        PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]
        POWERS = [0,0,0,0,0,0,0,0]
        PDB = [0,0,0,0,0,0,0,0]
        time.sleep(3)

        s = socketSetup()
        waitForAck(s)
        y = ["0","0","0"]*192
        sendConfig(y, s)
        waitForAck(s)
        print("ACK received... please wait.")
        time.sleep(10)
        PWR = tb.blocks_probe_signal_x_0.level()
        best_PWR = PWR
        print(":: Starting power 1: ", 10*np.log10(PWR), " dB")
        time.sleep(1)
        PWR = tb.blocks_probe_signal_x_0.level()
        best_PWR = PWR
        print(":: Starting power 2: ", 10*np.log10(PWR), " dB")

        PDB[7] = 10*np.log10(PWR)
        #sleeptime = 0.015
        sleeptime = 0.005
        AL = 1
        power_samples = [0]*AL
        count = 0
        while 1:
            for nn in range(0,576,3):
                if (count%100 == 0) or count == 8:
                    print(count)
                    print(":: Current best power: ", 10*np.log10(max(POWERS)), " dB")
                    print(''.join(str(int(e)) for e in y))
                k = 0
                while k < 8:
                    count = count + 1
                    y[nn:nn+3] = PERMS[k]
                    sendConfig(y, s)
                    while waitForAck(s) == 1:
                        print("Socket fail")
                    time.sleep(sleeptime)
                    PWR = tb.blocks_probe_signal_x_0.level()
                    POWERS[k] = PWR
                    k = k + 1
                y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]

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
