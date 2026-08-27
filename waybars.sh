#!/usr/bin/env bash
# The script is built to return a list of key-value pairs
# containing all possible Waybar configuration layouts.
#
# The script can be used by applications such as Rofi
# to make selecting an option more practical.

BASE_DIR="${1:-.}"

cd "$BASE_DIR" || exit 1

find . -type d -name .git -prune -o -type f -name "config" -print0 | while IFS= read -r -d '' config_file; do
    dir_path=$(dirname "$(realpath "$config_file")")
    dir_name=$(basename "$dir_path")
    
    echo "${dir_name}=\"${dir_path}\""
done
