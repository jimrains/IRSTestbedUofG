#
#   grcinsert.py: Insert blocks of code into compiled GNURadio flowgraphs
#
#   Useful for development of programs utilising GRC signal processing where
#   changes in signal processing chains is required.
#
#   Enter required imports and global variables into 'HEADER.py'
#   Place thread to run alongside flowgraph into 'BODY.py'
#
#   Usage: insert_grc.py <flowgraph python file> <header file> <body file>

import os,sys

def main():
#    inpath = "TEST.py"

    if len(sys.argv) == 1:
        print("\nProgram requires compiled GNURadio flowgraph as an input")
        print("\nUsage: grcinsert.py <compiled flowgraph> <header file> <body file>")
        print("\nHeader file contents are inserted into the start of the GRC flowgraph")
        print("\nBody file contents are inserted into the main loop of the GRC flowgraph\n")
        sys.exit()
    if len(sys.argv) < 4:
        header_file = "HEADER.py"
        body_file = "BODY.py"
        inpath = sys.argv[1]
    else:
        inpath = sys.argv[1]
        header_file = sys.argv[2]
        body_file = sys.argv[3]

    with open("temp.py", "w") as outfile:
        with open(inpath) as infile:
            if infile.readline() == "#!~!~!#\n":
                print("#!~!~!# File has already been processed - recompile in GNURadio and try again")
                outfile.write("#!~!~!#\n")
                sys.exit()
            else:
                outfile.write("#!~!~!#\n")
            with open(header_file) as headerfile:
                for line in headerfile:
                    outfile.write(line)
            for line in infile:
                outfile.write(line)
                if line == "    tb.show()\n":
                    with open(body_file) as bodyfile:
                        for inserted_line in bodyfile:
                            outfile.write("    " + inserted_line)
    os.replace(outfile.name, inpath)
    print("done")

main()
