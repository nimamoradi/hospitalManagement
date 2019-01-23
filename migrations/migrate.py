import subprocess



# def migrate():
bashCommand = 'for %f in (*.py) do python %f'
subprocess.run(bashCommand)
# output, error = process.communicate()


