from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello world'

@app.route('/download/<path:url>')
def download(url):
    print('url is ', url)
    myfile = requests.get(url, allow_redirects=True)
    content = myfile.headers.get('Content-Disposition')
    print('content is ', content)
    pre_filename = content[22:]
    filename = pre_filename[:-1]
    print(myfile.headers.get('Content-Disposition'))
    open(filename, 'wb').write(myfile.content)
    return send_file(filename, mimetype='application/zip', as_attachment=True, attachment_filename=filename)

@app.route('/test/<path:url>')
def test(url):
    myfile = requests.get(url, allow_redirects=True)
    content = myfile.headers.get('Content-Disposition')
    print('content is ', content)
    pre_filename = content[22:]
    filename = pre_filename[:-1]
    print(myfile.headers.get('Content-Disposition'))
    # open(filename, 'wb').write(myfile.content)
    # return send_file(filename, mimetype='application/zip', as_attachment=True, attachment_filename=filename)
    return filename

@app.route('/download/test')
def testdownload():
    filename = 'test.mp4'
    return send_file(filename, as_attachment=True, attachment_filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
