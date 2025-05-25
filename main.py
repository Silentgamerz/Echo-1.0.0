# -*- coding: utf-8 -*-

import sys, os
import subprocess

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

def get_dir():
    script_path = os.path.join(parent_folder_path, 'get-dir.ps1')
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    output = result.stdout.strip()
    return output


class EchoFileCreator(FlowLauncher):
    def query(self, query):
        args = query.strip().split()
        location = get_dir()

        if len(args) < 2:
            return [{
                "Title": "Please provide a filename and extension",
                "SubTitle": "Usage: echo <extension> <filename>",
                "IcoPath": "Images\\app.png"
            }]

        extension = args[0]
        filename = args[1]

        if len(args) >= 3:
            location = ' '.join(args[2:])

        subtitle = f"Location: {location}"

        return [{
            "Title": f"File to be created: {filename}.{extension}",
            "SubTitle": subtitle,
            "IcoPath": "Images/icon.png",
            "JsonRPCAction": {
                "method": "create_file",
                "parameters": [extension, filename, location],
                "dontHideAfterAction": False
            }
        }]

    def create_file(self, extension, filename, location):
            full_path = os.path.join(location, f"{filename}.{extension}")
            # Create the dir if it doesn't exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create the file
            with open(full_path, 'w') as f:
                f.write('')

if __name__ == "__main__":
    EchoFileCreator()