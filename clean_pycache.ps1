# clean_pycache.ps1
# Script para remover recursivamente todas as pastas __pycache__ a partir do diretório do script

Write-Host "Iniciando a limpeza das pastas __pycache__..." -ForegroundColor Cyan

# Busca e remove todas as pastas __pycache__ recursivamente
$pycacheFolders = Get-ChildItem -Path $PSScriptRoot -Filter "__pycache__" -Recurse -Directory

if ($pycacheFolders) {
    foreach ($folder in $pycacheFolders) {
        Write-Host "Removendo: $($folder.FullName)" -ForegroundColor Yellow
        Remove-Item -Path $folder.FullName -Recurse -Force
    }
    Write-Host "Limpeza concluída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "Nenhuma pasta __pycache__ encontrada." -ForegroundColor Gray
}
