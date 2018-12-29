def getRGBData(rgbStrip,led = 0):
    result = {}
    data = rgbStrip.getData()
    red = data[0]
    green = data[1]
    blue = data[2]
    result[led] = {'led': led, 'red': red[led], 'green': green[led], 'blue': blue[led]}
    return result

# return json of all configured rgbStrips
def getRGBStrips(rgbStripController):
    result = {}
    for rgbStrip in rgbStripController.getRGBStrips():
        result[rgbStrip.STRIP_UID] = {'index': rgbStrip.STRIP_UID, 'name': rgbStrip.STRIP_NAME}
    return result