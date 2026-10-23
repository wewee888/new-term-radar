@echo off
chcp 65001 >nul
title 上传部署到 Cloudflare Pages
echo ===================================================
echo   正在生成网页仪表盘并部署至 Cloudflare Pages...
echo ===================================================
python scripts/build_dist.py
if errorlevel 1 goto error
npx wrangler pages deploy dist --project-name new-term-radar --branch main --commit-dirty=true
if errorlevel 1 goto error
echo ===================================================
echo   部署成功!
echo   访问地址: https://new-term-radar-49k.pages.dev/
echo ===================================================
pause
exit /b 0

:error
echo ===================================================
echo   部署失败，请检查上方日志。
echo ===================================================
pause
exit /b 1
