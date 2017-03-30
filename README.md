How to run:

###Requirements

* Python 3
  * OpenAI Gym
* Lua 5.1
* FCEUX

###Setup

**Install FCEUX**

`brew install fceux`

**Install Lua 5.1**

`brew install lua@5.1`

**Install LuaSocket**

`luarocks install luasocket`

**Run FCEUX**

`fceux --loadlua gym.lua [game.nes]`

**Run MTPO Agent**

`python mtpo_agent.py [BoutName]`

e.g. `python mtpo_agent.py GlassJoe`
