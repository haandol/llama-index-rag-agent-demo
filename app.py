import os
import sys
import logging
from dotenv import load_dotenv

from llama_index.core.agent import ReActAgent
from llama_index.core.callbacks import CallbackManager
from llama_index.core.tools.types import BaseTool
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.llms.bedrock_converse import BedrockConverse
from langfuse.llama_index import LlamaIndexCallbackHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

load_dotenv()


async def main():
    # setup tools
    tools: list[BaseTool] = [
        TavilyToolSpec(api_key=os.environ["TAVILY_API_KEY"]).to_tool_list()[0],
    ]

    # setup llm
    llm = BedrockConverse(
        model=os.environ["MODEL_ID"],
        max_tokens=1024 * 2,
        temperature=0.4,
        profile_name=os.environ.get("AWS_PROFILE_NAME", None),
    )

    # setup tracing
    langfuse_callback_handler = LlamaIndexCallbackHandler(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_HOST"],
    )
    callback_manager = CallbackManager([langfuse_callback_handler])

    # setup agent
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        callback_manager=callback_manager,
        verbose=True,
    )

    resp = await agent.achat(
        "NCSoft 의 최신작과 월드 오브 워크래프트의 차이가 뭐야?"
        "캐주얼한 게이머에게 어떤 게임이 더 좋을까?"
    )
    logger.info(f"=== Response ===\n{resp}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
