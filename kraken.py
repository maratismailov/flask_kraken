from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import glob
import os
import lxml.etree as ET
import json
from zipfile import ZipFile

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
    filename_unzipped = filename[:-4]
    # print(myfile.headers.get('Content-Disposition'))
    open(filename, 'wb').write(myfile.content)
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall()
    return send_file(filename_unzipped, mimetype='text/html', as_attachment=True, attachment_filename=filename_unzipped)

@app.route('/html/<path:url>')
def html(url):
    removedownloads()
    myfile = requests.get(url, allow_redirects=True)
    content = myfile.headers.get('Content-Disposition')
    pre_filename = content[22:]
    filename = pre_filename[:-1]
    filename_unzipped = filename[:-4]
    open(filename, 'wb').write(myfile.content)
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall()
    dom = ET.parse(filename_unzipped)
    xslt = ET.parse('./FB2_2_xhtml.xsl')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    return ET.tounicode(newdom, pretty_print=True)


@app.route('/test/<path:url>')
def test(url):
    removedownloads()
    myfile = requests.get(url, allow_redirects=True)
    content = myfile.headers.get('Content-Disposition')
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
    zips = json.dumps(glob.glob('./*.zip'))
    fb2s = json.dumps(glob.glob('./*.fb2'))
    return jsonify(zips + fb2s)


def removedownloads():
    dir_name = "./"
    filestoremove = os.listdir(dir_name)
    for item in filestoremove:
        if item.endswith(".zip"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".fb2"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".epub"):
            os.remove(os.path.join(dir_name, item))
        elif item.endswith(".mobi"):
            os.remove(os.path.join(dir_name, item))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
