import asyncio
import simpleobsws
import json


_config = json.load(open('config.json'))
_parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)
_ws = simpleobsws.WebSocketClient(url = _config['obs_url'], 
                                 password = _config['obs_password'], 
                                 identification_parameters = _parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.
disconnect = True
my_var = 0

async def setup(run_reconnect = True, log = True):
    
    global disconnect
    
    try:
        await _ws.connect()
        await _ws.wait_until_identified() # Wait for the identification handshake to complete
        disconnect = False
        print("Setup!")
    except:
        if log:
            print("core.setup: OBS is not connected to the websocket or is closed")
        disconnect = True 
        if run_reconnect:
            asyncio.ensure_future(reconnect())
        return False
    
    return True
            
            
async def scene_list(): 
    print("core.scene_list: trying to get scene list") 
    print("core.scene_list: connection status = " + str(disconnect)) 
    if disconnect:
        return (False, [])
      
    request = simpleobsws.Request('GetSceneList')

    try:
        ret = await call(request) # Perform the request    
        
        scenes = ret.responseData['scenes']
        scenes = list(map(lambda scene: scene['sceneName'], scenes))
        return (ret.ok(), scenes)
    except:
        return (False, [])

async def set_scene(scene_name):
    if disconnect:
        return False
    
    request = simpleobsws.Request('SetCurrentProgramScene', { 'sceneName': scene_name })

    try:
        ret = await call(request) # Perform the request    

        return ret.ok()
    except:
        return False


async def get_current_scene():
    
    if disconnect:
        return (False, "")
    
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
    global disconnect
    
    try:
        ret = await _ws.call(request)
        return ret
    except simpleobsws.NotIdentifiedError as e:
        print("core.call: OBS is not connected to the websocket or is closed")
        disconnect = True 
        asyncio.ensure_future(reconnect())
        
async def reconnect():
    global disconnect
    
    print("core.reconnect: trying to Reconnect")
    reconnected = False 
    
    while not reconnected:
        reconnected = await setup(False, False)
        await asyncio.sleep(_config['update_time'])
    disconnect = False
    print("Reconnected")
    