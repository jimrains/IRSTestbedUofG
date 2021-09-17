############################################
##### added via insert_grc #################
############################################


# Enter loop to run alongside flowgraph here
# The example code takes a sample from a probe signal and prints the Rx power
def mainLoop():
    while 1:
        RXpower = tb.blocks_probe_signal_x_0_0.level()
        print("Received power: ", RXpower)
        time.sleep(3)

uiThread = Thread(target=mainLoop, args=())
uiThread.start()



############################################
##### \ insert_grc #########################
############################################
