#!/bin/bash

python_script="install.py"
log_file="logs/install.log"

python3 "$python_script" | sudo tee "$log_file"

echo "Installation complete. Check '$log_file' for details."