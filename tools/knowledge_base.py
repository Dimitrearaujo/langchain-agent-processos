"""Busca RAG em processos documentados (SQLite + similaridade de texto)."""

import sqlite3
import os
import json

DB_PATH = os.getenv("DB_PATH", "./data/memory.db")


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT,
            gargalos TEXT,
            solucao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def search_knowledge_base(query: str) -> str:
    """Busca processos similares na base de conhecimento local."""
    conn = _init_db()
    keywords = [w.lower() for w in query.split() if len(w) > 3]
    results = []

    for kw in keywords[:3]:
        rows = conn.execute(
            "SELECT nome, descricao, solucao FROM processos WHERE lower(descricao) LIKE ?",
            (f"%{kw}%",)
        ).fetchall()
        results.extend(rows)

    conn.close()

    if not results:
        return (
            "Nenhum processo similar encontrado na base de conhecimento. "
            "Este sera o primeiro processo deste tipo a ser analisado."
        )

    seen = set()
    unique = []
    for r in results:
        if r[0] not in seen:
            seen.add(r[0])
            unique.append(r)

    output = f"Encontrei {len(unique)} processo(s) similar(es):\n\n"
    for nome, desc, solucao in unique[:3]:
        output += f"**{nome}**\n{desc[:200]}...\nSolucao aplicada: {solucao[:150]}\n\n"
    return output


def save_process(nome: str, descricao: str, gargalos: str, solucao: str):
    conn = _init_db()
    conn.execute(
        "INSERT INTO processos (nome, descricao, gargalos, solucao) VALUES (?, ?, ?, ?)",
        (nome, descricao, gargalos, solucao)
    )
    conn.commit()
    conn.close()
