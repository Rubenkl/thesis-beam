import Socket

socket = Socket.Connection()
socket.wait(5)
socket2 = Socket.Connection()
socket.sendClassify('updown', 135)
socket.wait(5)
socket.sendClassify('fininshed', 125)