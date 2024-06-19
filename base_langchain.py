import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.email import UnstructuredEmailLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate


def get_insights(question):
# ---------------------------------------------------------------------------
#def get_insights(question, directory):

    #eml_files = [f for f in os.listdir(directory) if f.endswith(".eml")]
    #documents = []

    #for eml_file in eml_files:
    #    loader = UnstructuredEmailLoader(os.path.join(directory, eml_file))
    #    documents.extend(loader.load())
# ---------------------------------------------------------------------------
    #eml_files = [f for f in os.listdir(directory) if f.endswith(".eml")]
    #documents = []
    #for eml_file in eml_files:
    #    loader = UnstructuredEmailLoader(
    #       os.path.join(directory, eml_file), 
    #       mode="elements", 
    #       process_attachments=True,
    #   )
    #    documents.extend(loader.load())
# ---------------------------------------------------------------------------   
    loader = DirectoryLoader(
        "./downloaded_emails/valderlan.nobre/",
        glob="**/*.eml",
        show_progress=True,
        use_multithreading=True,
        loader_cls=UnstructuredEmailLoader,
    )
    documents = loader.load()
# ---------------------------------------------------------------------------
    print(len(documents))

    text_split = RecursiveCharacterTextSplitter()

    doc = text_split.split_documents(documents)

    # if documents:
    #   print("Estrutura do documento:", type(documents[0]), documents[0])

    embeddings = OllamaEmbeddings(model="llama3")

    chroma_db = Chroma.from_documents(doc, embeddings, persist_directory="./chroma_db")
    chroma_db.persist()

    llm = Ollama(model="llama3")

    prompt = """
    Use as seguintes partes do contexto para responder à pergunta no final.
    Se você não souber a resposta apenas com base no contexto, diga que não sabe a resposta. 

    {context}

    Questão: {question}
    """

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=chroma_db.as_retriever(),
        chain_type_kwargs={"prompt": prompt_template},
    )
    result = qa_chain({"query": question})
    return result
