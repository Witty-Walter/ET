# EPC AI Platform Setup Script

Write-Host "Installing Python requirements..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "Pulling required Ollama LLM models..." -ForegroundColor Green
ollama pull qwen3:8b
ollama pull nomic-embed-text:latest

Write-Host "Setup complete! You can now start the API and Frontend." -ForegroundColor Green
