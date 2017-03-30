import array
import os
import shutil
import socket

import gym
from gym import spaces
import numpy as np


class NESEnv(gym.Env):
    # RAM + 32bit GD format screen grab
    FCEUX_DATA_LENGTH = 2048 + 11 + 256*240*4

    def __init__(self, bout='GlassJoe', ntsc=True):
        super(NESEnv, self).__init__()
        self.bout = bout
        self.ntsc = ntsc

        shutil.copyfile('states/MTPO-{}.fc'.format(bout),
                        os.path.expanduser('~/.fceux/fcs/mtpo.fc0'))

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(('localhost', 6502))
        print("connected to FCEUX")

        width = 256
        height = 224 if ntsc else 240

        self.action_space = spaces.MultiDiscrete([
            [0, 8],  # d-pad: noop, u, ur, r, dr, d, dl, l, ul
            [0, 1],  # a button: noop, pressed
            [0, 1],  # b button: noop, pressed
            [0, 1],  # select button: noop, pressed
            [0, 1]   # start button: noop, pressed
        ])
        # video frame
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(height, width, 3))

    def __del__(self):
        try:
            self._socket.sendall(b"cmd='quit'\n")
            self._socket.close()
        except Exception:
            pass

    def _step(self, action):
        action_string = NESEnv._convert_action(action)
        msg = "cmd='step';action={"+action_string+"}\n"
        self._socket.sendall(msg.encode())
        memory, frame = self._receive_gamestate()
        stop = memory[0x0302] == 3  # we've hit the 3 min mark / end of round
        return frame, 0.0, stop, {}

    def _reset(self):
        self._socket.sendall(b"cmd='reset'\n")
        memory, frame = self._receive_gamestate()
        return memory

    def _render(self, mode='human', close=False):
        pass

    def _receive_gamestate(self):
        chunks = []
        bytes_remain = NESEnv.FCEUX_DATA_LENGTH
        while bytes_remain > 0:
            chunk = self._socket.recv(max(bytes_remain, 2048))
            if chunk == b'':
                raise ConnectionResetError("connection broken")
            chunks.append(chunk)
            bytes_remain -= len(chunk)
        data = b''.join(chunks)
        memory = array.array('B')
        memory.fromstring(data[0:2048])
        memory = np.array(memory, dtype=np.uint8)
        frame = self._gd2frame(data[2059:])
        return memory, frame

    def _gd2frame(self, raw):
        frame = array.array('B')
        frame.fromstring(raw)
        frame = np.array(frame).reshape((240, 256, 4))
        if self.ntsc:
            frame = frame[8:232]
        return frame[:, :, 1:4]

    @staticmethod
    def _convert_action(action):
        d_pad = {
            0: [('up', 0), ('right', 0), ('down', 0), ('left', 0)],
            1: [('up', 1), ('right', 0), ('down', 0), ('left', 0)],
            2: [('up', 1), ('right', 1), ('down', 0), ('left', 0)],
            3: [('up', 0), ('right', 1), ('down', 0), ('left', 0)],
            4: [('up', 0), ('right', 1), ('down', 1), ('left', 0)],
            5: [('up', 0), ('right', 0), ('down', 1), ('left', 0)],
            6: [('up', 0), ('right', 0), ('down', 1), ('left', 1)],
            7: [('up', 0), ('right', 0), ('down', 0), ('left', 1)],
            8: [('up', 1), ('right', 0), ('down', 0), ('left', 1)]
        }.get(action[0])
        buttons = [
            ('A', action[1]),
            ('B', action[2]),
            ('select', action[3]),
            ('start', action[4])
        ] + d_pad
        _action = ', '.join(["{}={}".format(b[0], 'true' if b[1] else 'false')
                            for b in buttons])
        return _action
