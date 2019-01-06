"""Document Coverter API"""
import os
from flask import Flask, request
from flask.helpers import make_response
from werkzeug.utils import secure_filename
from converter.unoconv import UnoconvConverter

app = Flask(__name__) # pylint: disable=invalid-name
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024 # 60mb

@app.route('/convert/<string:output_format>', methods=['POST'])
def convert(output_format):
    """Convert a form file upload to desired output format"""
    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1][1:]
    converter = UnoconvConverter()

    raw_bytes = converter.convert(file.read(), extension, output_format)
    res = make_response(raw_bytes)
    res.headers['Content-Type'] = "application/octet-stream"
    res.headers['Content-Disposition'] = "inline; filename=" + filename + ".%s" % (output_format, )
    return res
