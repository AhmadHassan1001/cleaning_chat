import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from django.conf import settings

class SchedulerAgent:
    def __init__(self,next_availability) -> None:
        print("directoryyyy:", settings.BASE_DIR)
        directory = str(settings.BASE_DIR)+"\\cleaning_agent\\docs\\Cleaning pricing.pdf"
        loader = PyPDFLoader(directory)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore=None
        try:
            vectorstore=Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY))
            print("loaded chroma")
        except Exception as e:
            print("chroma save",e)
            vectorstore = Chroma.from_documents(persist_directory="./chroma_db",documents=splits, embedding=OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY))

        retriever = vectorstore.as_retriever()
        llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,model_name="gpt-3.5-turbo", temperature=0)




        template = """You are a bot for booking cleaning services. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for your message!" at the end of the answer. 
        You should provide service availability time information in the answer also you should provide the price of the service.
        {context}"""+f"""
        Service next availability: {next_availability}"""+"""
        Question: {question}
        Helpful Answer:"""
        
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=retriever,
            # return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    def answer(self,query):

        return self.qa_chain({"query": query})["result"]

if __name__ == "__main__":
    print(SchedulerAgent("2022-01-05 06:00").answer("I want to book general cleaning"))
