from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def hello():
  return render_template('index.html')

@socketio.on('boton_rojo')
def boton_rojo():
    print 'boton rojo pulsado\n'

if __name__ == '__main__':
  #app.run(host='0.0.0.0', port=5000, debug=True)
  socketio.run(app, host='0.0.0.0', port=5000, debug=True)
