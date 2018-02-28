#!/bin/bash

if [ $UID -ne 0 ]; then
  echo -e "\033[41;37mRoot permission required.\033[0m"
  echo -e "\033[41;37mUse \"sudo bash $0\" instead.\033[0m"
  exit 3
fi

echo "Downloading required files..."
mkdir /etc/gekko >/dev/null 2>&1
mkdir /etc/bash_completion.d >/dev/null 2>&1
wget --no-check-certificate https://raw.githubusercontent.com/CYRO4S/Gekko/master/tab-complete/gekko_tc -O /etc/bash_completion.d/gekko_tc >/dev/null 2>&1
wget --no-check-certificate https://raw.githubusercontent.com/CYRO4S/Gekko/master/tab-complete/gekko_tc.py -O /etc/gekko/gekko_tc.py >/dev/null 2>&1

echo "Configurating tab-complete..."
echo "source /etc/bash_completion.d/gekko_tc" >> ~/.bashrc
echo ""
echo "Now, execute 'source ~/.bashrc'"
