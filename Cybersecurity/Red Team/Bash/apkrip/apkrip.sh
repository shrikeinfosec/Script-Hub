#!/bin/bash

## --- FUNCTIONS --- ##

function runAPKTool() {
    echo "Running APKTool extraction..."
    echo
    $(java -jar $apktool_loc decode -q -o $target/apktool/$target $file)
}

function runAPKLeaks() {
    echo "Running APKLeaks extraction..."
    echo
    $(apkleaks -f "$file" -o "$target/apkleaks_$target.json" --json -a "--log-level QUIET") # we don't want extra logging, so we use quiet.
}

print_usage() {
  printf "Usage: ./apkrip.sh -f <file> -d <output_path> -t <target>"
  printf "Eg.  : ./apkrip.sh -f com.example.app.apk -d /path/to/output -t google"
}
## SET UP VARIABLES
apktool_loc="apktool.jar"

# ---- #
echo "APK RIP Script v1.0.0"

while getopts 'f:t:' flag; do
  case "${flag}" in
    f) file="${OPTARG}" ;;
    t) target="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

echo
echo "Evaluating APK file..."
echo
echo "$file was selected for analysis"
echo
runAPKLeaks
echo "Initial analysis complete"
echo
runAPKTool
echo "APK decompiled and available in apktool"
echo
echo "Process complete! Press enter to exit..."
read junk