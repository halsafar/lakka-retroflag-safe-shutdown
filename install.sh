#!/bin/bash

# Script Config
TIMEZONE_FILE="/storage/.cache/timezone"
DEFAULT_TIMEZONE="America/Regina"
MASTER_ARCHIVE_URL="https://github.com/halsafar/lakka-retroflag-safe-shutdown/archive/master.zip"
MASTER_ARCHIVE_FILE="lakka-retroflag-safe-shutdown-master.zip"
AUTOSTART_SCRIPT="/storage/.config/autostart.sh"
TMP_DIR="/storage/.tmp"

# On Lakka the default user id is 0
if ! [ $(id -u) = 0 ]; then
   echo "Please execute script as root (on Lakka this should be the default user)." 
   exit 1
fi

# Set timezone
read -p "Enter your timezone [${DEFAULT_TIMEZONE}]:" USER_TIMEZONE
USER_TIMEZONE=${USER_TIMEZONE:-${DEFAULT_TIMEZONE}}
echo "TIMEZONE=${USER_TIMEZONE}" > "${TIMEZONE_FILE}"

# Download scripts
cd "${TMP_DIR}"
wget -O "${MASTER_ARCHIVE_FILE}" "${MASTER_ARCHIVE_URL}"

# Install scripts
unzip -o "${MASTER_ARCHIVE_FILE}"
cd lakka-retroflag-safe-shutdown/
mkdir -p /storage/scripts
cp -R lib/ /storage/scripts/
cp -R scripts/* /storage/scripts/

# Set autostart
if [ ! -f /storage/.config/autostart.sh ]; then
    echo "python /storage/scripts/safe_shutdown.py &" >> "${AUTOSTART_SCRIPT}"
fi

# Check success
if grep -Fxq "safe_shutdown.py"  "${AUTOSTART_SCRIPT}"
then
	echo "Error installing scripts, autostart configuration failed..."
	echo "Manually place 'python /storage/scripts/safe_shutdown.py &' in ${AUTOSTART_SCRIPT}"
else
    echo "Success installing scripts."
	echo "Will now reboot after 3 seconds."
	sleep 3
	reboot
fi
