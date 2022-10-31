import names
import squish
from helpers.SetupClientHelper import getClientDetails, createUserSyncPath
import test


class AccountConnectionWizard:
    SERVER_ADDRESS_BOX = names.contentWidget_urlLineEdit_QLineEdit
    NEXT_BUTTON = names.setupWizardWindow_nextButton_QPushButton
    CONFIRM_INSECURE_CONNECTION_BUTTON = names.insecure_connection_Confirm_QPushButton
    USERNAME_BOX = names.contentWidget_usernameLineEdit_QLineEdit
    PASSWORD_BOX = names.contentWidget_passwordLineEdit_QLineEdit
    SELECT_LOCAL_FOLDER = names.localDirectoryGroupBox_localDirectoryLineEdit_QLineEdit
    DIRECTORY_NAME_BOX = (
        names.localDirectoryGroupBox_chooseLocalDirectoryButton_QToolButton
    )
    CHOOSE_BUTTON = names.qFileDialog_Choose_QPushButton
    ERROR_LABEL = {
        "name": "errorMessageLabel",
        "type": "QLabel",
        "visible": 1,
        "window": names.setupWizardWindow_OCC_Wizard_SetupWizardWindow,
    }
    CREDENTIAL_PAGE = {
        "container": names.setupWizardWindow_contentWidget_QStackedWidget,
        "name": "CredentialsSetupWizardPage",
        "type": "OCC::Wizard::BasicCredentialsSetupWizardPage",
        "visible": 1,
    }

    ADVANCE_SETUP_PAGE = {
        "name": "OwncloudAdvancedSetupPage",
        "type": "OCC::OwncloudAdvancedSetupPage",
        "visible": 1,
        "container": names.setupWizardWindow_contentWidget_QStackedWidget,
    }
    CONF_SYNC_MANUALLY_RADIO_BUTTON = (
        names.syncModeGroupBox_configureSyncManuallyRadioButton_QRadioButton
    )
    ADVANCED_CONFIGURATION_CHECKBOX = {
        "container": names.setupWizardWindow_contentWidget_QStackedWidget,
        "name": "advancedConfigGroupBox",
        "type": "QGroupBox",
        "visible": 1,
    }
    DIRECTORY_NAME_EDIT_BOX = {
        "buddy": names.qFileDialog_fileNameLabel_QLabel,
        "name": "fileNameEdit",
        "type": "QLineEdit",
        "visible": 1,
    }
    VIRTUAL_FILE_RADIO_BUTTON = names.syncModeGroupBox_useVfsRadioButton_QRadioButton
    ENABLE_EXPERIMENTAL_FEATURE_BUTTON = (
        names.contentWidget_Enable_experimental_placeholder_mode_QPushButton
    )
    STAY_SAFE_BUTTON = names.contentWidget_Stay_safe_QPushButton

    def __init__(self):
        pass

    def sanitizeFolderPath(self, folderPath):
        return folderPath.rstrip("/")

    def addServer(self, context):
        clientDetails = getClientDetails(context)
        squish.mouseClick(squish.waitForObject(self.SERVER_ADDRESS_BOX))
        squish.type(
            squish.waitForObject(self.SERVER_ADDRESS_BOX),
            clientDetails['server'],
        )
        squish.clickButton(squish.waitForObject(self.NEXT_BUTTON))

        try:
            squish.clickButton(
                squish.waitForObject(self.CONFIRM_INSECURE_CONNECTION_BUTTON)
            )
        except:
            test.log(
                "No insecure connection warning for server " + clientDetails['server']
            )
            pass

    def addUserCreds(self, context):
        clientDetails = getClientDetails(context)

        squish.type(
            squish.waitForObject(self.USERNAME_BOX),
            clientDetails['user'],
        )
        squish.type(
            squish.waitForObject(self.USERNAME_BOX),
            "<Tab>",
        )
        squish.type(
            squish.waitForObject(self.PASSWORD_BOX),
            clientDetails['password'],
        )
        squish.clickButton(squish.waitForObject(self.NEXT_BUTTON))

    def nextStep(self):
        squish.clickButton(squish.waitForObject(self.NEXT_BUTTON))

    def selectSyncFolder(self, context):
        clientDetails = getClientDetails(context)
        # create sync folder for user
        syncPath = createUserSyncPath(context, clientDetails['user'])

        squish.waitForObject(self.ADVANCED_CONFIGURATION_CHECKBOX).setChecked(True)
        squish.mouseClick(squish.waitForObject(self.DIRECTORY_NAME_BOX))
        squish.type(squish.waitForObject(self.DIRECTORY_NAME_EDIT_BOX), syncPath)
        squish.clickButton(squish.waitForObject(self.CHOOSE_BUTTON))
        test.compare(
            str(squish.waitForObjectExists(self.SELECT_LOCAL_FOLDER).text),
            self.sanitizeFolderPath(syncPath),
        )

    def addAccount(self, context):
        self.addAccountCredential(context)
        self.nextStep()

    def addAccountCredential(self, context):
        self.addServer(context)
        self.addUserCreds(context)
        self.selectSyncFolder(context)

    def selectManualSyncFolderOption(self):
        squish.clickButton(squish.waitForObject(self.CONF_SYNC_MANUALLY_RADIO_BUTTON))

    def selectVirtualFileOption(self):
        squish.clickButton(squish.waitForObject(self.VIRTUAL_FILE_RADIO_BUTTON))

    def confirmEnableExperimentalVFSOption(self):
        squish.clickButton(
            squish.waitForObject(self.ENABLE_EXPERIMENTAL_FEATURE_BUTTON)
        )

    def cancelEnableExperimentalVFSOption(self):
        squish.clickButton(squish.waitForObject(self.STAY_SAFE_BUTTON))
