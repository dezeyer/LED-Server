"""
Convert the effectController function outputs to json format
"""

def responseHandler(effectController,rgbStripController,data):
    if "startEffect" in data:
        enabledRGBStrips = []
        for rgbStrip in rgbStripController.getRGBStrips():
            for rgbStripJsonArray in data['startEffect']['rgbStrips']:
                if rgbStrip.STRIP_UID in rgbStripJsonArray[0] and rgbStripJsonArray[1]:
                    enabledRGBStrips.append(rgbStrip)
        
        effectController.startEffect(effectController.getEffects()[data['startEffect']['effect']],enabledRGBStrips,data['startEffect']['params'])
    if "moveRGBStripToEffectThread" in data:
        for rgbStrip in rgbStripController.getRGBStrips():
            if rgbStrip.STRIP_UID in data['moveRGBStripToEffectThread']['rgbStrip']:
                effectController.moveRGBStripToEffectThread( \
                    rgbStrip, \
                    effectController.getEffectThreads()[data['moveRGBStripToEffectThread']['effectThread']] \
                )
    if "effectThreadChangeEffectParam" in data:
        effectController.updateEffectParameters(\
            effectController.getEffectThreads()[data['effectThreadChangeEffectParam']['effectThread']], \
            data['effectThreadChangeEffectParam']['params']
        )
    return 'ok'

# return json of all configured effects (except offEffect) with their paramDescriptions
def getEffects(effectController):
    result = {}
    for x, effect in enumerate(effectController.getEffects()):
        effectParams = {}
        for y, effectParam in enumerate(effect.effectParameters):
            effectParams[y] = {'index': y,'type': effectParam.type, 'name': effectParam.name, 'desc': effectParam.desc, 'options': effectParam.options}
        result[x] = {'index': x, 'name': effect.name, 'desc': effect.desc, 'effectParams': effectParams}
    return result

# return json of all running effectThreads with their active rgbStrips and params
def getEffectThreads(effectController):
    result = {}
    for x, effectThread in enumerate(effectController.getEffectThreads()):
        effectRGBStrips = {}
        for effectRGBStrip in effectController.getEffectRGBStrips(effectThread):
            effectRGBStrips[effectRGBStrip.STRIP_UID] = {'index': effectRGBStrip.STRIP_UID, 'name': effectRGBStrip.STRIP_NAME}
        effectParams = {}
        for z, effectParam in enumerate(effectThread.effectParameters):
            effectParams[z] = {'index': z,'type': effectParam.type, 'name': effectParam.name, 'desc': effectParam.desc, 'options': effectParam.options, 'values': effectThread.effectParameterValues[z]}
        result[x] = {'index': x, 'name': effectThread.name, 'desc': effectThread.desc,'activeRGBStips': effectRGBStrips, 'dump': str(effectThread), 'effectParams': effectParams}
    return result