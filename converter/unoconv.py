"""Unoconv Interface"""
import subprocess
import tempfile

class UnoconvConverter():
    """Wrapper around making os commands to unoconv"""

    __unoconv_bin = 'unoconv'

    def convert(self, file, input_format, output_format):
        """Convert bytes from one format to another."""
        temp_path = tempfile.NamedTemporaryFile(suffix=".%s" % (input_format, ))
        temp_path.write(file)
        temp_path.flush()

        command = self.__make_cmd(output_format, temp_path.name)
        proc = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        data, stderrdata = proc.communicate()

        if stderrdata:
            raise Exception(str(stderrdata))

        temp_path.close()

        return data

    def __make_cmd(self, output_fmt, tmp_path):
        return [
            self.__unoconv_bin,
            '--stdout',
            '-e',
            'UseLosslessCompression=false',
            '-e',
            'ReduceImageResolution=false',
            '--format',
            output_fmt,
            tmp_path
        ]
