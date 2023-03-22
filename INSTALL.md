# Installation

<p align="center">
    <img height='250' src="rsrcs/FSSC_icon.png" />
</p>

In the following sections, the available installation methods and instructions are provided.

## Index
- [Installation](#installation)
  - [Index](#index)
  - [From releases (Just Windows for the moment) -- Alpha release](#from-releases-just-windows-for-the-moment----alpha-release)
    - [Full-Installation](#full-installation)
  - [From sources (Linux, OSX, Windows)](#from-sources-linux-osx-windows)
    - [Requirements](#requirements)
      - [pipenv installation](#pipenv-installation)
      - [pip installation](#pip-installation)
    - [Post installation](#post-installation)

## From releases (Just Windows for the moment) -- Alpha release

The easiest way to run the software is to download the package version from the [Releases](https://github.com/Wauro21/sspc/releases). At the time of writting this guide version `v0.1.0-alpha` have just been released!

In the release section you will find three files, a zip-file corresponding to the full-installation (`SSPC.zip`) along with two files corresponding to the source code (zip and tar).

### Full-Installation

Download SSPC.zip and unzip it where you want it. Inside there will be a SSPC folder, inside are all the files needed to run the program (including all the LICENSES from third party libraries and SSPC itself). Just search for the executable: SSPC.exe and the program should launch.

![example-full-installation-windows]()

You can put the folder anywhere you want, and then generate a desktop shortcut of `SSPC.exe`.

## From sources (Linux, OSX, Windows)

To install from sources you only need a copy of this repository!

### Requirements

The software was developed using `Python 3.8`, and all of the following dependencies are listed with this version in mind. However, it is possible that the software is compatible with newer versions of the interpreter and dependencies. This includes the Pipfiles and requirements.txt files.

| **Dependency** | **Version** | **Description** | **License**|
|----------------|-------------|-----------------|------------|
| PySide2 | 5.15.2.1 | Used to build the GUI | [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html)|
| Pyserial | 3.5 | Used for serial communication | [BSD](https://github.com/pyserial/pyserial/blob/master/LICENSE.txt) |
| altgraph | 0.17.3 | Used by Pyserial | [MIT](https://github.com/ronaldoussoren/altgraph/blob/master/LICENSE)|
| numpy | 1.24.2 | Used for numerical operations | [BSD](https://github.com/numpy/numpy/blob/main/LICENSE.txt) [External](https://github.com/numpy/numpy/blob/main/LICENSES_bundled.txt) | 
| shiboken2 | 5.15.2.1 | Used by PySide2 | [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html) |


**\* External refers to third-party software used by the dependency itself.**

Although not requiered to run the software, this dependencies were used to compiled the package (`exe`) for Windows:

| **Dependency** | **Version** | **Description** |
|----------------|-------------|-----------------|
| pyinstaller | 5.9.0 | Package Windows application |
| pip-licenses | 4.1.0 | Try to understand what license can I use for this piece of software|


#### pipenv installation

To install the dependencies use the `Pipfile` and `Pipfile.lock` provided with the repository. Using the following command from the root of the project to install them:

```[bash]
$ pipenv install 
```

If you also want to install the `dev` dependencies (i.e to package for Windows), use the following command:

```
$ pipenv install -dev
```

After installation you need to activate the virtual environment running:

```[bash]
$ pipenv shell
```

#### pip installation

To install the dependencies use the `requirements.txt` provided with the repository. Using the following command from the roof of the project to install them: 

```[bash]
$ pip install -r requirements.txt
```

### Post installation

After installing the dependencies, you should be able to run the code. You can try to run it using the following commands from the root of the project.

```[bash]
$ python SSPC.py
```
![install-success]()
