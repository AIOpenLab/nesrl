-- AI OpenLab
-- Hooks to support synchronous RL experiments using OpenAI's Gym
-- author: bgalbraith

-- let FCEUX know where the luasocket package exists
-- no local in path for Docker version
package.path = package.path .. ";/usr/local/share/lua/5.1/?.lua"

-- reference to the savestate for reloading
-- resets will always be from savestate 0, the control server will copy the
-- apropriate save state into that position based on the requested environment
local state

-- environment reset
local function reset()
  savestate.load(state)
end

-- setup control server and wait for client to connect before starting game loop
local socket = require("socket")
local tcp = socket.tcp()
tcp:bind("localhost", 6502)
tcp:listen(1)
local conn
conn, err = tcp:accept()
print("connected")

state = savestate.object(10)
-- game loop
while true do
  msg, err = conn:receive()
  -- sets cmd and, optionally, action from received command string
  loadstring(msg)()

  if cmd == "reset" then
    reset()
  elseif cmd == "step" then
    joypad.set(1, action)
    emu.frameadvance()
  elseif cmd == "quit" then
    break
  end
  conn:send(memory.readbyterange(0, 2048) .. gui.gdscreenshot())
end

tcp:close()
emu.pause()
