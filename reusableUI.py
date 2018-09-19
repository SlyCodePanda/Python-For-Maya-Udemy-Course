from maya import cmds
# Import the tween and gear functions
from tweenerUI import tween
from gearClassCreator import Gear

class BaseWindow( object ) :

    windowName = "BaseWindow"

    def show(self) :

        # If a window with the window name "Tweener Window" already exists, delete UI. This stops you from being able
        # to open multiple tweener windows at once.
        if cmds.window(self.windowName, query=True, exists=True) :
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow()

    def buildUI(self) :
        pass

    # the *args parameter means that any extra arguments given to this function will be stored inside 'args'.
    def reset(self, *args) :
        pass

    def close(self, *args) :
        cmds.deleteUI(self.windowName)


class TweenerUI(BaseWindow) :

    windowName = "TweenerWindow"

    def buildUI(self) :
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    # the *args parameter means that any extra arguments given to this function will be stored inside 'args'.
    def reset(self, *args) :
        cmds.floatSlider(self.slider, edit=True, value=50)


class GearUI(BaseWindow) :
    windowName = "GearWindow"

    def __init__(self) :
        self.gear = None

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the gear")

        cmds.rowLayout(numberOfColumns=4)

        self.label = cmds.text(label="10")
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)

        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
        # Gives and integer value to use for the teeth.
        teeth = cmds.intSlider(self.slider, query=True, value=True)

        self.gear = Gear()
        self.gear.createGear(teeth=teeth)

    def modifyGear(self, teeth):
        # If gear exists, modify teeth of existing gear.
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)

        cmds.text(self.label, edit=True, label=teeth)

    def reset(self, *args):
        # Un-hook the slider from any current gear
        self.gear = None
        # Change the value of the slider back to 10.
        cmds.intSlider(self.slider, edit=True, value=10)
        # Change the text back to 10 also.
        cmds.text(self.label, edit=True, label=10)