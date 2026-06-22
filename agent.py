"""
LangChain Agent — Automacao Inteligente de Processos
Agente ReAct com tools customizadas para analise de processos corporativos.
"""

import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

from tools.knowledge_base import search_knowledge_base
from tools.bottleneck_analyzer import analyze_bottlenecks
from tools.doc_generator import generate_documentation
from tools.roi_estimator import estimate_automation_roi
from memory.conversation import ConversationStore

load_dotenv()

SYSTEM_PROMPT = """Voce e um especialista em analise e automacao de processos corporativos.
Seu papel e entender o processo descrito pelo usuario, identificar gargalos,
sugerir automacoes e gerar documentacao tecnica.

Voce tem acesso as seguintes ferramentas:
{tools}

Use o formato:
Pensamento: o que preciso fazer
Acao: nome_da_ferramenta
Entrada da Acao: input para a ferramenta
Observacao: resultado da ferramenta
... (repita conforme necessario)
Pensamento: Tenho a resposta final
Resposta Final: resposta completa para o usuario

Nomes das ferramentas disponiveis: {tool_names}

Historico da conversa:
{chat_history}

Pergunta do usuario: {input}
{agent_scratchpad}"""


def get_llm():
    provider = os.getenv("LLM_PROVIDER", "anthropic")
    if provider == "anthropic":
        return ChatAnthropic(
            model=os.getenv("MODEL_NAME", "claude-sonnet-4-6"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=4096,
        )
    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def build_tools():
    return [
        Tool(
            name="search_knowledge_base",
            func=search_knowledge_base,
            description="Busca processos similares ja documentados na base de conhecimento. "
                        "Input: descricao do processo em texto livre.",
        ),
        Tool(
            name="analyze_bottlenecks",
            func=analyze_bottlenecks,
            description="Analisa um processo e identifica os principais gargalos e ineficiencias. "
                        "Input: descricao detalhada do processo.",
        ),
        Tool(
            name="generate_documentation",
            func=generate_documentation,
            description="Gera documentacao tecnica estruturada de um processo em Markdown. "
                        "Input: JSON com campos 'processo', 'gargalos' e 'sugestoes'.",
        ),
        Tool(
            name="estimate_automation_roi",
            func=estimate_automation_roi,
            description="Estima o ROI de automatizar um processo. "
                        "Input: JSON com 'horas_por_dia', 'custo_hora' e 'reducao_percentual'.",
        ),
    ]


def run_agent():
    llm = get_llm()
    tools = build_tools()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)
    store = ConversationStore()

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)
    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=os.getenv("VERBOSE", "true").lower() == "true",
        max_iterations=int(os.getenv("MAX_ITERATIONS", 10)),
        handle_parsing_errors=True,
    )

    print("\n=== LangChain Agent — Analise de Processos ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Voce: ").strip()
        if user_input.lower() in ("sair", "exit", "quit"):
            print("Encerrando. Ate logo!")
            break
        if not user_input:
            continue

        result = executor.invoke({"input": user_input})
        output = result.get("output", "")
        store.save(user_input, output)
        print(f"\nAgente: {output}\n")


if __name__ == "__main__":
    run_agent()
