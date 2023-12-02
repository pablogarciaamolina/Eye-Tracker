import os
import configparser
from tqdm import tqdm
import subprocess

def install_dependencies():
    # Install dependencies from requirements.txt
    with open('requirements.txt', 'r') as requirements_file:
        dependencies = requirements_file.read().splitlines()

    for dependency in tqdm(dependencies, unit="package", desc="Installing dependencies"):
        subprocess.check_call(["pip", "install", dependency], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_folders(config):
    # Create folders based on configuration
    directories_section = config['directories']
    folders_to_create = [value for value in directories_section.values()]

    for folder in tqdm(folders_to_create, unit="folder", desc="Creating folders"):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")

def main():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config/config.ini'))

    # Install dependencies
    install_dependencies()

    # Create folders based on configuration
    create_folders(config)

    print("...DONE")

if __name__ == "__main__":
    main()
