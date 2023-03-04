# The Ars0n Framework

A Modern, Agile Framework for Bug Bounty Hunting on Kali Linux

### Install

`python3 install.py`

[Install Video](https://www.youtube.com/watch?v=cF4xtVS7Rnc)

### Run the Web Application (Client and Server)

`./run.sh`

### Basic Scan

`python3 wildfire.py --start --scan`

### Issues

If you run into any bugs or issues getting this framework to work, please include the output of `debug.sh` in any Issue raised.

### Troubleshooting

Most install/run issues are caused by the MongoDB service not running.  I'm working on building a fix for this but unvortunately the issues are out of my control.  In most cases, running `service mongodb start` will solve the problem.  If you are still unable to get MongoDB running, you can [download the MongoDB binary](https://www.mongodb.com/try/download/community) and run it manually as a work-around.

Under Construction...
