How to run:

### Requirements

* Python 3
  * OpenAI Gym
* Lua 5.1
* FCEUX

### Setup

**OSX:**

    brew install fceux
    brew install lua@5.1
    luarocks-5.1 install luasocket

**Ubuntu:**

    sudo apt-get install fceux
    sudo apt-get install lua5.1
    sudo luarocks install luasocket

### Running the code:

**Run FCEUX**

`fceux --loadlua gym.lua [game.nes]`

**Run MTPO Agent**

`python mtpo_agent.py [BoutName]`

e.g. `python mtpo_agent.py GlassJoe`

