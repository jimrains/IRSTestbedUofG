
# TOOLS: for IRS testbed-related development

## grcinsert

Program to insert snippets of code into the header and body of a compiled GNURadio flowgraph.

This is useful for developing programs which externally control or rely on GNURadio signal processing functions, particularly when several changes to the flowgraph are required.

Usage:

`insert_grc.py <compiled flowgraph> <header file> <body file>`

Example (files included in directory):

`insert_grc.py TEST.py HEADER.py BODY.py`
