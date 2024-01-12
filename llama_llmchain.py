from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

MODEL_PATH = ""

# 1. Create a function to load Llama Model
# 2. Create a function to load prompt

def create_prompt() -> PromptTemplate:
    """Creates prompt template"""
    
    # Prompt copied from langchain docs
    _DEFAULT_TEMPLATE: str = """
    Assistant is a large language model trained by OpenAI.
    Assistant is designed to be able to assist with a wide range of ta
    Assistant is constantly learning an improving, and its capabiliti
    Overall, Assistant is a powerful too that can help with a wide 
    
    
    Human: {question}
    Assistant:"""
    
    prompt: PromptTemplate = PromptTemplate(
        input_variables = ["question"],
        template = _DEFAULT_TEMPLATE
    )
    
    return prompt
# {history}

def load_model() -> LlamaCpp:
    """Loads Llama model"""
    callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])
    n_gpu_layer = 40
    n_batch = 512
    Llama_model: LlamaCpp = LlamaCpp(
        model_path = MODEL_PATH,
        temperature = 0.5,
        n_gpu_layer = n_gpu_layer,
        n_batch = n_batch,
        max_tokens = 2000,
        top_p = 1,
        callback_manager = callback_manager,
        verbose = True
    )
    
    prompt: PromptTemplate = create_prompt()
    
    llm_chain = LLMChain(
        llm = Llama_model,
        prompt = prompt
    )
    
    return Llama_model

llm_chain = load_model()

prompt: str = """What is the largest country on Earth?"""

response: str = llm_chain.run(prompt)

print(response)