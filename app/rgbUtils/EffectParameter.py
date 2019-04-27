import threading

class effectParameter(object):
    # The Name and the Description of the EffectParameter, 
    # should be overwritten by the inheritancing EffectParameter
    name="Undefined"
    desc = "No Description"

    # In the order you expect the options to be set
    # [
    #   [min/off,max/on,current,"description"],
    #   [min/off,max/on,current,"description"],
    #   [min/off,max/on,current,"description"],
    # ]
    options = []

    def __init__(self,name,desc,initOptions = []):
        self.name = name
        self.desc = desc
        self.options = initOptions

    # check if the given values are plausible
    def testValue(self,index,value):
        if value >= self.options[index][0] \
            and value <= self.options[index][1]:
            return True
        else:
            return False

class colorpicker(effectParameter):
    name="UndefinedColorpicker"
    desc="No Description"
    type="colorpicker"

    # check if the given values are plausible
    def testValue(self,index,value):
        return True

class slider(effectParameter):
    name="UndefinedSlider"
    desc="No Description"
    type="slider"