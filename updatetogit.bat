@echo off
cd %cd%
echo currentDirectory: %cd%
git add .
git commit -m "update"
git push -u origin main
pause