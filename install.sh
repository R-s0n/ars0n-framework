#!/bin/bash

python_script="install.py"
log_file="logs/install.log"

if [[ "$1" == "--arm" ]]; then
    python3 "$python_script" --arm 2>&1 | tee "$log_file"
else
    python3 "$python_script" 2>&1 | tee "$log_file"
fi

echo "Installation complete. Check '$log_file' for details."