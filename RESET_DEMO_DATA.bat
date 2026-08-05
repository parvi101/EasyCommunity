@echo off
cd /d "%~dp0"
if exist data\*.db del /q data\*.db
echo Demo database reset. It will be recreated when the app starts.
