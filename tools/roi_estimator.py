"""Estima ROI de automacao de processo."""

import json


def estimate_automation_roi(input_json: str) -> str:
    """Calcula ROI estimado de automatizar um processo."""
    try:
        data = json.loads(input_json)
    except json.JSONDecodeError:
        return "Erro: fornecer JSON com horas_por_dia, custo_hora e reducao_percentual."

    horas_dia = float(data.get("horas_por_dia", 2))
    custo_hora = float(data.get("custo_hora", 50))
    reducao = float(data.get("reducao_percentual", 70)) / 100
    custo_impl = float(data.get("custo_implementacao", 5000))

    economia_dia = horas_dia * custo_hora * reducao
    economia_mes = economia_dia * 22
    economia_ano = economia_mes * 12
    payback_meses = custo_impl / economia_mes if economia_mes > 0 else 999

    result = {
        "economia_por_dia": f"R$ {economia_dia:.2f}",
        "economia_por_mes": f"R$ {economia_mes:.2f}",
        "economia_por_ano": f"R$ {economia_ano:.2f}",
        "payback_estimado": f"{payback_meses:.1f} meses",
        "roi_12_meses": f"{((economia_ano - custo_impl) / custo_impl * 100):.0f}%",
        "recomendacao": "IMPLEMENTAR" if payback_meses < 6 else "AVALIAR" if payback_meses < 12 else "REVISAR ESCOPO",
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
