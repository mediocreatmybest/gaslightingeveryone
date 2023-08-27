import re
import streamlit as st
import subprocess
from pathlib import Path


# Global dictionary for accepted script types
# Available script_types
# Global dictionary for accepted script types and their interpreters
script_types = {
    'Python': {
        'extensions': ['.py'],
        'interpreter': 'python'
    },
    'Perl': {
        'extensions': ['.pl'],
        'interpreter': 'perl'
    },
    'Batch': {
        'extensions': ['.bat'],
        'interpreter': None  # Batch files are executable on their own in Windows
    },
    'PowerShell': {
        'extensions': ['.ps1'],
        'interpreter': 'powershell'
    }
}

def extract_arguments(script_content, script_type=None):
    """
    Extracts the arguments from a script that uses argparse.
    Args:
         script_content (str): The content of the script.
    Returns:
         list: A list of dictionaries containing the details of each argument.
                 Each dictionary contains the following keys:
                 - name: The name of the argument.
                 - type: The type of the argument.
                 - default: The default value of the argument.
                 - action: The action of the argument.
                 - choices: The choices of the argument.
                 - help: The help message of the argument.
                 - metavar: The metavar of the argument.
                 - arg_type: The type of the argument (positional, optional, or flag).
                 - is_store_true: True if the argument has the 'store_true' action, False otherwise.
                 - is_store_false: True if the argument has the 'store_false' action, False otherwise.
    """
    # Start with Python
    if script_type == "Python":

        argparse_section = re.findall(r'parser\.add_argument\((.+?)\)', script_content, re.DOTALL)
        args_list = []
        for argument in argparse_section:
            arg_name_match = re.search(r'(\'(.*?)\'|\"(.*?)\")', argument)
            arg_type_match = re.search(r'type=(.*?),', argument)
            arg_default_match = re.search(r'default=(.*?)(,|$)', argument)
            arg_action_match = re.search(r'action=(\'|")(.*?)(\'|")(|$)', argument)
            arg_choices_match = re.search(r'choices=\[(.*?)\]', argument)
            arg_help_match = re.search(r'help=(\'(.*?)\'|\"(.*?)\")', argument)
            arg_metavar_match = re.search(r'metavar=(\'(.*?)\'|\"(.*?)\")', argument)

            if arg_name_match is None:
                continue

            name = arg_name_match.group(2)
            arg_type = None
            if name.startswith('-'):
                if name.startswith('--'):
                    arg_type = 'optional'
                else:
                    arg_type = 'flag'
            else:
                arg_type = 'positional'

            arg_default = arg_default_match.group(1) if arg_default_match and arg_default_match.group(1) not in ('None', None) else None
            arg_action = arg_action_match.group(2) if arg_action_match else None
            arg_choices = arg_choices_match.group(1) if arg_choices_match else None
            arg_help = arg_help_match.group(2) if arg_help_match else None
            arg_metavar = arg_metavar_match.group(2) if arg_metavar_match else None

            is_store_true = False
            is_store_false = False
            if arg_action == 'store_true':
                is_store_true = True
            elif arg_action == 'store_false':
                is_store_false = True

            arg_details = {
                'name': name,
                'type': arg_type_match.group(1) if arg_type_match else None,
                'default': arg_default,  # Keeps the argument even if default is None or 'None'
                'action': arg_action,
                'choices': arg_choices,
                'help': arg_help,
                'metavar': arg_metavar,
                'arg_type': arg_type,
                'is_store_true': is_store_true,
                'is_store_false': is_store_false
            }
            args_list.append(arg_details)

        return args_list

    # For script types without a defined extraction method, return a generic input
    return [{'name': 'Input', 'type': None, 'default': '', 'help': 'Provide input for the script', 'arg_type': 'optional'}]


def list_scripts(directory, exclude_patterns=None, extensions=None):
    """
    Lists all the scripts of the specified types in a directory, excluding patterns if specified.

    :param directory: Path object for the directory.
    :param exclude_patterns: List of string patterns to exclude.
    :param extensions: List of file extensions to include.
    :return: List of Path objects for the specified scripts.
    """
    if exclude_patterns:
        exclude_regex = re.compile('|'.join(exclude_patterns))
    else:
        exclude_regex = None

    # Convert the list to a set for efficient lookup
    extensions = set(extensions)

    return [f for f in directory.iterdir() if f.is_file() and f.suffix.lower() in extensions and (not exclude_regex or not exclude_regex.search(f.name))]


