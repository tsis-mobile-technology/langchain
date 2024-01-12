# pip install langchain_community langchain llama-cpp-python
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp

# template = """Question: {question}
# Answer: Let's work this out in a step by step way to be sure we have the right answer."""
# prompt = PromptTemplate(template=template, input_variables=["question"])

# template = """A chat between a curious human ("USER") and an artificial intelligence assistant ("ASSISTANT"). The assistant gives helpful, detailed, and polite answers to the human's questions.

# USER: Hello, ASSISTANT.
# ASSISTANT: Hello. How may I help you today?
# USER: Please tell me the largest city in Europe.
# ASSISTANT: Sure. The largest city in Europe is Moscow, the capital of Russia.
# USER: {question}
# """

template = """[INST] <<SYS>>
Name the planets in the solar system? 
<</SYS>>
[/INST] {question}
"""

template = """
A chat between a curious human ("[[USER_NAME]]") and an artificial intelligence assistant ("[[AI_NAME]]"). The assistant gives helpful, detailed, and polite answers to the human's questions.

[[USER_NAME]]: Hello, [[AI_NAME]].
[[AI_NAME]]: Hello. How may I help you today?
[[USER_NAME]]: Please tell me the largest city in Europe.
[[AI_NAME]]: Sure. The largest city in Europe is Moscow, the capital of Russia.
[[USER_NAME]]:{question}
"""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = 40
# Change this value based on your model and your GPU VRAM pool.
n_batch = 512  
# Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
# Make sure the model path is correct for your system!
llm = LlamaCpp(
	model_path="D:\\Programming\\llama.cpp\\models\\16K-Vicuna-13B\\ggml-model-q4_k_m.gguf",
    # model_path="D:\\Programming\\llama.cpp\\models\\Code-34B-Instruct\\ggml-model-q4_k_m.gguf",
	n_gpu_layers=n_gpu_layers,
	n_batch=n_batch,
	callback_manager=callback_manager,
	verbose=True,
    repeat_penalty=1.1,
    ctx_size=4096,
    top_k=40,
    top_p=0.9,
    temp=0.1,
    n=-1
	# Verbose is required to pass to the callback manager
)

#-ngl 16000 -n -1 --repeat_penalty 1.1 --color -i -r "USER:"  
#--ctx_size 4096 -ins -b 128 --top_k 40 --top_p 0.9 --temp 0.1 -f prompts/chat-with-vicuna-v1.txt

llm_chain = LLMChain(prompt=prompt, llm=llm)

# question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
question = "조선의 세종대왕은 언제 태어났나?"

llm_chain.run(question)
