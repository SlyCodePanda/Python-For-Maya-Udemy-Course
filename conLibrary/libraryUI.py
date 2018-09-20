import pprint

import controllerLibrary
from maya import cmds

reload(controllerLibrary)
from PySide2 import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog) :
    """
    The controller library UI is a dialog that lets us save and import controllers.
    """

    def __init__(self) :
        # Find the super class of this class (in this case, QtWidgets.QDialog).
        # Then once we have found the thing our ControllerLibrary inherits from, we need to tell it how to refer to this
        # specific instance. Not necessary in Python 3 and above.
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')

        # The library variable points to an instance of our controller library.
        self.library = controllerLibrary.ControllerLibrary()

        # Every time we create a new instance we will automatically build our UI and populate it.
        self.buildUI()
        self.populate()


    def buildUI(self) :
        """
        This method builds out the UI.
        """

        # This is the master layout.
        layout = QtWidgets.QVBoxLayout(self)

        # This is a child horizontal widget.
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        # Adding the 'self.' at the front means that this variable will be available to the whole class.
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        # Create a new save button and add it to the saveLayout.
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # These are the parameters for our thumbnail size.
        size = 64
        buffer = 12

        # This will create a grid list widget to display our controller thumbnails.
        self.listWidget = QtWidgets.QListWidget()
        # Tells the listWidget to display in icon mode.
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        # Set the icon size to be 64 x 64 pixels
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        # Set it so the widget moves and resizes when the window is resized.
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        # Gives a buffer between list objects.
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)

        # This is our child widget that holds all the buttons.
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        # Create and add buttons to the btnWidget.
        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)


    def populate(self) :
        """
        This clears the listWidget and then re-populates it with the contents of our library.
        """

        # Clear the list widget's contents before populating.
        self.listWidget.clear()
        self.library.find()

        for name, info in self.library.items() :
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot :
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))


    def load(self) :
        """
        This loads the currently selected controller.
        """

        currentItem = self.listWidget.currentItem()
        if not currentItem :
            return

        name = currentItem.text()
        self.library.load(name)

        #self.saveNameField.setText(name)


    def overwriteDialog(self, name) :
        """
        Warning message box that appears when you try to save over an existing object in library.
        """

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("This object already exists")
        msg.setInformativeText("Do you want to overwrite it?:")
        msg.setWindowTitle("Item Already Exists")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        retval = msg.exec_()

        # Depending on whether 'Yes' or 'No' was pressed, do the following:
        if retval == 16384 :
            print "YES was pressed"
            self.library.save(name)
            self.populate()
            self.saveNameField.setText('')
        elif retval == 65536 :
            print "NO was pressed"
            return


    def save(self) :
        """
        This saves the controller with the given file name.
        """

        name = self.saveNameField.text()
        # Strip name of any white spaces.
        # If after striping the name the name no longer exists.
        if not name.strip() :
            cmds.warning("You must give a name.")
            return

        # Check if object is already in library, if so warn the user that proceeding will result in saving over the
        # top of existing object in library.
        if name in self.library :
            #print "This item already exists!"
            cmds.warning("This item already exists!")
            self.overwriteDialog(name)



def showUI() :
    """
    This shows and returns a handle to the UI.
    Returns:
        QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui