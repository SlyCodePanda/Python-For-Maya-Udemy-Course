from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')


def createDirectory(directory=DIRECTORY) :

    """
    Creates the given directory if it does not already exist.
    Args:
        directory (str): The directory to create.
    """

    if not os.path.exists(directory) :
        os.mkdir(directory)


class ControllerLibrary(dict) :

    # Store any extra variables in the 'info' variable using double stars (**).
    def save(self, name, directory=DIRECTORY, screenshot=True, **info) :

        createDirectory(directory)

        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        # If there is an object selected, save out a file with just that selected object.
        # else, just do a regular save.
        if cmds.ls(selection=True) :
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        else :
            # force=True means if the file already exists, we save over it.
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot :
            info['screenshot'] = self.saveScreenshot(name, directory=directory)

        # Open a file in write mode and store this open file in a temp variable f.
        # Then with this variable f, use json to dump the info dictionary (**info) into f, and indent everything by
        # 4 spaces.
        with open(infoFile, 'w') as f :
            json.dump(info, f, indent=4)

        # Update ourselves every time we save.
        self[name] = info


    def find(self, directory=DIRECTORY) :

        """
        Finds controllers on disk.
        Args:
            directory: The directory to search in.

        Returns:

        """

        # clear our dictionary.
        self.clear()

        if not os.path.exists(directory) :
            return

        files = os.listdir(directory)

        # Filter out anything that isn't a maya file.
        mayaFiles = [f for f in files if f.endswith('.ma')]

        # Loop through all the maya files in the directory and add them to our dictionary.
        for ma in mayaFiles :
            # This will split the name from the extension and give us back the name and extension in separate variables.
            name, extension = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            # Look for the info JSON file, and if we don't find it, set info to be an empty dictionary.
            infoFile = '%s.json' % name
            if infoFile in files :
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)
            else :
                info = {}

            # Check to see if the screenshot also exists
            screenshot = '%s.jpg' % name
            if screenshot in files :
                info['screenshot'] = os.path.join(directory, name)

            # Make sure the info dictionary is populated.
            info['name'] = name
            info['path'] = path

            # Remember that the class ControllerLibrary is actually a dictionary.
            # This means we can access ourselves as if we are a dictionary.
            self[name] = info


    def load(self, name) :

        # Look up name in our dictionary.
        path = self[name]['path']
        # 'i' flag means 'import'
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenshot(self, name, directory=DIRECTORY) :
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path