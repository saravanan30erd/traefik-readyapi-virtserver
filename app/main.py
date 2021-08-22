from flask import Flask, jsonify, request
import socket

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def check_health():
    return jsonify({'status' : 'OK', 'hostname' : socket.gethostname()}), 200

## Custom HTTP status error handler ##
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(500)
def interval_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=3000)
