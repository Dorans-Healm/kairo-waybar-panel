#!/bin/bash

FILE="$HOME/.config/waybar/config"

TOP_FILE="$HOME/.config/waybar/base_config/config_left"
BOT_FILE="$HOME/.config/waybar/base_config/config_right"

TOP='left'
BOT='right'

value=$(grep '"position"' "$FILE" | sed -E 's/.*"position": *"([^"]*)".*/\1/')
config=""

case "$value" in
    "$TOP")
        config="$BOT_FILE"
        ;;
    "$BOT")
        config="$TOP_FILE"
        ;;
    *)
        echo "Unknown position: $value"
        exit 1
        ;;
esac

cp -f "$config" "$FILE"

killall -9 waybar
bash "$HOME/.config/waybar/scripts/generate_colors.sh"
waybar
