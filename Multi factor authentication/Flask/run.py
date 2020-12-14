from MFA import socketio, app

if __name__ == '__main__':
    socketio.run(app,debug=True)


'''
from flask_app import app, cer, key
#to let the app run with python "filename.py" and enable debug mode for sync changes
if __name__=='__main__':
    app.run(host='0.0.0.0', port='443', ssl_context=context, debug=True)

'''