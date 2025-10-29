@echo off
REM setup.bat - Script d'installation pour VisionOCR (Windows)

echo ================================================================
echo            Installation de VisionOCR v1.0.0
echo ================================================================
echo.

REM Vérifier Python
echo Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo Telechargez Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detecte
echo.

REM Avertissement poppler
echo Verification de poppler-utils...
echo [INFO] Sur Windows, poppler doit etre installe manuellement
echo Telechargez depuis: https://github.com/oschwartz10612/poppler-windows/releases/
echo Et ajoutez le dossier bin au PATH
echo.
pause

REM Créer l'environnement virtuel
echo.
echo Creation de l'environnement virtuel...
if exist venv (
    echo [INFO] L'environnement virtuel existe deja
    choice /C YN /M "Le recreer ?"
    if errorlevel 2 goto skip_venv
    rmdir /s /q venv
)

python -m venv venv
echo [OK] Environnement virtuel cree
:skip_venv

REM Activer l'environnement virtuel
echo.
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo.
echo Installation des dependances...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [OK] Dependances installees

REM Créer les répertoires
echo.
echo Creation des repertoires...
if not exist credentials mkdir credentials
if not exist logs mkdir logs
if not exist .cache\vision_api mkdir .cache\vision_api
if not exist examples\input mkdir examples\input
if not exist examples\output mkdir examples\output
echo [OK] Repertoires crees

REM Copier .env.example
if not exist .env (
    echo.
    echo Creation du fichier .env...
    copy .env.example .env
    echo [OK] Fichier .env cree
)

REM Instructions finales
echo.
echo ================================================================
echo              Installation terminee !
echo ================================================================
echo.
echo Prochaines etapes :
echo.
echo 1. Configurer Google Cloud Vision API :
echo    python main.py setup
echo.
echo 2. Placer votre fichier credentials.json dans credentials\
echo.
echo 3. (Optionnel) Editer le fichier .env
echo.
echo 4. Tester l'installation :
echo    python main.py --help
echo.
echo 5. Convertir votre premier PDF :
echo    python main.py convert votre_document.pdf
echo.
echo Documentation complete : README.md
echo.
echo Pour activer l'environnement virtuel :
echo    venv\Scripts\activate.bat
echo.
pause
