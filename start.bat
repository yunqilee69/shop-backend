@echo off
REM 超市后端管理系统启动脚本

echo ========================================
echo 超市后端管理系统
echo ========================================
echo.

echo 正在启动应用...
echo 应用地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.

uv run python main.py

pause
