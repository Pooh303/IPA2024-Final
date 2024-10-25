import subprocess
import os

def showrun():
    student_id = "65070182"  # Replace with your actual student ID
    router_name = "CSR1KV-Pod1-3"  # Replace with your router name
    filename = f"show_run_{student_id}_{router_name}.txt"

    command = ['ansible-playbook', '/ansible/playbook.yml']
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:  # Check for successful execution
        # Check if the file exists before returning 'ok'
        if os.path.exists(filename):
            return "ok"  # Signal to ipa2024_final.py to attach the file
        else:
            return f"Error: Output file '{filename}' not found." 
    else:
        return "Error: Ansible\n" + result.stderr  # Return stderr for debugging