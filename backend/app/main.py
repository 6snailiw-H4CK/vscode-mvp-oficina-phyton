"""Aplicação Principal FastAPI"""
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.database import Base, engine, SessionLocal
from sqlalchemy.exc import OperationalError
from app.models.cliente import Cliente
from app.models.fornecedor import Fornecedor
from app.models.produto import Produto
from app.models.ordem_servico import OrdemServico, StatusOS
from app.routes import clientes, fornecedores, produtos, estoque, ordem_servico, demo

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema Simples - Gestão de Estoque e Ordem de Serviço"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(clientes.router, prefix=settings.api_prefix)
app.include_router(fornecedores.router, prefix=settings.api_prefix)
app.include_router(produtos.router, prefix=settings.api_prefix)
app.include_router(estoque.router, prefix=settings.api_prefix)
app.include_router(ordem_servico.router, prefix=settings.api_prefix)
app.include_router(demo.router, prefix=settings.api_prefix)


def initialize_database() -> None:
    """Cria as tabelas no banco de dados se possível.
    Também aplica alterações simples em esquemas para ambientes SQLite (ALTER TABLE add column) quando necessário.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso.")

        # Se SQLite, verificar colunas adicionais que possam ter sido adicionadas ao modelo
        if settings.database_url.startswith("sqlite"):
            try:
                with engine.connect() as conn:
                    # Verifica se coluna valor_pago existe na tabela ordens_servico
                    res = conn.execute("PRAGMA table_info('ordens_servico')").fetchall()
                    cols = [r[1] for r in res]
                    if 'valor_pago' not in cols:
                        logger.info("Adicionando coluna 'valor_pago' em ordens_servico (SQLite)")
                        conn.execute("ALTER TABLE ordens_servico ADD COLUMN valor_pago FLOAT")
            except Exception as e:
                logger.warning(f"Falha ao ajustar esquema SQLite automaticamente: {e}")

    except OperationalError as e:
        logger.warning(f"Não foi possível inicializar o banco de dados: {e}")



def seed_demo_data() -> None:
    """Insere dados de exemplo em SQLite para testes locais."""
    if not settings.database_url.startswith("sqlite"):
        return

    db = SessionLocal()
    try:
        if db.query(Cliente).count() == 0:
            db.add_all([
                Cliente(nome="João Silva", cpf_cnpj="123.456.789-00", email="joao@email.com",
                        telefone="11-99999-1001", cidade="São Paulo", estado="SP"),
                Cliente(nome="Maria Santos", cpf_cnpj="987.654.321-00", email="maria@email.com",
                        telefone="21-99999-1002", cidade="Rio de Janeiro", estado="RJ")
            ])
            logger.info("Clientes de exemplo inseridos.")

        if db.query(Fornecedor).count() == 0:
            db.add_all([
                Fornecedor(nome="Fornecedor ABC Ltda", cnpj="12.345.678/0001-90",
                           email="contato@fornecedorabc.com", telefone="11-99999-0001",
                           cidade="São Paulo", estado="SP"),
                Fornecedor(nome="Distribuidor XYZ", cnpj="98.765.432/0001-10",
                           email="vendas@distribuidorxyz.com", telefone="21-99999-0002",
                           cidade="Rio de Janeiro", estado="RJ")
            ])
            logger.info("Fornecedores de exemplo inseridos.")

        if db.query(Produto).count() == 0:
            db.add_all([
                Produto(nome="Produto A", sku="SKU-001", descricao="Descrição do Produto A",
                        categoria="Eletrônicos", quantidade_atual=50, quantidade_minima=10,
                        preco_custo=100.00, preco_venda=150.00, fornecedor_id=1),
                Produto(nome="Produto B", sku="SKU-002", descricao="Descrição do Produto B",
                        categoria="Vestuário", quantidade_atual=30, quantidade_minima=5,
                        preco_custo=50.00, preco_venda=80.00, fornecedor_id=2)
            ])
            logger.info("Produtos de exemplo inseridos.")

        if db.query(OrdemServico).count() == 0:
            db.add_all([
                OrdemServico(numero="OS-20260429-001", cliente_id=1, 
                            descricao="Manutenção de computador", 
                            tecnico_responsavel="Carlos Silva",
                            status=StatusOS.ABERTA,
                            valor_estimado=500.00),
                OrdemServico(numero="OS-20260428-002", cliente_id=2,
                            descricao="Repair de notebook",
                            tecnico_responsavel="Ana Costa", 
                            status=StatusOS.EM_ANDAMENTO,
                            valor_estimado=350.00)
            ])
            logger.info("Ordens de Serviço de exemplo inseridas.")

        db.commit()
    except Exception as e:
        logger.warning(f"Falha ao inserir dados de exemplo: {e}")
        db.rollback()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()
    seed_demo_data()


# Servir arquivos estáticos (CSS, JS)
try:
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
    if os.path.exists(frontend_path):
        app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
        app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")
        logger.info(f"Frontend montado: {frontend_path}")
    else:
        logger.warning(f"Diretório frontend não encontrado: {frontend_path}")
except Exception as e:
    logger.warning(f"Erro ao montar arquivos estáticos: {e}")
    
# Servir arquivo index.html na raiz
@app.get("/", tags=["Frontend"])
async def index():
    """Serve a página inicial"""
    try:
        import os
        frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html"))
        return FileResponse(frontend_path)
    except Exception as e:
        logger.error(f"Erro ao servir index.html: {e}")
        return {
            "message": "Bem-vindo ao Sistema Simples!",
            "docs": "/docs",
            "api": "/api/v1"
        }


@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version
    }


@app.get("/test", tags=["Frontend"])
async def test_page():
    """Página de teste"""
    try:
        frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "test.html"))
        return FileResponse(frontend_path)
    except Exception as e:
        logger.error(f"Erro ao servir test.html: {e}")
        return {"error": str(e)}


@app.get("/{page_name}.html", tags=["Frontend"])
async def serve_html(page_name: str):
    """Serve outras páginas HTML do frontend"""
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", f"{page_name}.html"))
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    raise HTTPException(status_code=404, detail="Página não encontrada")


@app.get("/api/v1")
async def api_root():
    """Retorna informações da API"""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "clientes": "/api/v1/clientes",
            "fornecedores": "/api/v1/fornecedores",
            "produtos": "/api/v1/produtos",
            "estoque": "/api/v1/estoque",
            "ordens_servico": "/api/v1/ordens-servico"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
