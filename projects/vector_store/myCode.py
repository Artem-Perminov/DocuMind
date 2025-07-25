import time
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


relevant_doc = Document(
    page_content="Большая языковая модель это языковая модель, состоящая из нейронной сети со множеством параметров (обычно миллиарды весовых коэффициентов и более), обученной на большом количестве неразмеченного текста с использованием обучения без учителя."
)
irrelevant_doc = Document(
    page_content="Задачи сокращения размерности. Исходная информация представляется в виде признаковых описаний, причём число признаков может быть достаточно большим. Задача состоит в том, чтобы представить эти данные в пространстве меньшей размерности, по возможности, минимизировав потери информации.."
)

# Using free local embeddings - no API key required!
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vectorstore = InMemoryVectorStore.from_documents(
    [relevant_doc, irrelevant_doc],
    embedding=embeddings,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
time.sleep(2)
result = retriever.invoke("Что такое большая языковая модель?")
print(result)
