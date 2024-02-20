import requests
from langchain.chat_models import ChatOllama

def setup(ToolManager):
    ToolManager.add(web_search_tool)
    ToolManager.add(science_archive_search_tool)
    ToolManager.add(medical_search_tool)
    ToolManager.add(wikipedia_search_tool)
    ToolManager.add(web_archive_search_tool)
    ToolManager.add(code_search_tool)
    ToolManager.add(math_search_tool)
    ToolManager.add(video_search_tool)
    ToolManager.add(image_search_tool)
    ToolManager.add(product_search_tool)
    ToolManager.add(music_search_tool)
    ToolManager.add(street_map_search_tool)

"""
    Call a SearxNG server with a specified query and additional optional parameters.
    Args:
    - query: The search query string.
    - searxng_url: URL of the SearxNG instance.
    - kwargs: Optional parameters such as format, lang, time_range, safesearch, etc.
    
    Returns:
    - A JSON response with search results.
    
    Common SearxNG Engines and Their Uses:
    'google' - Comprehensive searches, including web, images, news, and videos.
    'bing' - Similar to Google, strong in image and video searches.
    'duckduckgo' - Privacy-focused, no personalized tracking.
    'yahoo' - Web searches, images, and news, with Yahoo's content network.
    'startpage' - Privacy-oriented, uses Google's results.
    'qwant' - Privacy-focused, based in Europe, good for social and news.
    'wikipedia' - Direct searches in Wikipedia.
    'yandex' - Strong in Russian content and regions where Yandex is popular.
    'baidu' - Ideal for content relevant to China.
    'swisscows' - Privacy-focused, family-friendly general web searches.
    'archiveorg' - Searches the Internet Archive for historical web content.
    'github' - Searches repositories and code on GitHub.
    'gitlab' - Similar to GitHub, for GitLab repositories and code.
    'reddit' - Searches within Reddit posts and comments.
    'stackexchange' - Ideal for programming and technical queries.
    'wolframalpha' - Answers from structured data, good for math and science.
    'youtube' - Searches for video content on YouTube.
    'vimeo' - High-quality, artistic video content.
    'dailymotion' - Another source for video content.
    'flickr' - Searches for images and photos on Flickr.
    'unsplash' - High-quality, royalty-free images.
    'twitter' - Searches for tweets and Twitter profiles.
    'ebay' - Product and listing searches on Ebay.
    'amazon' - Product searches on Amazon.
    'genius' - Song lyrics and music-related content.
    'openstreetmap' - Geographical and map-related information.
    'pubmed' - Scientific papers, particularly in biomedicine.
    'arxiv' - Preprints in physics, mathematics, computer science, etc.

    SearxNG Search Parameters (excluding 'engines'):

    'q': The search query string.
    Example: 'q': 'OpenAI'

    'format': Specifies the format of the response.
    Legal values: 'html', 'json', 'csv', 'rss'
    Example: 'format': 'json'

    'lang': Sets the language for the search results.
    Legal values: Language codes like 'en', 'de', 'fr', etc.
    Example: 'lang': 'en'

    'time_range': Filters results based on time.
    Legal values: 'day', 'week', 'month', 'year'
    Example: 'time_range': 'week'

    'safesearch': Enables or disables safe search.
    Legal values: 0 (off), 1 (moderate), 2 (strict)
    Example: 'safesearch': 1

    'categories': Filters results by category.
    Legal values: 'general', 'images', 'news', 'science', etc.
    Example: 'categories': 'general'

    'pageno': Specifies the page number of the results.
    Legal values: Any positive integer
    Example: 'pageno': 1

    'pagesize': Number of results per page.
    Legal values: Typically from 1 to 20 (depends on the instance)
    Example: 'pagesize': 10

    'image_proxy': Proxies images through the instance for privacy.
    Legal values: 'true', 'false'
    Example: 'image_proxy': 'true'

    'autocomplete': Enables or disables autocomplete suggestions.
    Legal values: 'true', 'false'
    Example: 'autocomplete': 'false'

    'origin': Specifies the region or country for localized search results.
    Legal values: Region or country codes like 'us', 'eu', etc.
    Example: 'origin': 'us'

    'enable_http': Allows results from HTTP sources.
    Legal values: 'true', 'false'
    Example: 'enable_http': 'true'

    'no_redirect': Prevents automatic redirection to the result URL.
    Legal values: 'true', 'false'
    Example: 'no_redirect': 'true'

    'no_cache': Disables caching of the search results.
    Legal values: 'true', 'false'
    Example: 'no_cache': 'true'
    

    # Example usage
query = "Who won the Iowa caucus in 2024?"
results = call_searxng_server(
    query, 
    format="json", 
    lang="en", 
    time_range="week", 
    safesearch=1, 
    engines="bing,duckduckgo", 
    categories="general",
    image_proxy=True,
    autocomplete="off",
    origin="us",
    enable_http=True,
    no_redirect=True,
    no_cache=True,
    pageno=1,
    pagesize=10
)
print(results)

    """

