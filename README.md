# lakka-retroflag-safe-shutdown
Simple script to setup a safe shutdown on Lakka+RetroFlag

Works on NESPi and SNESPi cases.

# How to install

## Enable SSH In Lakka
1. Connect rPi to internet
1. Boot up Lakka
1. Config -> Services -> SSH Enable -> On

## Install scripts

1. ssh to your Lakka instance
   ```text
   ssh root@YOUR_LAKKA_IP_ADDRESS
   password: root (if unchanged)
   ```
1. `wget -O - "https://github.com/halsafar/lakka-retroflag-safe-shutdown/raw/master/install.sh" | bash`

# Credits
This is pretty much a cleaned up version of:
- https://github.com/thiagoauler/lakka_nespi_power
- https://github.com/marcelonovaes/lakka_nespi_power