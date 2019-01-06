import subprocess


def migrate():
    bashCommand = 'cd migrations &python user.py & for f in *.py; do python "$f"; done'
    subprocess.run(bashCommand)
    #   output, error = process.communicate()

