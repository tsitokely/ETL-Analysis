@echo off
title Turnover of customers
color e

echo ..........Please press enter to continue..........
pause > nul
echo Script Started: %date% %time%

echo  ------------------------
echo   Getting Data through SFTP 
echo  ------------------------ 


echo Getting Data started: %date% %time% 
cd WORK_PATH\Purge\scripts
python "1 - sftp.py"

echo  ------------------------
echo   Getting Data completed
echo  ------------------------ 


echo Get Finished: %date% %time%

echo  ------------------------
echo   Insert data in SQLite  
echo  ------------------------ 


echo Insert started: %date% %time%
cd WORK_PATH\Purge\scripts
python "2 - insert_data.py"
cd WORK_PATH\Purge
sqlite3 suivi_purge.db < insert_purge.sql

echo -----------------------
echo  Insert task completed 
echo -----------------------


echo Insert Finished: %date% %time%
cd WORK_PATH\Purge
del insert_purge.sql

echo --------------------------
echo  Analyze data in Database 
echo -------------------------- 


echo Analysis Started: %date% %time%
cd WORK_PATH\Purge\scripts
python "3 - priority_purge.py"

echo -------------------------
echo  Analysis task completed 
echo -------------------------
 
echo Analysis Finished: %date% %time%

echo -------------------------
echo Moving files to directories
echo -------------------------
cd WORK_PATH\Purge\Result
move result_purge_Query*.csv Result_Query
move result_purge_Flag*.csv Result_Flag
move log_priority*.txt Log_priorite
cd WORK_PATH\Purge
move *.csv dumps

echo -------------------------

echo ...Go to results folder to see the files...
pause > nul
echo Script Finished: %date% %time%

