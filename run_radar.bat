@echo off
chcp 65001 >nul
title 运行新词雷达 (new-term-radar)
echo ===================================================
echo   正在运行新词雷达每日扫描...
echo ===================================================
python -m radar daily --skip x,newsites,revenue,asks,sellers,review,judge,usecases --out report.md
if errorlevel 1 goto error
echo.
echo ===================================================
echo   扫描完成，更新网页静态文件...
echo ===================================================
python scripts/build_dist.py
if errorlevel 1 goto error
echo.
echo ===================================================
echo   完成！最新报告已保存至 report.md 与 dist/index.html
echo   如需发布上线，请运行 deploy.bat
echo ===================================================
pause
exit /b 0

:error
echo ===================================================
echo   执行失败，请检查报错信息。
echo ===================================================
pause
exit /b 1
