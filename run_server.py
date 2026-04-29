#!/usr/bin/env python
"""Script para iniciar o servidor FastAPI"""
import os
import sys
import uvicorn

# Adicionar o diretório backend ao path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
