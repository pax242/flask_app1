import eventlet

eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
from threading import Thread
import time

puerto = '/dev/ttyACM0'
baudrate = 115200

def serialThread():
    global end

    while not end:
        try:
            bytesInBuffer = serialPort.inWaiting()
        except:
            print 'Fallo en la comprobacion del puerto serie'

        if (bytesInBuffer > 0):
            try:
                mensaje = serialPort.read(bytesInBuffer)
            except:
                print 'Error de lectura del puerto serie'

        time.sleep(0.01)

try:
    serialPort = serial.Serial('/dev/ttyACM0', 115200)
    serialPort.flushInput()
    serialPort.flushOutput()
    end = False
except:
    print 'error al abrir el puerto', puerto
    end = True

thread = Thread(target=serialThread)
thread.daemon = True
thread.start()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,  async_mode = 'eventlet')

@app.route('/')
def index():
  return render_template('index.html')

@socketio.on('boton')
def button(led):
    c = str(led)
    try:
        serialPort.write(c)
    except:
        print 'Error en escritura del pureto serie'

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=5000, debug=True)
