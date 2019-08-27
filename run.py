import gui
import setup
import os.path
import json
import sys

if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Minimum Python version: 3.7.0"
    if not os.path.exists("./configinfo.json"):
        with open("./configinfo.json", "w") as configinfo_json:
            json.dump({"first_time_setup": False}, configinfo_json, indent=4)

    with open("./configinfo.json", "r") as configinfo_json:
        loaded_json_obj = json.load(configinfo_json)
        try:
            if not loaded_json_obj["first_time_setup"]:
                # if input("Would you like to run the first-time setup for this program? (y/n): ").lower() == "y":
                print("Running first-time-setup, ensure you have a stable internet connection.")
                setup.install_from_requirements("./requirements.txt")
                loaded_json_obj["first_time_setup"] = True
                print("First time setup complete.")
                # else:
                #     print("To install packages required for this program, run ./setup.py, found in this folder.")
        except KeyError:
            loaded_json_obj = {"first_time_setup": False}

    with open("./configinfo.json", "w") as configinfo_json:
        json.dump(loaded_json_obj, configinfo_json, indent=4)

    gui_object = gui.MainGUI()
