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

## About

Howdy!  My name is Harrison Richardson, or `rs0n` (arson) when I want to feel cooler than I really am.  The code in this repository started as a small collection of scripts to help automate many of the common Bug Bounty hunting processes I found myself repeating.  Over time, I built a simple web application with a MongoDB connection to manage my findings and identify valuable data points.  After 5 years of Bug Bounty hunting, both part-time and full-time, I'm finally ready to package this collection of tools into a proper framework.

**The Ars0n Framework** is designed to provide aspiring Application Security Engineers with all the tools they need to leverage Bug Bounty hunting as a means to learn valuable, real-world AppSec concepts and make 💰 doing it!  My goal is to lower the barrier of entry for Bug Bounty hunting by providing easy-to-use automation tools in combination with educational content and how-to guides for a wide range of Web-based and Cloud-based vulnerabilities.  In combination with my YouTube content, this framework will help aspiring Application Security Engineers to quickly and easily understand real-world security concepts that directly translate to a high paying career in Cyber Security.  

In addition to using this tool for Bug Bounty Hunting, aspiring engineers can also use this Github Repository as a canvas to practice collaborating with other developers!  This tool was inspired by Metasploit and designed to be modular in a similar way.  Each Script (Ex: `wildfire.py` or `slowburn.py`) is basically an algorithm that runs the Modules (Ex: `fire-starter.py` or `fire-scanner.py`) in a specific patter for a desired result.  Because of this design, the community is free to build new Scripts to solve a specific use-case or Modules to expand the results of these Scripts.  By learning the code in this framework and using Github to contribute your own code, aspiring engineers will continue to learn real-world skills that can be applied on the first day of a Security Engineer I position.

My hope is that this modular framework will act as a canvas to help share what I've learned over my career to the next generation of Security Engineers!  Trust me, we need all the help we can get!!

<h4 align="center">
🤠 Did you know that over 95% of scientists believe there is a direct correlation between the amount of coffee I drink and how quickly I can build a working Alpha version of this framework?  Crazy, right?!  Well, now you can test their hypothesis and Buy Me a Coffee through this fancy button!!  🤯
<br>
<br>
<a href="https://www.buymeacoffee.com/rs0n.evolv3" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
</h4>

## Install

`python3 install.py`

[Install Video](https://www.youtube.com/watch?v=cF4xtVS7Rnc)

#### Run the Web Application (Client and Server)

`./run.sh`

If you run into any bugs or issues getting this framework to work, please include the output of `debug.sh` in any Issue raised.

## Scripts

#### Wildfire Script

`python3 wildfire.py --start --scan`

#### Slowburn Script

`python3 slowburn.py`

#### Troubleshooting

## Modules

#### Fire-Starter

#### Fire-Scanner

#### Fire-Spreader

#### Fire-Enumerator (Gotta think of a better name...)

## For Developers

## FAQ

Most install/run issues are caused by the MongoDB service not running.  I'm working on building a fix for this but unvortunately the issues are out of my control.  In most cases, running `service mongodb start` will solve the problem.  If you are still unable to get MongoDB running, you can [download the MongoDB binary](https://www.mongodb.com/try/download/community) and run it manually as a work-around.
