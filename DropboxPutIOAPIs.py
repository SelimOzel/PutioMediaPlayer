'''
Example Links:
https://www.youtube.com/watch?v=fB329zX9wyQ

'''

# To access put.io
import putiopy

# For GUI
import PySimpleGUI as ui

# Handle browser side
import webbrowser

# MACRO: Put.io 
PUT_ID			= 0
PUT_SECRET		= ""
PUT_TOKEN		= ""
PUT_CB 			= ""

# MACRO: User interface
BTN_DOWNLOAD 	= "Download"
BTN_REFRESH 	= "Refresh File List"
BTN_PLAY 		= "Play"

# If this your first time running this program you have to fight.
# Joking aside, set the [authenticate_IN = True] if this is first time
# so you allow Put.io with your web app.
def ConfigurePutIOClient(id_IN, secret_IN, token_IN, callback_IN, authenticate_IN):
	# Just annoying numbers and values to keep track of...
	CLIENT_ID = id_IN
	CLIENT_SECRET = secret_IN
	OAUTH_TOKEN = token_IN
	CALLBACK_URL = callback_IN

	# Some authentication code I copy pasted from their github.
	# Only works if specified by function call.
	if(authenticate_IN):
		helper = putiopy.AuthHelper(CLIENT_ID, CLIENT_SECRET, CALLBACK_URL, type='token')
		helper.open_authentication_url()

	# Set client here.
	client = putiopy.Client(OAUTH_TOKEN)

	return client

def Transfer(client_IN, url_IN):
	transfer = client_IN.Transfer.add_url(url_IN)

def main():
	# Contains all *.mp4 files in the main folder
	mainFolderNameList = []
	mainFolderIDList = []

	# One liner config
	mediaClient = ConfigurePutIOClient(PUT_ID, PUT_SECRET, PUT_TOKEN, PUT_CB, False)

	# Main page layout
	layout = [ 
				[ui.Text('Media Player', size=(30, 1), font=("Helvetica", 25), text_color='black')],
				[ui.Text('Copy-paste download URL below:'), ui.Button(BTN_DOWNLOAD)],
				[ui.InputText()],
				[ui.Text('List of *.mp4 files:'), ui.Button(BTN_REFRESH)],
				[ui.Listbox(values=['Empty'], size=(30, 6), key='_FileList_')],
				[ui.Button(BTN_PLAY)]
	]
	mediaWindow  = ui.Window('Put.io Media Player', layout, auto_size_text=True, default_element_size=(40, 1))

	# Run forever.
	while (True):
		event, values = mediaWindow.Read(timeout=10)

		if(event == BTN_REFRESH):
			fileList_NonString = mediaClient.File.list()
			newNameList_Local = []
			newIDList_Local = []
			for file in fileList_NonString:
				if(file.name[-4:] == '.mp4'):
					newNameList_Local.append(file.name)
					newIDList_Local.append(file.id)

			# Update folder list at program memory
			mainFolderNameList = newNameList_Local
			mainFolderIDList = newIDList_Local
			mediaWindow.Element('_FileList_').Update(mainFolderNameList)

		if(event == BTN_DOWNLOAD):
			Transfer(mediaClient, values[0])

		if(event == BTN_PLAY):
			# Name of current selected *.mp4 in the UI list
			currentName = values['_FileList_']

			# Its index in the UI list
			index = newNameList_Local.index(currentName[0])
			
			# Now get the file from the put.io API
			myFile = mediaClient.File.get(newIDList_Local[index])

			# This call gets the streaming link using put.io API
			webbrowser.open_new(mediaClient.File.get_stream_link(myFile))

if __name__ == "__main__":
    main()