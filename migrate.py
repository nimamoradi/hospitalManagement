
import subprocess

bashCommand = 'cd migrations &python user.py & for f in *.py; do python "$f"; done'
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()