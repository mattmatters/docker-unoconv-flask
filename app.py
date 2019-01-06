"""Document Coverter API"""
import os
import subprocess
import tempfile

from flask import Flask, request
from flask.helpers import make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024 # 60mb

class UnoconvConverter(object):
    def convert(self, file, input_format, output_format):
        temp_path = tempfile.NamedTemporaryFile(suffix=".%s" % (input_format, ))
        temp_path.write(file)
        temp_path.flush()

        unoconv_bin = 'unoconv'
        command = [
            unoconv_bin,
            '--stdout',
            '-e',
            'UseLosslessCompression=false',
            '-e',
            'ReduceImageResolution=false',
            '--format',
            output_format,
            temp_path.name
        ]

        p = subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data, stderrdata = p.communicate()

        if stderrdata:
            raise Exception(str(stderrdata))

        temp_path.close()

        return data

@app.route('/convert/<string:output_format>', methods=['POST'])
def convert(output_format):
        file = request.files['file']
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1][1:]
        converter = UnoconvConverter()

        raw_bytes = converter.convert(file.read(), extension, output_format)
        response = make_response(raw_bytes)
        response.headers['Content-Type'] = "application/octet-stream"
        response.headers['Content-Disposition'] = "inline; filename=" + filename + ".%s" % (output_format, )
        return response
