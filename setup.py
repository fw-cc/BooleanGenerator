import sys
import subprocess

try:
    import urllib3.exceptions
except ModuleNotFoundError:
    subprocess.call([sys.executable, "-m", "pip", "install", "urllib3"])
    import urllib3.exceptions


def install_package(package_name, install_attempt_counter=1):
    print(f"Install attempt {install_attempt_counter} {package_name}")
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", package_name])
    except urllib3.exceptions.ReadTimeoutError:
        if install_attempt_counter > 5:
            print(f"{package_name} install timeout.")
            exit()
        else:
            install_package(package_name, install_attempt_counter+1)


def install_from_requirements(file_path: str):
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    try:
        with open(file_path, "r") as requirements_obj:
            for line in requirements_obj.readlines():
                install_package(line.split("==")[0])
    except NameError:
        print("Improper path to requirements.txt given.")


if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Minimum Python version: 3.7"
    install_from_requirements("./requirements.txt")
