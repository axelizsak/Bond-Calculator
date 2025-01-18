from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from typing import Optional, Union, Dict, Any
from .bond_calculator import BondCalculator
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérifier que la clé API est disponible
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("La clé API Anthropic n'est pas définie dans le fichier .env")

class BondCalculatorTool(BaseTool):
    name: str = "bond_calculator"
    description: str = """
    Calcule les métriques importantes d'une obligation comme le prix propre,
    le prix sale, la duration modifiée, la convexité et l'élasticité.
    Input doit être au format: principal,coupon_rate,ytm,maturity_date
    Exemple: "1000,5,6,2025-01-18"
    """
    
    def _run(self, input_str: str) -> Dict[str, float]:
        principal, coupon_rate, ytm, maturity_date = input_str.split(',')
        calculator = BondCalculator(
            principal=float(principal),
            coupon_rate=float(coupon_rate),
            ytm=float(ytm),
            maturity_date=maturity_date
        )
        return calculator.get_all_metrics()

    async def _arun(self, input_str: str) -> Dict[str, float]:
        return self._run(input_str)

# ... (reste du code inchangé jusqu'au template)

template = """Tu es un expert en obligations et finance de marché.
Tu as accès à un calculateur de prix d'obligations sophistiqué.

Pour utiliser le calculateur, tu dois formater les données exactement comme ceci: principal,coupon_rate,ytm,maturity_date
Par exemple: 1000,5,6,2025-01-18

IMPORTANT - Format de réponse requis:
1. Tu dois toujours utiliser ce format:
   Thought: [ta réflexion]
   Action: [bond_calculator OU respond]
   Action Input: [données OU réponse simple]

2. Garde tes réponses concises et évite les répétitions.
3. Pour des calculs:
   Action: bond_calculator
   Action Input: [données au format requis]
4. Pour des explications:
   Action: respond
   Action Input: [une seule réponse claire et concise]

Outils disponibles:
{tools}

Noms des outils: {tool_names}

Historique de la conversation:
{chat_history}

Question humaine: {input}
{agent_scratchpad}
"""

# Création des outils et de l'agent
tools = [
    BondCalculatorTool(),
    Tool(
        name="respond",
        func=lambda x: x,
        description="Utilise cet outil pour donner une réponse directe"
    )
]

llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.5,  # Réduit pour plus de consistance
    max_tokens=1000
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=2  # Réduit pour éviter les boucles
)