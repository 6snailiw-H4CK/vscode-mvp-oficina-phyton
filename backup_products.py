#!/usr/bin/env python3
"""Backup/exportação de produtos do banco de dados do SistemaSimples."""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'backend'))

try:
    from app.database import SessionLocal
    from app.models.produto import Produto
    from app.models.fornecedor import Fornecedor
except ImportError as exc:
    raise ImportError(
        'Não foi possível importar o pacote de backend. ' \
        'Execute este script a partir da raiz do repositório SistemaSimples.'
    ) from exc

HEADERS = [
    'id',
    'nome',
    'sku',
    'descricao',
    'categoria',
    'quantidade_atual',
    'quantidade_minima',
    'preco_custo',
    'preco_venda',
    'fornecedor_id',
    'fornecedor_nome',
    'ativo',
    'data_cadastro',
    'data_atualizacao',
]


def carregar_produtos(include_inativos: bool = False) -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        query = db.query(Produto).outerjoin(Fornecedor, Produto.fornecedor_id == Fornecedor.id)
        if not include_inativos:
            query = query.filter(Produto.ativo == True)
        produtos = query.all()

        resultados = []
        for produto in produtos:
            fornecedor_nome = None
            if produto.fornecedor_id is not None:
                fornecedor = db.query(Fornecedor).filter(Fornecedor.id == produto.fornecedor_id).first()
                fornecedor_nome = fornecedor.nome if fornecedor else None

            resultados.append({
                'id': produto.id,
                'nome': produto.nome,
                'sku': produto.sku or '',
                'descricao': produto.descricao or '',
                'categoria': produto.categoria or '',
                'quantidade_atual': produto.quantidade_atual,
                'quantidade_minima': produto.quantidade_minima,
                'preco_custo': produto.preco_custo if produto.preco_custo is not None else '',
                'preco_venda': produto.preco_venda,
                'fornecedor_id': produto.fornecedor_id if produto.fornecedor_id is not None else '',
                'fornecedor_nome': fornecedor_nome or '',
                'ativo': produto.ativo,
                'data_cadastro': produto.data_cadastro.isoformat() if produto.data_cadastro else '',
                'data_atualizacao': produto.data_atualizacao.isoformat() if produto.data_atualizacao else '',
            })

        return resultados
    finally:
        db.close()


def export_csv(produtos: List[Dict[str, Any]], output_path: Path) -> None:
    with output_path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(produtos)
    print(f'Backup criado: {output_path} ({len(produtos)} produtos)')


def export_json(produtos: List[Dict[str, Any]], output_path: Path) -> None:
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)
    print(f'Backup criado: {output_path} ({len(produtos)} produtos)')


def export_xlsx(produtos: List[Dict[str, Any]], output_path: Path) -> None:
    try:
        from openpyxl import Workbook
    except ImportError as exc:
        raise ImportError(
            'openpyxl não está instalado. Execute: pip install openpyxl'
        ) from exc

    wb = Workbook()
    ws = wb.active
    ws.title = 'produtos'
    ws.append(HEADERS)

    for produto in produtos:
        ws.append([produto.get(col, '') for col in HEADERS])

    wb.save(output_path)
    print(f'Backup criado: {output_path} ({len(produtos)} produtos)')


def criar_template(output_path: Path, formato: str) -> None:
    if formato == 'csv':
        with output_path.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(HEADERS)
        print(f'Template CSV criado: {output_path}')
    elif formato == 'json':
        with output_path.open('w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f'Template JSON criado: {output_path}')
    elif formato == 'xlsx':
        try:
            from openpyxl import Workbook
        except ImportError as exc:
            raise ImportError(
                'openpyxl não está instalado. Execute: pip install openpyxl'
            ) from exc
        wb = Workbook()
        ws = wb.active
        ws.title = 'produtos'
        ws.append(HEADERS)
        wb.save(output_path)
        print(f'Template XLSX criado: {output_path}')
    else:
        raise ValueError('Formato não suportado: ' + formato)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Exporta backup de produtos do banco de dados no formato compatível com o modelo do sistema.'
    )
    parser.add_argument('--format', '-f', choices=['csv', 'json', 'xlsx'], default='csv', help='Formato de saída')
    parser.add_argument('--output', '-o', help='Caminho do arquivo de saída')
    parser.add_argument('--template', action='store_true', help='Gerar somente um template em branco com cabeçalho')
    parser.add_argument('--include-inactive', action='store_true', help='Incluir produtos inativos no backup')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output) if args.output else Path(f'produtos_backup.{args.format}')

    if args.template:
        criar_template(output_path, args.format)
        return

    produtos = carregar_produtos(include_inativos=args.include_inactive)
    if args.format == 'csv':
        export_csv(produtos, output_path)
    elif args.format == 'json':
        export_json(produtos, output_path)
    else:
        export_xlsx(produtos, output_path)


if __name__ == '__main__':
    main()
