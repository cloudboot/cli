import subprocess

from InquirerPy.utils import color_print

from cloudboot.enum.ColorCode import ColorCode


def execute(cmd):
    """Runs a command synchronously and returns the output."""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, error = process.communicate()
    if process.returncode != 0:
        color_print([(ColorCode.ERROR, output.decode())])
        return False, output.decode()
    return True, output.decode()
