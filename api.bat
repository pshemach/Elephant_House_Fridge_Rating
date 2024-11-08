@echo off
cd /d D:\YoloV8\Elephant_House_Fridge_Rating  REM Change this to your app directory

REM Activate the virtual environment
call .venv\Scripts\activate

REM Run the Flask app (adjust this line if you are using Waitress or another server)
waitress-serve --host=0.0.0.0 --port=5051 demo:app
