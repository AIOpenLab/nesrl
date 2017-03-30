import sys

import gym
from gym.envs.registration import register
import numpy as np

for bout in ('GlassJoe', 'VonKaiser', 'PistonHondaI', 'DonFlamencoI',
             'KingHippo', 'GreatTiger', 'BaldBullI'):
    register(
        id='MTPO-{}-v0'.format(bout),
        entry_point='envs:NESEnv',
        kwargs={'bout': bout}
    )

"""
Memory Map
0x0600-0x06FF -> fighter state, 81 tracks consecutive hits to a point?, special move started, little mac knock downs
0x0600-0x06FF -> BO,B1 related to loss of bout, appear at results screen
0x0700-0x07FF -> appears to be sound related
"""


env = gym.make("MTPO-{}-v0".format(sys.argv[1]))
for ep in range(10):
    observation = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            break
