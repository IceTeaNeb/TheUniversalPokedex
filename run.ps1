#!/usr/bin/env pwsh
# Run The Universal Pokedex using the top-level .venv
Set-Location "$PSScriptRoot"
. 'C:\Users\Belinda\GitStuff\.venv\Scripts\Activate.ps1'
Write-Host "Using python: $(python -c 'import sys; print(sys.executable)')"
python 'C:\Users\Belinda\GitStuff\TheUniversalPokedex\The Universal Pokedex.py'
