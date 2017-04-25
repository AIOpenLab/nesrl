<!-- toc -->

- [Requirements](#requirements)
- [Setup](#setup)
  * [OSX](#OSX)
  * [Ubuntu](#ubuntu)
- [Running The Code](#running-the-code)
- [Further Reading](#further-reading)

<!-- tocstop -->

## Requirements

* Python 3
  * OpenAI Gym
* Lua 5.1
* FCEUX

## Setup

### OSX:

    brew install fceux
    brew install lua@5.1
    luarocks-5.1 install luasocket

### Ubuntu:

    sudo apt-get install fceux
    sudo apt-get install lua5.1
    sudo luarocks install luasocket

## Running the code:

Grab a ROM for Mike Tyson's Punch Out, save it as `mtpo.nes`, then execute the two commands:

```bash
$ fceux --loadlua gym.lua mtpo.nes
$ python mtpo_agent.py GlassJoe 
```
GlassJoe is one of a several possible entry points, see the [states](states) directory for other options.

## Further Reading:

Memory locations for Mike Tyson's Punch Out:
 * https://raw.githubusercontent.com/esc0rtd3w/nes-rom-tools/master/0_multi/fceux-2.2.2-win32/luaScripts/PunchOutChallenge.lua
