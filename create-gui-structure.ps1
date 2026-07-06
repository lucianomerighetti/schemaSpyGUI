<#
.SYNOPSIS
Cria a estrutura padrão do Frontend PyQt6 do SchemaSpy GUI

.DESCRIPTION
Constrói toda a estrutura MVVM do frontend desktop.

Autor: M2D
Projeto: SchemaSpy GUI v2
#>

param(
    [string]$RootPath = "."
)

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " SchemaSpy GUI - Frontend Structure" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$GuiRoot = Join-Path $RootPath "application\platform\frontend\apps\gui"

if (!(Test-Path $GuiRoot))
{
    New-Item -ItemType Directory -Path $GuiRoot -Force | Out-Null
}

$Folders = @(

    # App
    "app",

    # Assets
    "assets",
    "assets\icons",
    "assets\images",
    "assets\styles",

    # Core
    "core",
    "core\config",
    "core\constants",
    "core\events",
    "core\exceptions",
    "core\logging",
    "core\security",

    # Infrastructure
    "infrastructure",
    "infrastructure\api",
    "infrastructure\database",
    "infrastructure\filesystem",
    "infrastructure\schemaspy",

    # Shared
    "shared",
    "shared\components",
    "shared\dialogs",
    "shared\widgets",
    "shared\layouts",
    "shared\themes",

    # Modules
    "modules",

    # Home
    "modules\home",
    "modules\home\views",
    "modules\home\viewmodels",
    "modules\home\services",

    # Projects
    "modules\projects",
    "modules\projects\views",
    "modules\projects\viewmodels",
    "modules\projects\services",
    "modules\projects\models",

    # Connections
    "modules\connections",
    "modules\connections\views",
    "modules\connections\viewmodels",
    "modules\connections\services",
    "modules\connections\models",

    # Analysis
    "modules\analysis",
    "modules\analysis\views",
    "modules\analysis\viewmodels",
    "modules\analysis\services",
    "modules\analysis\models",

    # Execution
    "modules\execution",
    "modules\execution\views",
    "modules\execution\viewmodels",
    "modules\execution\services",

    # History
    "modules\history",
    "modules\history\views",
    "modules\history\viewmodels",
    "modules\history\services",

    # Settings
    "modules\settings",
    "modules\settings\views",
    "modules\settings\viewmodels",
    "modules\settings\services",

    # About
    "modules\about",
    "modules\about\views",
    "modules\about\viewmodels",

    # Tests
    "tests",
    "tests\unit",
    "tests\integration"
)

foreach ($Folder in $Folders)
{
    $Path = Join-Path $GuiRoot $Folder

    if (!(Test-Path $Path))
    {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "[OK] $Folder" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Criando arquivos base..." -ForegroundColor Yellow

$Files = @(

    # Root
    "main.py",
    "requirements.txt",
    ".env",
    ".gitignore",

    # App
    "app\application.py",
    "app\bootstrap.py",
    "app\startup.py",

    # Core
    "core\config\settings.py",
    "core\logging\logger.py",

    # Database
    "infrastructure\database\database.py",
    "infrastructure\database\session.py",

    # Shared
    "shared\themes\dark_theme.py",
    "shared\themes\light_theme.py",

    # Main Components
    "shared\components\main_window.py",
    "shared\components\sidebar.py",
    "shared\components\status_bar.py",

    # Dashboard
    "modules\home\views\dashboard_view.py",
    "modules\home\viewmodels\dashboard_viewmodel.py",

    # Projects
    "modules\projects\views\project_view.py",
    "modules\projects\viewmodels\project_viewmodel.py",

    # Connections
    "modules\connections\views\connection_view.py",
    "modules\connections\viewmodels\connection_viewmodel.py",

    # Execution
    "modules\execution\views\execution_view.py",
    "modules\execution\viewmodels\execution_viewmodel.py",

    # History
    "modules\history\views\history_view.py",
    "modules\history\viewmodels\history_viewmodel.py",

    # Settings
    "modules\settings\views\settings_view.py",
    "modules\settings\viewmodels\settings_viewmodel.py",

    # About
    "modules\about\views\about_view.py"
)

foreach ($File in $Files)
{
    $FilePath = Join-Path $GuiRoot $File

    if (!(Test-Path $FilePath))
    {
        New-Item -ItemType File -Path $FilePath -Force | Out-Null
        Write-Host "[FILE] $File" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "Criando __init__.py..." -ForegroundColor Yellow

Get-ChildItem $GuiRoot -Directory -Recurse | ForEach-Object {

    $InitFile = Join-Path $_.FullName "__init__.py"

    if (!(Test-Path $InitFile))
    {
        New-Item -ItemType File -Path $InitFile -Force | Out-Null
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " Estrutura Frontend criada com sucesso" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""