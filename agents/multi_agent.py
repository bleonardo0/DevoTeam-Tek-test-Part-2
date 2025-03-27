from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory

load_dotenv()

def load_retriever(vector_path):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        vector_path, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever()

def create_tool(name, vector_path, description):
    retriever = load_retriever(vector_path)
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o", temperature=0.3),
        retriever=retriever,
        return_source_documents=False
    )

    return Tool(
        name=name,
        func=qa_chain.invoke,
        description=description
    )

tools = [
    create_tool(
        name="AgentProgrammeFormation",
        vector_path="vectors/programmes_faiss",
        description="Répond aux questions sur les programmes de formation disponibles."
    ),
    create_tool(
        name="AgentMeilleuresPratiques",
        vector_path="vectors/pratiques_faiss",
        description="Répond aux questions sur les meilleures pratiques en entreprise."
    ),
    create_tool(
        name="AgentEtudesDeCas",
        vector_path="vectors/etudes_faiss",
        description="Répond aux questions en fournissant des exemples concrets à partir d'études de cas."
    )
]

memory = ConversationBufferMemory(memory_key="chat_history")

multi_agent = initialize_agent(
    tools=tools,
    agent="conversational-react-description",
    llm=ChatOpenAI(model="gpt-4o", temperature=0.3),
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)
def demander_agent(question):
    reponse = multi_agent.invoke({"input": question})
    return reponse['output']

if __name__ == "__main__":
    question_test = "Quels programmes de formation sont recommandés pour améliorer le leadership ?"
    print("🧑‍💻 Question :", question_test)
    reponse_test = demander_agent(question_test)
    print("🤖 Réponse :", reponse_test)
