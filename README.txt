Django project - Trash Explorer

uses smrm module to work with Trash
python version - 2.7
Django version - 1.11.4

to run:
	python manage.py runserver

modules:
	utils.py
		Module with some utils which is used in views of app

web:
	Trash List page:
		list of created Trashes, click "Edit" to edit Trash
		To get in Trash click the name of Trash
	Add Task page:
		creating new Trash, and saving it to datebase
	Task List page:	
		list of created Tasks, click "Update" to edit Task
		click "run" to run task
		after running it will return results, to see them - click "Done
	File Exlporer:
	 	green - files
		gray - directiries
	
