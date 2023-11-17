import subprocess

from InquirerPy.utils import color_print

from cloudboot.enum.ColorCode import ColorCode


def execute(cmd):
    """Execute CLI commands.

    Runs a command synchronously and returns the output. Errors will be printed to the console.

    Parameters
    -----------------------
    cmd: str
        CLI command which requires to be executed.

    Returns
    -----------------------
    object: Tuple
        succeeded: bool
            Status of the executed command.
        result: any
            Output captured from the command execution.
    """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, error = process.communicate()
    if process.returncode != 0:
        color_print([(ColorCode.ERROR, output.decode().strip())])
        return False, output.decode()
    return True, output.decode()
