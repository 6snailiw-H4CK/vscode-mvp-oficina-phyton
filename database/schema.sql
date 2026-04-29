-- ============================================
-- SISTEMA SIMPLES - SCHEMA POSTGRESQL
-- ============================================

-- Criar database se não existir
CREATE DATABASE sistema_simples;

-- ============================================
-- TABELA: CLIENTES
-- ============================================
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf_cnpj VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco VARCHAR(255),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    
    INDEX idx_nome (nome),
    INDEX idx_cpf_cnpj (cpf_cnpj),
    INDEX idx_email (email)
);

-- ============================================
-- TABELA: FORNECEDORES
-- ============================================
CREATE TABLE fornecedores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(20) UNIQUE,
    contato VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco VARCHAR(255),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    
    INDEX idx_nome (nome),
    INDEX idx_cnpj (cnpj),
    INDEX idx_email (email)
);

-- ============================================
-- TABELA: PRODUTOS
-- ============================================
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    sku VARCHAR(50) UNIQUE,
    descricao VARCHAR(500),
    categoria VARCHAR(50),
    quantidade_atual INTEGER DEFAULT 0,
    quantidade_minima INTEGER DEFAULT 0,
    preco_custo NUMERIC(10,2),
    preco_venda NUMERIC(10,2) NOT NULL,
    fornecedor_id INTEGER REFERENCES fornecedores(id) ON DELETE SET NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    
    INDEX idx_nome (nome),
    INDEX idx_sku (sku),
    INDEX idx_categoria (categoria),
    INDEX idx_fornecedor_id (fornecedor_id)
);

-- ============================================
-- TABELA: MOVIMENTAÇÕES DE ESTOQUE
-- ============================================
CREATE TABLE movimentacoes_estoque (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER NOT NULL REFERENCES produtos(id) ON DELETE CASCADE,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    quantidade INTEGER NOT NULL,
    motivo VARCHAR(100),
    observacao VARCHAR(500),
    data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INTEGER,
    
    INDEX idx_produto_id (produto_id),
    INDEX idx_data_movimento (data_movimento)
);

-- ============================================
-- TABELA: ORDENS DE SERVIÇO
-- ============================================
CREATE TABLE ordens_servico (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(20) UNIQUE NOT NULL,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ABERTA' CHECK (status IN ('ABERTA', 'EM_ANDAMENTO', 'FECHADA', 'CANCELADA')),
    tecnico_responsavel VARCHAR(100),
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_prevista_conclusao TIMESTAMP,
    data_conclusao TIMESTAMP,
    valor_estimado NUMERIC(10,2),
    valor_final NUMERIC(10,2),
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_numero (numero),
    INDEX idx_cliente_id (cliente_id),
    INDEX idx_status (status),
    INDEX idx_data_abertura (data_abertura)
);

-- ============================================
-- TABELA: ITENS DE ORDEM DE SERVIÇO
-- ============================================
CREATE TABLE ordens_servico_itens (
    id SERIAL PRIMARY KEY,
    ordem_servico_id INTEGER NOT NULL REFERENCES ordens_servico(id) ON DELETE CASCADE,
    produto_id INTEGER REFERENCES produtos(id) ON DELETE SET NULL,
    descricao VARCHAR(255),
    quantidade INTEGER NOT NULL DEFAULT 1,
    valor_unitario NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    
    INDEX idx_ordem_servico_id (ordem_servico_id),
    INDEX idx_produto_id (produto_id)
);

-- ============================================
-- TABELA: AUDITORIA
-- ============================================
CREATE TABLE auditoria (
    id SERIAL PRIMARY KEY,
    modulo VARCHAR(50) NOT NULL,
    operacao VARCHAR(50) NOT NULL,
    tabela VARCHAR(50) NOT NULL,
    registro_id INTEGER NOT NULL,
    usuario VARCHAR(100),
    descricao TEXT,
    dados_antes TEXT,
    dados_depois TEXT,
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_modulo (modulo),
    INDEX idx_tabela (tabela),
    INDEX idx_data_operacao (data_operacao)
);

-- ============================================
-- DADOS DE EXEMPLO
-- ============================================

INSERT INTO fornecedores (nome, cnpj, email, telefone, cidade, estado, ativo) VALUES
('Fornecedor ABC Ltda', '12.345.678/0001-90', 'contato@fornecedorabc.com', '11-99999-0001', 'São Paulo', 'SP', TRUE),
('Distribuidor XYZ', '98.765.432/0001-10', 'vendas@distribuidorxyz.com', '21-99999-0002', 'Rio de Janeiro', 'RJ', TRUE);

INSERT INTO clientes (nome, cpf_cnpj, email, telefone, cidade, estado, ativo) VALUES
('João Silva', '123.456.789-00', 'joao@email.com', '11-99999-1001', 'São Paulo', 'SP', TRUE),
('Maria Santos', '987.654.321-00', 'maria@email.com', '21-99999-1002', 'Rio de Janeiro', 'RJ', TRUE),
('Empresa Ltda', '11.222.333/0001-44', 'contato@empresa.com', '31-99999-1003', 'Belo Horizonte', 'MG', TRUE);

INSERT INTO produtos (nome, sku, descricao, categoria, quantidade_atual, quantidade_minima, preco_custo, preco_venda, fornecedor_id, ativo) VALUES
('Produto A', 'SKU-001', 'Descrição do Produto A', 'Eletrônicos', 50, 10, 100.00, 150.00, 1, TRUE),
('Produto B', 'SKU-002', 'Descrição do Produto B', 'Vestuário', 30, 5, 50.00, 80.00, 2, TRUE),
('Produto C', 'SKU-003', 'Descrição do Produto C', 'Alimentos', 100, 20, 5.00, 10.00, 1, TRUE);

INSERT INTO ordens_servico (numero, cliente_id, descricao, status, tecnico_responsavel, valor_estimado, ativo) VALUES
('OS-20260101-A1B2', 1, 'Manutenção do equipamento', 'ABERTA', 'Carlos Silva', 500.00, TRUE),
('OS-20260102-C3D4', 2, 'Instalação e configuração', 'EM_ANDAMENTO', 'Ana Costa', 800.00, TRUE);

-- ============================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- ============================================
CREATE INDEX idx_produtos_fornecedor ON produtos(fornecedor_id);
CREATE INDEX idx_ordens_cliente ON ordens_servico(cliente_id);
CREATE INDEX idx_ordens_status ON ordens_servico(status);
CREATE INDEX idx_movimentacoes_produto ON movimentacoes_estoque(produto_id);

-- ============================================
-- VIEWS ÚTEIS
-- ============================================

-- View: Resumo de Estoque
CREATE OR REPLACE VIEW vw_resumo_estoque AS
SELECT 
    p.id,
    p.nome,
    p.sku,
    p.categoria,
    p.quantidade_atual,
    p.quantidade_minima,
    (p.quantidade_atual <= p.quantidade_minima) as estoque_baixo,
    p.preco_venda,
    (p.quantidade_atual * p.preco_venda) as valor_total,
    f.nome as fornecedor
FROM produtos p
LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
WHERE p.ativo = TRUE;

-- View: Ordens de Serviço Abertas
CREATE OR REPLACE VIEW vw_ordens_abertas AS
SELECT 
    os.id,
    os.numero,
    c.nome as cliente,
    os.descricao,
    os.status,
    os.tecnico_responsavel,
    os.data_abertura,
    os.valor_estimado
FROM ordens_servico os
JOIN clientes c ON os.cliente_id = c.id
WHERE os.status IN ('ABERTA', 'EM_ANDAMENTO')
ORDER BY os.data_abertura DESC;
