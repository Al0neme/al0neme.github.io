@echo off
cd %CD%
echo currentDirectory: %cd%

::更新pagefind html索引
rmdir /s /q pagefind
pagefind_extended.exe -s . --output-path pagefind

:: 推送到仓库
git add .
git commit -m "update"
git push -u origin main

pause