def create_input_fields(arguments, script_type=None):
    """
    Creates Streamlit input fields based on the arguments.

    :param arguments: List of dictionaries containing argument details.
    :return: Dictionary of input values.
    """
    inputs = {}

    # Start with Python input fields
    if script_type == "Python":

        for arg in arguments:
            if arg['is_store_true'] or arg['is_store_false'] or arg['type'] == 'bool':
                inputs[arg['name']] = st.checkbox(arg['name'],
                                                value=bool(arg['default']),
                                                help=arg['help'] or '')
            elif arg['choices']:
                choices = [""] + [choice.strip("' ") for choice in arg['choices'].split(',')]
                default_choice = arg['default'].strip("' ") if arg['default'] else None
                inputs[arg['name']] = st.selectbox(arg['name'],
                                                choices,
                                                index=choices.index(default_choice) if default_choice else 0, help=arg['help'] or '')

            else:
                default_value = arg['default'].strip("' ") if arg['default'] else ""
                inputs[arg['name']] = st.text_input(arg['name'],
                                                    value=default_value,
                                                    help=arg['help'] or '')

        return inputs

    return inputs


def generate_streamlit_interface(script_path, script_type):
    """
    Generates the entire Streamlit interface for the script.

    :param script_path: Path object pointing to the script.
    """
    with open(script_path, encoding='utf-8') as file:
        script_content = file.read()
    # Get the arguments from the script / pass on script_type
    arguments = extract_arguments(script_content, script_type)

    # Add info_box variable to collect any info for later
    info_box = ""
    # Set info_box to the string if "" otherwise add to it
    if info_box == "":
        info_box = arguments
    else:
        info_box += arguments
    # End info box

    inputs = create_input_fields(arguments, script_type)
    positional_args_order = [arg['name'] for arg in arguments if arg['arg_type'] == 'positional']
    if st.button("Run"):
        stdout, stderr = run_script(script_path, inputs, arguments, positional_args_order)
        st.text("Output:\n")
        st.code(stdout)
        if stderr:
            st.error(stderr)
    if st.button("Help"):
        cmd_args = ["python", str(script_path), "--help"]
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        st.text("Help:\n")
        st.code(result.stdout)

    #concat any info and pass to the return
    return info_box

def run_script(script_path, inputs, arguments, script_type, positional_args_order):
    """
    Runs the script using the provided inputs.

    :param script_path: Path to the script.
    :param inputs: Dictionary containing the input values.
    :param arguments: List of dictionaries with the argument details.
    :param positional_args_order: List of positional arguments in order.
    :return: stdout and stderr of the script execution.
    """
    interpreter = script_types[script_type]['interpreter']
    cmd_args = [interpreter, str(script_path)] if interpreter else [str(script_path)]
    #cmd_args = ["python", str(script_path)]  # Add "python3" to execute the script using Python
    for key in positional_args_order:  # Add positional arguments first
        value = inputs[key]
        if value:
            cmd_args.append(str(value))
    for arg in arguments:  # Iterate through arguments, not inputs
        key = arg['name']
        value = inputs[key]
        if key not in positional_args_order and (value or value is False):  # Skip positional arguments and None/empty strings
            if arg['is_store_true'] and value is True:
                cmd_args.append(key)
            elif arg['is_store_false'] and value is False:
                cmd_args.append(key)
            elif not (arg['is_store_true'] or arg['is_store_false']):
                cmd_args.append(key)
                cmd_args.append(str(value))

    st.text("Executing command:")
    st.code(" ".join(cmd_args))  # Display the command being executed
    result = subprocess.run(cmd_args, capture_output=True, text=True)
    return result.stdout, result.stderr


def main():
    """
    Main app to launch the Streamlit app.
    """
    # Top Title
    st.title("ScriptRunner")

    # Main script path is not recursive
    scripts_directory = Path("tools")
    # Exclude patterns of files, func, etc.
    exclude_patterns = ["func*", "test_func*"]
    # Create empty list for info_box
    info_box = []

    # Create a Streamlit sidebar with menu items / set script_type from dictionary
    script_type = st.sidebar.selectbox('Select script type', list(script_types.keys()), index=0)

    # Get the list of scripts from dictionary with get method
    available_scripts = list_scripts(scripts_directory, exclude_patterns, script_types[script_type]['extensions'])
    st.sidebar.text(f"Selected script type: {script_type}")
    #st.sidebar.text(f"Available scripts: {[script.name for script in available_scripts]}")

    selected_script_name = st.selectbox("Select script to run:", [script.name for script in available_scripts])

    if selected_script_name:
        selected_script_path = scripts_directory / selected_script_name
        # Pass args to the generate_streamlit_interface function including script_type
        args_info = generate_streamlit_interface(selected_script_path, script_type)

        # append any info together with new lines for info_box
        info_box.append('\nListed arguments are:\n')
        info_box.append(args_info)

        # append the scripts info to the info_box list
        info_box.append('\nAvailable scripts are:\n')
        info_box.append([script.name for script in available_scripts])

    # Set expander on the sidebar
    with st.sidebar:
        with st.expander("Info"):
            st.text('\n')
            st.write(info_box)

if __name__ == "__main__":
    main()
