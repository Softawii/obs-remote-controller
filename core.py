import asyncio
import simpleobsws
import json


config = json.load(open('credentials.json'))
parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)
ws = simpleobsws.WebSocketClient(url = config['obs_url'], 
                                 password = config['obs_password'], 
                                 identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.


async def setup():
    await ws.connect()
    await ws.wait_until_identified() # Wait for the identification handshake to complete
    print("Setup!")


async def scene_list():
    
    request = simpleobsws.Request('GetSceneList')

    ret = await ws.call(request) # Perform the request    
    
    scenes = ret.responseData['scenes']
    scenes = list(map(lambda scene: scene['sceneName'], scenes))
    
    return (ret.ok(), scenes)


async def set_scene(scene_name):
    request = simpleobsws.Request('SetCurrentProgramScene', { 'sceneName': scene_name })

    ret = await ws.call(request) # Perform the request    

    return ret.ok()
