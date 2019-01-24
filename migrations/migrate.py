import subprocess
import os


def migrate():
    # bashCommand = 'for %f in (.\migrations\*.py) do python .\migrations\%f'
    # subprocess.run(bashCommand)
    # specify your cmd command
    # subprocess.call(['c'])
    o = os.popen(
        'for %f in (.\migrations\*.py) do python %f').read()
    print(o)
    # output, error = process.communicate()


