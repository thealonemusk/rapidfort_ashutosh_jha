@echo off
REM Check if the image name parameter is provided
IF "%~1"=="" (
    echo Usage: start.bat ^<image-name^>
    exit /b 1
)

REM Build Docker image
docker build -t %~1 .

REM Run Docker container
docker run -p 8080:8080 %~1
