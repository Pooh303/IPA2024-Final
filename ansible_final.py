import subprocess

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', '/ansible/playbook.yml']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    output = result.stdout
    if 'ok=2' in result:
        return "Playbook executed successfully."
    else:
        return "Error running playbook. Output:\n" + output
    