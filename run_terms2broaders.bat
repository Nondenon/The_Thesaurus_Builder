@echo off
echo Checking required Python libraries (installing if missing)...
python -m pip install --user requests pandas openpyxl tqdm

echo Running the script...
python "%~dp0terms2broaders.py"

pause