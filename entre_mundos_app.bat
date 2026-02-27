@echo off
echo ============== Checking updates ===============
call git pull
if %ERRORLEVEL% == 0 goto :proceed

:proceed
call python -c "import virtualenv" > nul 2>&1
if %ERRORLEVEL% == 0 goto :activatevenv
echo ====== Installing the virtualenv package ======
call python -m pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install virtualenv


:activatevenv
echo ======= Activating virtual environment ========
call venv\Scripts\activate > nul 2>&1
if %ERRORLEVEL% == 0 goto :installpkg
echo ======== Creating virtual environment =========
call python -m venv venv
call venv\Scripts\activate

:installpkg
call python -c "import entre_mundos_app" > nul 2>&1
if %ERRORLEVEL% == 0 goto :endofscript
echo ========= Installing the application ==========
call python -m pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install -e .

:endofscript
cls
echo ===================================================
echo ===            Software Entre Mundos            ===
echo ===================================================
call python -m streamlit run "entre_mundos_app\main.py"
pause