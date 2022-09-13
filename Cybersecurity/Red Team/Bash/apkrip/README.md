This is a very rudimentary bash script that utilises [APKTool](https://github.com/iBotPeaches/Apktool) and [APKLeaks](https://github.com/dwisiswant0/apkleaks) to extract potentially exploitable API Keys/Secrets from `.apk` files.

## Notice
This script has not been thoroughly tested and may produce a number of errors. Use this script at your own risk - it is *definitely not* production-ready.

## Installation

1. Download [APKTool](https://github.com/iBotPeaches/Apktool) and place it in the same directory as the `apkrip.sh` script.
2. Install [APKLeaks](https://github.com/dwisiswant0/apkleaks) via Python.

## Usage

Run the following command:
`./apkrip.sh -f <package> -d <output_path> -t <target_name>`

| Argument | Description                                                   | Example                      |
| -------- | ------------------------------------------------------------- | ---------------------------- |
| -f       | The `.apk` file to analyse.                                   | `-f com.example.app.apk`     |
| -d       | The output directory for the reports.                         | `-d /home/shrike/my_target` |
| -t       | The name of the target. Used for filename/directory creation. | `-t google`                  |