llm = ChatOllama(model="llama2", temperature=0)


def science_archive_search_tool(query:str)->str:
    """
    This tool is best for searching research papers.
    """
    print("Searching research papers...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="arxiv",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at understanding research articles in Physics, Mathematics, Computer Science, Quantitative Biology, Quantitative Finance, and Statistics. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def medical_search_tool(query:str)->str:
    """
    This tool is best for searching medical research papers.
    """
    print("Searching medical research papers...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="pubmed",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at understanding research articles in Medicine. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def wikipedia_search_tool(query:str)->str:
    """
    This tool is useful for when you need to answer general questions about 
        people, places, companies, facts, historical events, and concepts.
    """
    print("Searching wikipedia...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="wikipedia",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at answering general questions about 
        people, places, companies, facts, historical events, and concepts. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def web_archive_search_tool(query:str)->str:
    """
    This tool is best for searching historical web content.
    """
    print("Searching web archive...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="archiveorg",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at  researching historical web content. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def code_search_tool(query:str)->str:
    """
    This tool is best for finding answers to software and hardware questions.
    """
    print("Searching github...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="github,gitlab,stackexchange",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at answering questions about software and hardware. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def video_search_tool(query:str)->str:
    """
    This tool is best for searching video content.
    """
    print("Searching video content...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="youtube,vimeo,dailymotion",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at researching video content. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def image_search_tool(query:str)->str:
    """
    This tool is best for answering questions about images.
    """
    print("Searching image content...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="flickr,unsplash",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at understanding images and photos. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def product_search_tool(query:str)->str:
    """
    This tool is best for doing product searches on Amazon and Ebay.
    """
    print("Searching Amazon and Ebay...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="amazon,ebay",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at performing product searches on Amazon and Ebay. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def music_search_tool(query:str)->str:
    """
    This tool is best for searching music lyrics and music related content.
    """
    print("Searching music lyrics...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="genius",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at understanding music lyrics and music related content. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def street_map_search_tool(query:str)->str:
    """
    This tool is best for understanding geographical and map-related information.
    """
    print("Searching research papers...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="openstreetmap",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at understanding geographical and map-related information. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def math_search_tool(query:str)->str:
    """
This tool is best for answering queries about mathematics, science, engineering, and society.    """
    print("Searching Wolfram Alpha...")
    se_resp = web_search(
        query, 
        format="json", 
        engines="wolframalpha",
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at answering queries about mathematics, science, engineering, and society. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def web_search_tool(query:str)->str:
    """
    This tool is best for searching the Internet.
    """
    print("Searching the web...")
    se_resp = web_search(
        query, 
        format="json", 
    )
    se_url = '\n'.join(result['url'] for result in se_resp['results'][:3])
    se_resp = '\n'.join(result['content'] for result in se_resp['results'][:3])
    reassess_instructionsextract_instructions = f"""
    System: 
    <System>
    You are an expert at reading responses from search engines. 
    </System>
    
    Instructions: 
    <Instructions>
    You are to extract from the Background Information find the best, most current and concise response to the Search Request and rewrite the response to be concise.
    </Instructions>

    Background Information: 
    <Background Information>
    {se_resp}
    </Background Information>

    Search Request: 
    <Search Request>
    {query}
    </Search Request>
    """
    search_result = llm.invoke(reassess_instructionsextract_instructions) 
    output = f"""{search_result.content}

    Citations: {se_url}
    """
    return output

def web_search(query, searxng_url="http://localhost:9080", **kwargs):
    """
    Call a SearxNG server with a specified query and additional optional parameters.
    Args:
    - query: The search query string.
    - searxng_url: URL of the SearxNG instance.
    - kwargs: Optional parameters such as format, lang, time_range, safesearch, etc.
    
    Returns:
    - A JSON response with search results.
    """
    headers = {'Accept': 'application/json'}  # Request JSON response
    params = {"q": query}
    params.update(kwargs)  # Update with any additional parameters provided

    response = requests.get(f"{searxng_url}/search", params=params, headers=headers)

    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)
        return None

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON. Response:", response.text)
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def print_results(results):
    if not results or 'results' not in results:
        print("No results found.")
        return

    for i, result in enumerate(results['results'], start=1):
        title = result.get('title', 'No Title')
        url = result.get('url', 'No URL')
        content = result.get('content', 'No Content')
        print(f"Result {i}:")
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Content: {content}\n")

def main():
    # Example usage
    # query = "Who won the Iowa caucus in 2024?"
    # results = web_search(
    #     query, 
    #     format="json", 
    #     lang="en", 
    #     time_range="week", 
    #     safesearch=1, 
    #     engines="bing", 
    #     categories="general",
    #     image_proxy=True,
    #     autocomplete="off",
    #     origin="us",
    #     enable_http=True,
    #     no_redirect=True,
    #     no_cache=True,
    #     pageno=1,
    #     pagesize=10
    # )

    # wikipedia

    # print(results)
    print(wikipedia_search_tool("""January 6th"""))

if __name__ == "__main__":
    main()


