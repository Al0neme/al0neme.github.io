@echo off
cd %CD%
echo currentDirectory: %cd%

::复制搜索的html文章到博客Html目录
copy C:\syn-notes\Wiki\html文章\* C:\al0neme.github.io\Html\

::更新pagefind html索引
rmdir /s /q pagefind
pagefind_extended.exe -s . --output-path pagefind

:: 推送到仓库
git add .
git commit -m "update"
git push -u origin main

pause