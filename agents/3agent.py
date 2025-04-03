from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

def load_retriever(vector_path):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        vector_path, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever()

def create_qa_tool(name, vector_path, description):
    """Crée un outil basé sur RetrievalQA pour un vector store spécifique."""
    retriever = load_retriever(vector_path)
    # Chaîne simple pour répondre aux questions basées sur les documents récupérés
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff", # Méthode simple pour combiner les documents
        return_source_documents=False
    )
    return Tool(
        name=name,
        func=qa_chain.invoke, # La fonction de l'outil appelle la chaîne QA
        description=description
    )

# --- 2. Création des Outils Spécifiques ---

try:
    tool_programmes = create_qa_tool(
        name="FormationProgrammeTool",
        vector_path="../vectors/programmes_faiss",
        description="Utile pour répondre aux questions sur les programmes de formation disponibles."
    )

    tool_pratiques = create_qa_tool(
        name="MeilleuresPratiquesTool",
        vector_path="../vectors/pratiques_faiss",
        description="Utile pour répondre aux questions sur les meilleures pratiques, conseils et méthodes éprouvées en entreprise."
    )

    tool_etudes = create_qa_tool(
        name="EtudesDeCasTool",
        vector_path="../vectors/etudes_faiss",
        description="Utile pour trouver des exemples concrets, des illustrations ou des retours d'expérience à partir d'études de cas."
    )
except FileNotFoundError as e:
    print(f"Erreur: {e}")
    print("Veuillez vérifier les chemins des fichiers FAISS ('vectors/...') et que les index existent.")
    exit()

# --- 3. Création des Trois Agents Spécialisés ---
# Chaque agent n'a accès qu'à son propre outil.
# On utilise ici un agent React simple qui est bon pour utiliser des outils.

react_prompt = hub.pull("hwchase17/react")

agent_programmes = AgentExecutor(
    agent=create_react_agent(llm, [tool_programmes], react_prompt),
    tools=[tool_programmes],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

agent_pratiques = AgentExecutor(
    agent=create_react_agent(llm, [tool_pratiques], react_prompt),
    tools=[tool_pratiques],
    verbose=True,
    handle_parsing_errors=True,
     max_iterations=3
)

agent_etudes = AgentExecutor(
    agent=create_react_agent(llm, [tool_etudes], react_prompt),
    tools=[tool_etudes],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

# --- 4. Fonction d'Orchestration et de Fusion ---

fusion_prompt_template = """
Vous êtes un assistant expert en synthèse d'informations.
L'utilisateur a posé la question suivante : "{question}"

Vous avez reçu des informations potentiellement pertinentes de trois sources spécialisées :

1. Informations sur les Programmes de Formation :
{reponse_programmes}

2. Informations sur les Meilleures Pratiques :
{reponse_pratiques}

3. Informations provenant d'Études de Cas :
{reponse_etudes}

Votre tâche est de synthétiser ces informations pour fournir une réponse globale, cohérente et utile à la question initiale de l'utilisateur. Ignorez les informations non pertinentes provenant des sources. Si une source ne fournit pas d'information utile pour répondre à la question, ne l'inventez pas. Basez votre réponse uniquement sur les éléments fournis.

Réponse Synthétisée :
"""

fusion_prompt = PromptTemplate(
    input_variables=["question", "reponse_programmes", "reponse_pratiques", "reponse_etudes"],
    template=fusion_prompt_template,
)

# LLM pour la fusion
fusion_llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

def orchestrate_and_fuse(question: str) -> str:
    print(f"\n--- Orchestration pour la question : '{question}' ---")

    # Appeler chaque agent spécialisé
    try:
        print("\n[Orchestrateur] Interrogation de l'agent Programmes...")
        response_prog_agent = agent_programmes.invoke({"input": question})
        reponse_programmes = response_prog_agent['output']
        print(f"[Agent Programmes] Réponse reçue.")
    except Exception as e:
        print(f"[Agent Programmes] Erreur : {e}")
        reponse_programmes = "Erreur lors de la récupération des informations sur les programmes."

    try:
        print("\n[Orchestrateur] Interrogation de l'agent Meilleures Pratiques...")
        response_prat_agent = agent_pratiques.invoke({"input": question})
        reponse_pratiques = response_prat_agent['output']
        print(f"[Agent Pratiques] Réponse reçue.")
    except Exception as e:
        print(f"[Agent Pratiques] Erreur : {e}")
        reponse_pratiques = "Erreur lors de la récupération des informations sur les meilleures pratiques."

    try:
        print("\n[Orchestrateur] Interrogation de l'agent Études de Cas...")
        response_etu_agent = agent_etudes.invoke({"input": question})
        reponse_etudes = response_etu_agent['output']
        print(f"[Agent Etudes] Réponse reçue.")
    except Exception as e:
        print(f"[Agent Etudes] Erreur : {e}")
        reponse_etudes = "Erreur lors de la récupération des informations des études de cas."

    # Fusionner les réponses
    print("\n[Orchestrateur] Fusion des réponses...")
    formatted_prompt = fusion_prompt.format(
        question=question,
        reponse_programmes=reponse_programmes,
        reponse_pratiques=reponse_pratiques,
        reponse_etudes=reponse_etudes
    )

    final_response = fusion_llm.invoke(formatted_prompt)
    print("[Orchestrateur] Fusion terminée.")

    return final_response.content


if __name__ == "__main__":
    question_test = "Quelles formations et bonnes pratiques sont recommandées pour améliorer le leadership, avec des exemples concrets ?"
    print(f"🧑‍💻 Question : {question_test}")
    reponse_finale = orchestrate_and_fuse(question_test)
    print("\n==================== RÉPONSE FINALE ====================")
    print(f"🤖 Réponse : {reponse_finale}")
    print("========================================================")

    question_test_2 = "Donne-moi juste la liste des programmes de formation sur la gestion de projet."
    print(f"\n🧑‍💻 Question : {question_test_2}")
    reponse_finale_2 = orchestrate_and_fuse(question_test_2)
    print("\n==================== RÉPONSE FINALE 2 ====================")
    print(f"🤖 Réponse : {reponse_finale_2}")
    print("==========================================================")