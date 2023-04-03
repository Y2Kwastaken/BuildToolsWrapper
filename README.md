# BuildToolsWrapper


## Features

Build Tools wrapper is a simple wrapper script that provides a easy way to install and use BuildTools. it provides built in cacheing and support and allows you to easily choose your output directory etc.

## Why?
While the wrapper itself at the moment does not provide much, it is a good starting point for more features that are planned.

### What is planned?
* Support for downloading multiple spigot versions at once
* Support for downloading BungeeCord
* PaperMC and Waterfall support


## Installation

`git clone https://github.com/Y2Kwastaken/BuildToolsWrapper.git`

`cd BuildToolsWrapper`

`pip3 install -r requirements.txt`

`chmod +x btools`

## Usage

`./btools -h`
options:
    -h, --help            show this help message and exit
    -v, --version         The version of spigot to build
    --output-dir OUTPUT_DIR, -o OUTPUT_DIR 
                            The directory to output the jar to

## Adding to PATH
`cd`

`nano .bashrc` or `vim .bashrc`

add the following line to the end of the file:
`export PATH=$PATH:/path/to/BuildToolsWrapper`

`source .bashrc` or restart your terminal

`btools -h` should now work