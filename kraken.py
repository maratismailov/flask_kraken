from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import glob
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello world'


@app.route('/download/<path:url>')
def download(url):
    removedownloads()
    # print('url is ', url)
    myfile = requests.get(url, allow_redirects=True)
    content = myfile.headers.get('Content-Disposition')
    # print('content is ', content)
    pre_filename = content[22:]
    filename = pre_filename[:-1]
    print(myfile.headers.get('Content-Disposition'))
    open(filename, 'wb').write(myfile.content)
    return send_file(filename, mimetype='application/zip', as_attachment=True, attachment_filename=filename)

@app.route('/test/<path:url>')
def test(url):
    removedownloads()
    myfile = requests.get(url, allow_redirects=True)
    content = myfile.headers.get('Content-Disposition')
    print('content is ', content)
    pre_filename = content[22:]
    filename = pre_filename[:-1]
    print(myfile.headers.get('Content-Disposition'))
    return filename


@app.route('/download/test')
def testdownload():
    filename = 'test.mp4'
    return send_file(filename, as_attachment=True, attachment_filename=filename)


@app.route('/list')
def listfiles():
    return jsonify(glob.glob('./*.zip'))


def removedownloads():
    print('delete begin')
    dir_name = "./"
    filestoremove = os.listdir(dir_name)
    for item in filestoremove:
        if item.endswith(".zip"):
            os.remove(os.path.join(dir_name, item))
    print('delete success')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
