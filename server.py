#!/usr/bin/env python

"""
Kindle VNC Server 1.0
(c) 2016 Jerzy Glowacki
Apache 2.0 License
"""

import SimpleHTTPServer
import SocketServer
import socket
import os
import wx

HOST = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
PORT = 5900
FILENAME = '/dev/shm/frame.jpg'
QUALITY = 50
ROTATE = True
GRAYSCALE = True
OPTIMIZE = True
W = 700
H = 600
X = 0
Y = 0

class VNCServer(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def getFrame(self):
        app = wx.PySimpleApp()
        bmp = wx.EmptyBitmap(W, H, -1)
        mem = wx.MemoryDC()
        mem.SelectObject(bmp)
        mem.Blit(0, 0, W, H, wx.ScreenDC(), X, Y)
        mem.SelectObject(wx.NullBitmap)
        img = wx.ImageFromBitmap(bmp)
        if GRAYSCALE:
            img = img.ConvertToGreyscale()
        if ROTATE:
            img = img.Rotate90()
        img.SetOptionInt(wx.IMAGE_OPTION_QUALITY, QUALITY)
        img.SaveFile(FILENAME, wx.BITMAP_TYPE_JPEG)
        if OPTIMIZE:
            os.system('jpegtran -optimize -progressive ' + ('', '-grayscale ')[GRAYSCALE] + '-copy none -outfile ' + FILENAME + ' ' + FILENAME)
    def do_GET(self):
        self.path = self.path.split('?')[0]
        if self.path == '/frame.jpg':
            self.getFrame()
            with open(FILENAME, 'rb') as frame:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(frame.read())
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    httpd = SocketServer.TCPServer((HOST, PORT), VNCServer)
    httpd.allow_reuse_address = True
    print 'Kindle VNC Server started at http://%s:%s' % (HOST, PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
       pass
    httpd.server_close()
    print 'Server stopped'