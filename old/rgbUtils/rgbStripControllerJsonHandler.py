def getRGBData(rgbStrip):
    result = {}
    data = rgbStrip.getData()
    red = data[0]
    green = data[1]
    blue = data[2]
    for x in range(len(red)):
        result[x] = {'red': red[x], 'green': green[x], 'blue': blue[x]}
    return result

# return json of all configured rgbStrips
def getRGBStrips(rgbStripController):
    result = {}
    for rgbStrip in rgbStripController.getRGBStrips():
        result[rgbStrip.STRIP_UID] = {'index': rgbStrip.STRIP_UID, 'name': rgbStrip.STRIP_NAME}
    return result