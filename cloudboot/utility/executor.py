import subprocess


def execute(cmd):
    """Runs a command synchronously and returns the output."""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception(error.decode())
    return output.decode()
