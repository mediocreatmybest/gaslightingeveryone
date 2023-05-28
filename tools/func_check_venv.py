import os
import sys

def activate_venv():
    # Find Script path, so we can locate venv
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set directory path for venv
    venv_dir = os.path.join(script_dir, 'venv')

    # Check if the venv directory exists
    if os.path.isdir(venv_dir):
        # Check for Windows / or *nix systems
        if sys.platform.startswith('win'):  # Windows
            venv_activate = os.path.join(venv_dir, 'Scripts', 'activate.bat')
            activate_cmd = f'call "{venv_activate}"'
        else:  # Linux/*nix
            venv_activate = os.path.join(venv_dir, 'bin', 'activate')
            activate_cmd = f'source "{venv_activate}"'

        # Activate the system!
        os.system(activate_cmd)