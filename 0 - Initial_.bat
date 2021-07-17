@echo off
title Initial script
color e

echo ..........Please press enter to continue..........
pause > nul
echo Script Started: %date% %time%

echo  ------------------------
echo   Getting Data through SFTP 
echo  ------------------------ 


echo Getting Data started: %date% %time% 
cd WORK_PATH\scripts
python "1 - sftp.py"

echo  ------------------------
echo   Data download completed
echo  ------------------------ 


echo Download finished on: %date% %time%

echo  ------------------------
echo   Insert data in SQLite DB 
echo  ------------------------ 


echo Insert started on: %date% %time%
cd WORK_PATH\scripts
python "2 - insert_data.py"
cd WORK_PATH\Data
sqlite3 data.db < insert_query.sql

echo -----------------------
echo  DB load completed 
echo -----------------------


echo DB load completed on: %date% %time%
cd WORK_PATH\Data
del insert_query.sql

echo --------------------------
echo  Analyze data in DB 
echo -------------------------- 


echo Analysis Started on: %date% %time%
cd WORK_PATH\scripts
python "3 - analysis.py"

echo -------------------------
echo  Analysis task completed 
echo -------------------------
 
echo Analysis Finished on: %date% %time%

echo -------------------------
echo Moving files to directories
echo -------------------------
cd WORK_PATH\Result
move result_data*.csv Result_Data
move result_data_Flag*.csv Result_Flag
move log*.txt Logs
cd WORK_PATH\Data
move *.csv dumps

echo -------------------------

echo ...Go to results folder to see the files...
pause > nul
echo All tasks completed on: %date% %time%

