"""
Convert the rgbStripController function outputs to json format
"""

# get the color values of a single led in json format
def getRGBData(rgbStrip,led = 0):
    return {'led': led, 'red': rgbStrip.getData()[0][led], 'green': rgbStrip.getData()[1][led], 'blue': rgbStrip.getData()[2][led]}

# return json of all configured rgbStrips
def getRGBStrips(rgbStripController):
    result = {}
    for rgbStrip in rgbStripController.getRGBStrips():
        result[rgbStrip.STRIP_UID] = {'index': rgbStrip.STRIP_UID, 'name': rgbStrip.STRIP_NAME}
    return result