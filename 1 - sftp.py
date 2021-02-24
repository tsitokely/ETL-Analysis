# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:29:13 2017

@author: Tsitohaina
"""

import paramiko
import datetime as dt
import os

# Avoir la date du jour sous format YYYYMMDD
now = dt.datetime.now()
currDate = now.strftime("%Y%m%d")
# Using to test currDate = '20170125'

#Set different paths
workingDir = os.path.join('WORK_PATH')
cwd = os.getcwd()

#Création des logs
logFileDir = os.path.join(workingDir,'Logs')
logName = r'paramiko_purge_%s.log' % currDate
logFile = os.path.join(logFileDir,logName)
paramiko.util.log_to_file(logFile)

# Déclaration du host / Open transport
host = "X.X.X.X"
port = 22
transport = paramiko.Transport((host,port))


CurrFile = os.path.join(workingDir,r'working_file%s.csv' % currDate)
workFile = os.path.join(cwd,r'working_file%s.csv' % currDate)

# Connexion 
transport.connect(username = 'username' , password = 'password')

# Go
sftp = paramiko.SFTPClient.from_transport(transport)

# Download the file
dir_remote = 'DIR_REMOTE'
file_remote = dir_remote + 'working_file%s.csv' % currDate

#Using default C:\Users\toe
sftp.get(file_remote,r'./working_file%s.csv' % currDate)

#move du fichier dans la purge
os.rename(workFile,CurrFile)


sftp.close()
transport.close()