import os
import configparser
import subprocess

def install_dependencies():
    # Install dependencies from requirements.txt
    with open('requirements.txt', 'r') as requirements_file:
        dependencies = requirements_file.read().splitlines()

    print('Installing dependencies...', end='', flush=True)
    for dependency in dependencies:
        subprocess.check_call(["pip", "install", dependency], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('DONE')

def create_folders(config):
    # Create folders based on configuration
    directories_section = config['directories']
    folders_to_create = [value for value in directories_section.values()]

    print('Managing directories...', end='', flush=True)
    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)
    print('DONE')

def main():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config/config.ini'))

    # Install dependencies
    install_dependencies()

    # Create folders based on configuration
    create_folders(config)

    print('ALL DONE')

if __name__ == "__main__":
    main()
