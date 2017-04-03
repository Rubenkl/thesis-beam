from socketIO_client import SocketIO, LoggingNamespace

class Connection(object):
  SOCKET_URL = 'https://thesis-backend.ruub.eu'

  def on_connect(self):
    self.socket.emit('machinelearner')
    print("[SOCKET] Connected.")
    self.isConnected = True

  def on_disconnect(self):
    print("[SOCKET] Disconnected!")
    self.isConnected = False

  def on_reconnect(self):
    print("[SOCKET] Reconnected.")
    self.isConnected = True

  def sendClassify(self, gesture, BPM):
    ''' Sends out a JSON object of the classified gesture & BPM
    '''
    self.socket.emit('classify',"{ 'gesture': '" + gesture + "', 'bpm': " + str(BPM) + " }" )

  def __init__(self, type='Classify'):
    '''Creates a socket.io connection to connect with the server
    '''
    self.socket = SocketIO(self.SOCKET_URL,port=443, Namespace=LoggingNamespace)
    self.socket.on('connect', self.on_connect)
    self.socket.on('disconnect', self.on_disconnect)
    self.socket.on('reconnect', self.on_reconnect)

    self.isConnected = False

  def wait(self, time):
    self.socket.wait(time)
  

