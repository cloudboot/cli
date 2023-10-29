import subprocess

from InquirerPy.utils import color_print


def execute(cmd):
    """Runs a command synchronously and returns the output."""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, error = process.communicate()
    if process.returncode != 0:
        color_print([('#ffc1cc', output.decode())])
    return output.decode()
