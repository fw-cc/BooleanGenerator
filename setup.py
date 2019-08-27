import sys
import subprocess


def install_package(package_name):
    subprocess.call([sys.executable, "-m", "pip", "install", package_name])


def install_from_requirements(file_path: str):
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    try:
        with open(file_path, "r") as requirements_obj:
            for line in requirements_obj.readlines():
                install_package(line.split("==")[0])
    except NameError:
        print("Improper path to requirements.txt given.")


if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Minimum Python version: 3.7.0"
    install_from_requirements("./requirements.txt")
