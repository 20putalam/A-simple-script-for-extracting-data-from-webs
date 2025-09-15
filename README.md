# A simple script for extracting data from webs

Simple program for extracting data from webs made with Python 3.12.

## Autor

Marek Putala, Ing.

## Prerequisites

To successfully run this application, it is first necessary to install Python on the given device. If the current device does not have Python fully installed, it can be installed on UNIX systems by entering a command into the command line as follows:
* First, it is recommended to update all other libraries on the system:
  ```sh
  sudo apt update

* Then, proceed with installing the Python software:
  ```sh
  sudo apt install python3

* After installation is complete, the functionality can be verified by opening the Command Prompt and entering the following command:
  ```sh
  python3 --version

If the current device is running Windows and does not have Python fully installed, it can be installed in the following way:

* First, download the official Python installer from the Python website:
https://www.python.org/downloads/windows/

* Run the downloaded installer and make sure to select the option “Add Python to PATH” during installation so that Python can be accessed from the command line.

* After installation is complete, the functionality can be verified by opening the Command Prompt and entering the following command:
    ```bat
    python --version

* After installation is complete, the functionality can be verified by opening the Command Prompt and entering the following command:
  ```sh
  python3 --version

The library also uses the external libraries requests and beautifulsoup4 for handling HTTP requests and parsing HTML. For proper functionality, it is therefore necessary to install these libraries if they are not already present on the device.

* First, it is recommended to update all other libraries on the system:
  ```sh
  sudo apt update

* Then, proceed with the installation of the required Python libraries:
  ```sh
  python3 -m pip install requests beautifulsoup4

## Running the Application

The application is launched using the main script run.py, which then executes either the main program modules or the test modules.

* Command to run the script:
  ```sh
  python3 run.py

The behavior of the application can be modified using a set of arguments:

- `--test`
  Runs the unit tests instead of the main program. This is useful for verifying that the code works as expected before running it on real input data.
- `-i <path>`, `--input <path>`  
  Specifies the path to a file containing URLs to process.
  * If this argument is not provided, the program will read URLs from standard input (stdin).
- `-o`, `--output <path>`  
  Specifies the path to a file where the results should be saved.

  * If this argument is not provided, the results will be printed to standard output (stdout).

You can immediately launch the application with this command.

  ```sh
  python3 run.py -o output_example < input_example
