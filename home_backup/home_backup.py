#!/usr/bin/env python

import os
import shutil
import logging
import RSyncBackup
import time

logging.basicConfig()

# Functions


def check_dir_exist(os_dir):
	if not os.path.exists(os_dir):
		print os_dir, "does not exist."
		exit(1)


def confirm():
	gogo = raw_input("Continue? yes/no\n")
	global exit_condition
	if gogo == 'yes':
		exit_condition = 0
		return exit_condition
	elif gogo == "no":
		exit_condition = 1
		return exit_condition
	else:
		print "Please answer with yes or no."
		confirm()


def delete_files(ending):
	os.chdir(backup_path)
	for r, d, f in os.walk(backup_path):
		for files in f:
			if files.endswith("." + ending):
				os.remove(os.path.join(r, files))


# Specify what and where to backup.
backup_path = raw_input("What should be backed up today?\n")
check_dir_exist(backup_path)
print "Okay", backup_path, "will be saved."
time.sleep(3)

backup_to_path = raw_input("Where to backup?")
check_dir_exist(backup_to_path)


# Delete files first
print "First, let's cleanup unnecessary files in the backup path."
file_types = ["tmp", "bak", "dmp"]
for file_type in file_types:
	print "Delete", file_type, "files?"
	confirm()
	if exit_condition == 0:
		delete_files(file_type)


# Empty trash can
print "Empty trash can?"
confirm()
if exit_condition == 0:
	print "emptying"
	shutil.rmtree("~/.local/share/Trash/files")


# Do the actual backup
print "Doing the backup now!"
confirm()
if exit_condition == 1:
		print "Aborting!"
		exit(1)


backup = RSyncBackup.RSyncBackup(rsync="/usr/bin/rsync")

backup.backup(source = backup_path,
	destination = backup_to_path+"/",
	excludeList = ['lost+found', '/sys', '/tmp', '/proc', '/mnt', '/dev', '/backup'])