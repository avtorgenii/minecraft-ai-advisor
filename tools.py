from typing import List, Dict
from langchain_core.tools import tool


from context_preparator import ContextPreparator




cp = ContextPreparator()

@tool(parse_docstring=True)
def unified_search_tool(queries: List[str], tools_to_call: List[str]) -> Dict[str, List[str]]:
    """
    A unified tool that performs web searches for multiple queries using specified functions.

    Args:
        queries (List[str]): A list of search queries. Add to the end of query "in minecraft" words.
        tools_to_call (List[str]): A list of tool names to call. Supported tools: ["info", "images", "videos"]. Use "info" tool when user asks you about information on something.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are tool names and values are lists of results
        corresponding to the queries for each tool.
    """
    results = {"info": [], "images": [], "videos": []}

    for query in queries:
        if "info" in tools_to_call:
            results["info"] = cp.get_context(query)
        if "images" in tools_to_call:
            results["images"] = cp.search_images(query)
        if "videos" in tools_to_call:
            results["videos"] = cp.search_videos(query)

    # Remove keys with no results
    results = {k: v for k, v in results.items() if v}
    return results



def info_web_search(query: str) -> str:
    """
    Use this tool when you need to find some information on a certain topic.

    Args:
        query (str): The web search query to look up.

    Returns:
        str: Contextual information related to the query.
    """
    return cp.get_context(query)


def images_web_search(query: str) -> str:
    """
    Use this tool when you need to find some images.

    Args:
        query (str): The web search query for finding images.

    Returns:
        str: Links or data about the images found for the query.
    """
    return cp.search_images(query)


def videos_web_search(query: str) -> str:
    """
    Use this tool when you need to find some videos.

    Args:
        query (str): The web search query for finding videos.

    Returns:
        str: Links or data about the videos found for the query.
    """
    return cp.search_videos(query)


if __name__ == '__main__':
    # llm = ChatOllama(
    #     model="cow/gemma2_tools:9b",
    #     temperature=0.2,
    #     num_predict=256
    # )
    #
    #
    # print('Model loaded')
    #
    #
    #
    #
    # # history = [
    # #     HumanMessage("how to craft stone axe"),
    # #     AIMessage("""{"stick": 2, "cobblestone": 3}""")
    # # ]
    # #
    # # stream_with_custom_prompt(llm, query="how does axe look like", history=history, custom_system_prompt=DETERMINE_IF_QUERY_IS_ABOUT_LOOKS_PROMPT)
    #
    # history = [
    #     HumanMessage("what is nether portal"),
    #     AIMessage("""Nether portal is a building that is used to enter Nether dimension""")
    # ]
    #
    # res = invoke_with_custom_prompt(llm, query="how to build it",
    #                           custom_system_prompt=CONSTRUCT_WEB_SEARCH_QUERY_PROMPT)
    #
    # print(res)
    pass