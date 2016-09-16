Kindle VNC Server & Client
=======================

Simple VNC-like server and client for Kindle 3+ using plain old HTML. However, it does not use the RFB protocol, but a series of JPEG frames.

## Requirements

 - Python 2
 - wxPython
 - jpegtran (optional)

## Usage

Run `./server.py` and connect to `http://[local_address]:5900` using your Kindle's web browser. For configuration options look at the top of the `server.py` file.

## Screenshot

![Preview of Kindle VNC Client](http://i.imgur.com/pKdzviw.jpg)

## Author

Developed by Jerzy Głowacki under Apache 2.0 License
