"""Gera documentacao tecnica de processo em Markdown."""

import json
import os
from datetime import date


OUTPUT_DIR = "./output"


def generate_documentation(input_json: str) -> str:
    """Gera arquivo .md com documentacao estruturada do processo."""
    try:
        data = json.loads(input_json)
    except json.JSONDecodeError:
        data = {"processo": input_json, "gargalos": [], "sugestoes": []}

    processo = data.get("processo", "Processo sem nome")
    gargalos = data.get("gargalos", [])
    sugestoes = data.get("sugestoes", [])
    hoje = date.today().isoformat()

    doc = f"""# Documentacao de Processo — {processo}
**Data:** {hoje}
**Status:** Em analise

## Descricao
{processo}

## Gargalos Identificados
{chr(10).join(f'- {g}' for g in gargalos) if gargalos else '- Nenhum gargalo critico identificado'}

## Sugestoes de Automacao
{chr(10).join(f'- {s}' for s in sugestoes) if sugestoes else '- Avaliar metricas de volume antes de automatizar'}

## Proximos Passos
1. Validar analise com responsavel pelo processo
2. Priorizar automacoes por ROI
3. Implementar em sprints de 2 semanas
4. Medir reducao de tempo apos 30 dias

---
*Gerado automaticamente pelo LangChain Process Agent*
"""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/{processo[:30].replace(' ', '_').lower()}_{hoje}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc)

    return f"Documentacao gerada com sucesso em: {filename}\n\nPrevia:\n{doc[:400]}..."
