#!/bin/bash
# Script para iniciar o Sistema Simples com Docker

echo "=================================================="
echo "Sistema Simples - Iniciando Aplicação"
echo "=================================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale Docker."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale Docker Compose."
    exit 1
fi

# Build e inicie os containers
echo ""
echo "🔨 Construindo e iniciando containers..."
docker-compose up -d

# Aguardar inicialização
echo ""
echo "⏳ Aguardando inicialização do PostgreSQL..."
sleep 10

# Verificar saúde do banco
echo ""
echo "✅ Containers iniciados!"
echo ""
echo "=================================================="
echo "Sistema Simples - PRONTO PARA USAR"
echo "=================================================="
echo ""
echo "🌐 Acessar a aplicação:"
echo "   Frontend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📊 Banco de Dados:"
echo "   Host: localhost:5432"
echo "   Usuario: postgres"
echo "   Senha: postgres"
echo "   Database: sistema_simples"
echo ""
echo "🛑 Para parar a aplicação:"
echo "   docker-compose down"
echo ""
echo "📝 Ver logs:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f postgres"
echo ""
echo "=================================================="
