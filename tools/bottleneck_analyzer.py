"""Analisa descricao de processo e identifica gargalos."""

import json
import re


BOTTLENECK_PATTERNS = [
    (r"\b(\d+)\s*(dias?|horas?|semanas?)\b", "tempo_elevado"),
    (r"\bmanual\b|\bmanualmente\b", "processo_manual"),
    (r"\b(\d+)\s*departamentos?\b|\b(\d+)\s*areas?\b", "multiplas_areas"),
    (r"\baprovac\w+\b|\bvalidac\w+\b", "etapa_aprovacao"),
    (r"\bemail\b|\bplanilha\b|\bexcel\b", "ferramenta_legada"),
    (r"\brepetitiv\w+\b|\bmanual\w+\b", "tarefa_repetitiva"),
]

AUTOMATION_SUGGESTIONS = {
    "tempo_elevado": "Automatizar etapas sequenciais para execucao em paralelo",
    "processo_manual": "Criar workflow automatizado com n8n ou RPA",
    "multiplas_areas": "Implementar sistema de notificacoes automaticas via webhook",
    "etapa_aprovacao": "Criar regras automaticas de aprovacao para casos padrao",
    "ferramenta_legada": "Migrar para API REST com integracao direta aos sistemas",
    "tarefa_repetitiva": "Automatizar com script Python + agendamento",
}


def analyze_bottlenecks(process_description: str) -> str:
    """Identifica gargalos em um processo descrito em texto livre."""
    found = {}
    text = process_description.lower()

    for pattern, category in BOTTLENECK_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found[category] = AUTOMATION_SUGGESTIONS[category]

    if not found:
        return json.dumps({
            "gargalos": [],
            "sugestoes": ["Processo parece bem estruturado. Analisar metricas de volume para identificar oportunidades."],
            "potencial_automacao": "BAIXO"
        }, ensure_ascii=False, indent=2)

    potential = "ALTO" if len(found) >= 3 else "MEDIO" if len(found) >= 2 else "BAIXO"

    return json.dumps({
        "gargalos": list(found.keys()),
        "sugestoes": list(found.values()),
        "potencial_automacao": potential,
        "num_oportunidades": len(found),
    }, ensure_ascii=False, indent=2)
