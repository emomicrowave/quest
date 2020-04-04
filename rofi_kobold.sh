#!/bin/bash
task=$(kobold ls | rofi -dmenu -p "kobold")
pom "$task" &
