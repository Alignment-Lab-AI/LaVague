from llama_index.llms.litellm import LiteLLM
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import PromptTemplate
from lavague.core import BaseHtmlRetriever, OpsmSplitRetriever
from lavague.core import DEFAULT_PROMPT_TEMPLATE
from lavague.core import BaseExtractor, PythonFromMarkdownExtractor
from lavague.core import ActionContext
from lavague.core.action_context import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE

class LiteLLMContext:
    def from_defaults(
        llm: BaseLLM = LiteLLM(model="gpt-3.5-turbo", max_tokens=DEFAULT_MAX_TOKENS, temperature=DEFAULT_TEMPERATURE),
        embedding: BaseEmbedding = OpenAIEmbedding(model="text-embedding-3-large"),
        retriever: BaseHtmlRetriever = OpsmSplitRetriever(),
        prompt_template: PromptTemplate = DEFAULT_PROMPT_TEMPLATE,
        extractor: BaseExtractor = PythonFromMarkdownExtractor(),
    ) -> ActionContext:
        return ActionContext(llm, embedding, retriever, prompt_template, extractor)