import os
from dotenv import load_dotenv

from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler

load_dotenv()


async def main():
    # setup tools
    tools = [
        TavilyToolSpec(api_key=os.environ["TAVILY_API_KEY"]).to_tool_list()[0],
    ]

    # setup llm
    llm = BedrockConverse(
        model=os.environ["MODEL_ID"],
        max_tokens=1024 * 2,
        temperature=0.4,
        profile_name=os.environ.get("AWS_PROFILE_NAME", None),
    )

    # setup memory
    memory = ChatMemoryBuffer.from_defaults()

    # setup tracing
    langfuse_callback_handler = LlamaIndexCallbackHandler(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_HOST"],
    )
    callback_manager = CallbackManager([langfuse_callback_handler])

    # setup agent
    agent = ReActAgent(
        tools=tools,
        llm=llm,
        memory=memory,
        callback_manager=callback_manager,
        verbose=True,
    )

    resp = await agent.achat("NCSoft 의 Lineage M 에 대한 게이머들의 최근 평가는 어때?")
    print(resp)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
