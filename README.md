<h1 align="center">
  <a href="https://www.linkedin.com/in/%E2%84%8C%F0%9D%94%9E%F0%9D%94%AF%F0%9D%94%AF%F0%9D%94%A6%F0%9D%94%B0%F0%9D%94%AC%F0%9D%94%AB-%E2%84%9C%F0%9D%94%A6%F0%9D%94%A0%F0%9D%94%A5%F0%9D%94%9E%F0%9D%94%AF%F0%9D%94%A1%F0%9D%94%B0%F0%9D%94%AC%F0%9D%94%AB-%F0%9D%96%A2%F0%9D%96%A8%F0%9D%96%B2%F0%9D%96%B2%F0%9D%96%AF-%F0%9D%96%AE%F0%9D%96%B2%F0%9D%96%B6%F0%9D%96%A4-%F0%9D%96%AC%F0%9D%96%B2%F0%9D%96%BC-7a55bb158/"><img src="static/rs0n-logo.png" width="200px" alt="Arson Logo"></a>
  <br>
  The Ars0n Framework
  <br>
</h1>

<h4 align="center">A Modern, Agile Framework for Bug Bounty Hunting on Kali Linux</h4>
      
<p align="center">
  <a href="#hows">About</a> •
  <a href="#install">Install</a> •
  <a href="#scripts">Scripts</a> •
  <a href="#modules">Modules</a> •
  <a href="#for-developers">For Developers</a> •
  <a href="#faq">FAQs</a> •
  <a href="https://www.youtube.com/@rs0n_live">YouTube</a> •
  <a href="https://www.twitch.tv/rs0n_live">Twitch</a> •
  <a href="#coming-soon">Discord</a>
</p>

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
