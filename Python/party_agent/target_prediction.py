import asyncio
import logging
import os
import random
from datetime import datetime

import azure.identity
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient, OpenAIChatCompletionClient
from dotenv import load_dotenv
from rich.logging import RichHandler
import requests

# Setup logging with rich
logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("weekend_planner")


# Setup the client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")


if API_HOST == "github":
    client = OpenAIChatCompletionClient(model=os.getenv("GITHUB_MODEL", "gpt-4o"), api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com", parallel_tool_calls=False)
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    client = AzureOpenAIChatCompletionClient(model=os.environ["AZURE_OPENAI_CHAT_MODEL"], api_version=os.environ["AZURE_OPENAI_VERSION"], azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"], azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"], azure_ad_token_provider=token_provider, parallel_tool_calls=False)


# Define the tools

def get_history_party_signature() -> list:
    """returns a list of party collection history. with information about the
    status of the signature collection.

    Returns:
        dict: list of party collection history.
    """
    logger.info("Fetching data from API...")
    response = requests.get("https://partido-missao-api.azurewebsites.net/api/missao_api")

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error("Error fetching data from API: %s", response.status_code)
        return None

agent = AssistantAgent(
    "target_predictor",
    model_client=client,
    tools=[get_history_party_signature],
    system_message="You help me to forecast the party signature collection target. The party needs to collect 547,503 signatures.",
)


async def main() -> None:
    team = RoundRobinGroupChat([agent], termination_condition=TextMessageTermination(agent.name))

    async for task_result in team.run_stream(task="Please then the party will achieve the target of 547,503 signatures?"):
        logger.debug("%s: %s", type(task_result).__name__, task_result)
    print(task_result.messages[-1].content)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    asyncio.run(main())
