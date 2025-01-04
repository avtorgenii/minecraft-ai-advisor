from typing import List, Dict
from langchain_core.tools import tool


from context_preparator import ContextPreparator




cp = ContextPreparator()

@tool(parse_docstring=True)
def unified_search_tool(queries: List[str], tools_to_call: List[str]) -> Dict[str, List[str]]:
    """A unified tool that performs web searches for multiple queries using specified functions.

    This tool can search for text-based info, images, and videos. Use it when you don't have enough
    information to answer user's query.

    Tool Usage:
        - Add "info" to tools_to_call for text-based information
        - Add "images" to tools_to_call for finding images or appearance
        - Add "videos" to tools_to_call for finding videos, tutorials, or guides

    Search Query Construction Rules:
        1. ALWAYS include specific keywords about what you're searching for
           (e.g., "Blood Altar tier 4", not just "altar")
        2. ALWAYS add relevant modpack names
           (e.g., "BuildCraft", "Blood Magic", "ThaumCraft")
        3. ALWAYS include purpose or context
           (e.g., "how to build", "appearance", "requirements")
        4. ALWAYS append "in minecraft" to EVERY query
        5. ALWAYS use multiple queries for different aspects

    Example Queries:
        - ["buildcraft quarry appearance in minecraft",
           "buildcraft quarry setup in minecraft"]
        - ["blood altar tier 4 requirements in minecraft",
           "blood altar tier 4 construction steps in minecraft"]
        - ["thaumcraft infusion altar layout in minecraft",
           "thaumcraft infusion altar tutorial in minecraft"]

    Args:
        queries: A list of search queries. Each query must end with "in minecraft".
        tools_to_call: A list of tool names to call. Supported tools: ["info", "images", "videos"].

    Returns:
        A dictionary where keys are tool names and values are lists of results
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