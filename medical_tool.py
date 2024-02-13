from langchain.chat_models import ChatOllama
from langchain.docstore.document import Document
from pymed import PubMed

def setup(ToolManager):
    ToolManager.add(medical_tool)

pubmed = PubMed(tool="Jim.Babcock", email="test@test.com")

def medical_tool(query:str)->str:
    """
    This tool reads medical white papers and answers questions about them in terms that average patients can understand.
    """
    prompt_text = f"""
Your task is to convert the follwing question into 3 keywords that can be used to find relevant medical research papers on PubMed.
Here is an examples:
question: "What are the latest treatments for major depressive disorder?"
keywords:
Antidepressive Agents
Depressive Disorder, Major
Treatment-Resistant depression
---
Output format:
put each word on a separate line
---
question: { query }
keywords:
""" 
    llm=ChatOllama(model="mistral", temperature=0)
    answer =  llm.invoke(prompt_text)
    cleaned_queries = answer.content.strip().split('\n')
    def documentize(article):
        return Document(page_content=article.abstract, metadata={'title': article.title, 'keywords': article.keywords})
    
    articles = []
    try:
        for query in cleaned_queries:
            response = pubmed.query(query, max_results=1)
            documents = [documentize(article) for article in response]
            articles.extend(documents)
    except Exception as e:
        print(e)
        print(f"Couldn't fetch articles")

    prompt = "Answer the question truthfully based on the given documents.\n"
    prompt += "If the documents don't contain an answer, use your existing knowledge base.\n\n"
    prompt += f"q: {query}\n"
    prompt += "Articles:\n"

    for article in articles:
        prompt += f"{article.page_content}\n"
        prompt += f"keywords: {article.metadata['keywords']}\n"
        prompt += f"title: {article.metadata['title']}\n\n"

    answer =  llm.invoke(prompt)


    return answer.content

