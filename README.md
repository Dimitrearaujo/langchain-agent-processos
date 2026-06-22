# LangChain Agent — Automação Inteligente de Processos

[![CI](https://github.com/Dimitrearaujo/langchain-agent-processos/actions/workflows/ci.yml/badge.svg)](https://github.com/Dimitrearaujo/langchain-agent-processos/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Um **agente de IA para análise e automação de processos corporativos** usando LangChain + Python. Integra LLMs (Claude/GPT-4o) com ferramentas customizadas para identificar gargalos, sugerir melhorias e gerar documentação automaticamente.

## Quick Start

```bash
git clone https://github.com/Dimitrearaujo/langchain-agent-processos.git
cd langchain-agent-processos
pip install -r requirements.txt
cp .env.example .env  # configure sua API key
python agent.py
```

## O que você vai ter

- Agente conversacional que analisa processos de negócio em linguagem natural
- Tools customizadas: busca em base de conhecimento, geracao de documentacao, analise de SLA
- Memoria persistente de conversas via SQLite
- RAG simples para consultar processos ja documentados
- Output estruturado em JSON e Markdown
- Pronto para integrar com APIs internas via REST

## Arquitetura

### Stack

- **LangChain** — orquestracao do agente e chains
- **OpenAI / Anthropic Claude** — LLM base (configuravel via .env)
- **SQLite** — memoria persistente e base de conhecimento local
- **FastAPI** — endpoint REST opcional para integrar com outros sistemas
- **Python 3.10+** — runtime principal

### Fluxo

```
Usuario descreve o processo
        |
Agente analisa com LLM (LangChain ReAct)
        |
Tools executadas conforme necessario:
  - search_knowledge_base()   <- busca processos similares
  - analyze_bottlenecks()     <- identifica gargalos
  - generate_documentation()  <- gera doc tecnica
  - estimate_automation_roi() <- calcula ROI estimado
        |
Resposta estruturada + sugestoes de automacao
        |
Salva resultado em SQLite + exporta .md
```

## Estrutura

```
langchain-agent-processos/
├── agent.py                  <- Agente principal (ReAct + tools)
├── tools/
│   ├── knowledge_base.py     <- Busca RAG em processos documentados
│   ├── bottleneck_analyzer.py <- Identifica gargalos e ineficiencias
│   ├── doc_generator.py      <- Gera documentacao tecnica automatica
│   └── roi_estimator.py      <- Calcula ROI de automacao
├── memory/
│   ├── conversation.py       <- Historico de conversas (SQLite)
│   └── process_store.py      <- Base de processos analisados
├── api/
│   └── server.py             <- FastAPI endpoint (opcional)
├── data/
│   └── sample_processes/     <- Exemplos de processos para testar
├── .env.example              <- Template de configuracao
├── requirements.txt
└── README.md
```

## Exemplo de Uso

Voce descreve o processo:
> "Nosso processo de onboarding de clientes leva 3 dias e envolve 5 departamentos. O maior gargalo e a aprovacao de credito que leva 24h."

O agente responde:
```
Analise concluida para: Onboarding de Clientes

Gargalos identificados:
  1. Aprovacao de credito manual (24h) — potencial de automacao: ALTO
  2. Notificacoes entre departamentos (manual) — automacao via webhook
  3. Preenchimento de cadastro duplicado — unificar formulario

Sugestao de automacao:
  - Regras de credito automaticas para perfis de baixo risco (70% dos casos)
  - n8n workflow para notificacoes automaticas entre departamentos
  - Formulario unico com pre-preenchimento via API

ROI estimado:
  - Reducao de 24h -> 4h no processo
  - Economia: ~R$12.000/mes em horas operacionais

Documentacao gerada em: output/onboarding_analise_2026-06-22.md
```

## Configuracao

```env
# .env.example
LLM_PROVIDER=anthropic          # anthropic | openai
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
MODEL_NAME=claude-sonnet-4-6    # ou gpt-4o
DB_PATH=./data/memory.db
MAX_ITERATIONS=10
VERBOSE=true
```

## Casos de Uso

- Analise de processos de RH, financeiro, TI e operacoes
- Geracao automatica de documentacao tecnica (BPMN textual)
- Identificacao de oportunidades de automacao com ROI estimado
- Base de conhecimento conversacional para times de processo

## Requisitos

- Python 3.10+
- API key da Anthropic (Claude) ou OpenAI
- 50MB de espaco em disco

## Licenca

MIT — use livremente em producao.

---

**Feito por [Dimitre Araujo](https://github.com/Dimitrearaujo) — CD Tech**
Junho 2026 | v1.0
