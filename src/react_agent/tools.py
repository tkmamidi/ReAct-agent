"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated

from react_agent.configuration import Configuration
from neo4j import AsyncGraphDatabase


async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_runnable_config(config)
    wrapped = TavilySearchResults(max_results=configuration.max_search_results)
    result = await wrapped.ainvoke({"query": query})
    return cast(list[dict[str, Any]], result)


async def query_neo4j(
    query: str,
) -> Optional[list[dict[str, Any]]]:
    """Query the Neo4j database.
    This function executes a Cypher query against a Neo4j database and returns the results. It's particularly useful
    for answering questions about proteins, drugs, pathways, phenotypes, diseases and their relationships. Use proteins
    as nodes to query about genes.
    """
    uri = "bolt://tarun.servebeer.com/neo4j-api"  # Update with your Neo4j instance URI
    user = "neo4j"  # Update with your Neo4j username
    password = "password"  # Update with your Neo4j password
    driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
    records, _, _ = await driver.execute_query(
        query,
        routing_="r",  # short for neo4j.RoutingControl.READ
        database_="neo4j",
    )

    return cast(list[dict[str, Any]], records)


TOOLS: List[Callable[..., Any]] = [search, query_neo4j]
