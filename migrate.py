import subprocess


def migrate():
    bashCommand = 'cd migrations &python user.py & for f in *.py; do python "$f"; done'
    subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #   output, error = process.communicate()

