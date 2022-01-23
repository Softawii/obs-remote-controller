import asyncio
import simpleobsws
import json


_config = json.load(open('config.json'))
_parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)
_ws = simpleobsws.WebSocketClient(url = _config['obs_url'], 
                                 password = _config['obs_password'], 
                                 identification_parameters = _parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

my_var = 0

async def setup():
    try:
        await _ws.connect()
        await _ws.wait_until_identified() # Wait for the identification handshake to complete
        print("Setup!")
    except:
        print("Error!")
        return False
    
    return True
            
            
async def scene_list():
    
    request = simpleobsws.Request('GetSceneList')

    try:
        ret = await call(request) # Perform the request    
        
        scenes = ret.responseData['scenes']
        scenes = list(map(lambda scene: scene['sceneName'], scenes))
        return (ret.ok(), scenes)
    except:
        return (False, [])

async def set_scene(scene_name):
    request = simpleobsws.Request('SetCurrentProgramScene', { 'sceneName': scene_name })

    try:
        ret = await call(request) # Perform the request    

        return ret.ok()
    except:
        return False


async def get_current_scene():
    request = simpleobsws.Request('GetCurrentProgramScene')

    try:
        ret = await call(request) # Perform the request    

        if ret:
            print (ret.responseData)
            
            return (ret.ok(), ret.responseData['currentProgramSceneName'])
        else:
            return (False, "")
    except:
        return (False, "")

async def call(request):
    try:
        ret = await _ws.call(request)
        return ret
    except simpleobsws.NotIdentifiedError as e:
        await setup()
        await asyncio.sleep(_config['update_time'])
        await call(request)