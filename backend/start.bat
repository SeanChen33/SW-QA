@echo off
echo 启动后端服务...
echo.
echo 如果8000端口被占用，将尝试使用8001端口
echo.

netstat -ano | findstr :8000 >nul
if %errorlevel% == 0 (
    echo 端口8000已被占用，使用8001端口启动...
    python main.py 8001
) else (
    echo 使用8000端口启动...
    python main.py 8000
)

pause

