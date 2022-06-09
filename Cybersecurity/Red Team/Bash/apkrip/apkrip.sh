#!/bin/bash

runAPKTool() {
    printf "Running APKTool extraction...\n"
    apktool_cmd=$(java -jar "$apktool_loc" decode -q -o "$target/apktool/$target" "$file")
    eval "$apktool_cmd"
}

runAPKLeaks() {
    printf "Running APKLeaks extraction...\n"
    apkleaks_cmd=$(apkleaks -f "$file" -o "$target/apkleaks_$target.json" --json -a "--log-level QUIET") # we want to remove extra logging, so we use quiet.
    eval "$apkleaks_cmd"
}

print_usage() {
  printf "Usage: ./apkrip.sh -f <file> -d <output_path> -t <target>"
  printf "Eg.  : ./apkrip.sh -f com.example.app.apk -d /path/to/output -t google"
}

apktool_loc="apktool.jar"

printf "APK RIP Script v1.0.0"

while getopts "f:t:" flag; do
  case "${flag}" in
    f) file="${OPTARG}" ;;
    t) target="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

printf "\nEvaluating APK file...\n"
printf "%s was selected for analysis\n" "$file"

runAPKLeaks

printf "Initial analysis complete\n"

runAPKTool

printf "APK decompiled and available in apktool\n"
printf "Process complete! Press enter to exit...\n"