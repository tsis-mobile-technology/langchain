from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_experimental.chat_models import Llama2Chat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage

template_messages = [
    SystemMessage(content="You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{text}"),
]
prompt_template = ChatPromptTemplate.from_messages(template_messages)
from os.path import expanduser

from langchain_community.llms import LlamaCpp

# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\7B\\ggml-model-q4_0.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\13B-Chat\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\M-SOLAR-10.7B-V1\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\M-SOLAR-10.7B-V2\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\Code-13B-Instruct\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\Code-34B-Instruct\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\M-WIZARD-13B\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\Code-34B-Python\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\Code-13B-Python\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\C-WIZARD-33B-Python\\ggml-model-q4_k_m.gguf")
model_path = expanduser("D:\\Programming\\llama.cpp\\models\\16K-Vicuna-13B\\ggml-model-q4_k_m.gguf")
n_batch = 1024
max_new_tokens = 2048
temperature = 0.5
top_p = 0.95
top_k = 40
repetition_penalty = 1.1
callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])
n_gpu_layers = 40
# Change this value based on your model and your GPU VRAM pool.
  
llm = LlamaCpp(
    n_gpu_layers=n_gpu_layers,
	n_batch=n_batch,
    model_path=model_path,
    temp=temperature,
    max_new_tokens=max_new_tokens,
    ctx_size=30000,
    top_k=top_k,
    top_p=top_p,
    repeat_penalty=repetition_penalty,
    callback_manager=callback_manager, 
    verbose=True, # Verbose is required to pass to the callback manager
    streaming=False
)
model = Llama2Chat(llm=llm)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = LLMChain(llm=model, prompt=prompt_template, memory=memory)

## Vicuna Model test prompt(16k)
print(
    chain.run(
        text = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
USER: Hello!
ASSISTANT: Hello!</s>
USER: How are you?
ASSISTANT: I am good.</s>
"""
    )
)

## Python Code Model test prompt(LLAMA 2 LLM)
# print(
#     chain.run(
#         text="""[INST] Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:
#         I have a Python class that would benefit from a binary sorting algorithm. Could you please create a Python class that takes in a list of values, sorts them using binary sort, and returns the sorted list. 
#         [/INST]"""
#     )
# )

## Python Code Model test prompt(WIZARD LLM)
# print(
#     chain.run("""### System Prompt
#               Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:
#         ### User Message
#               I have a Python class that would benefit from a binary sorting algorithm. Could you please create a Python class that takes in a list of values, sorts them using binary sort, and returns the sorted list. 
#         ### Assistant
#         """
#     )
# )

## Math Model test prompt
# print(
#     chain.run(text="""### System Prompt
#         ### User Message
#                Fifty people and 50 lamps were numbered from 1 to 50. All of these lights are turned on by the number 1, and those with number 2 are turned off by numbers in multiples of 2. If you are number n, look at the light with the number of the multiple of n and turn it off if it's on, and turn it on if it's off. After all 50 people have done this one after the other, ask how many lights are on.
#         ### Assistant
#         """
#     )
# )

# print(
#     chain.run("""### System Prompt
#               Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:
#         ### User Message
#               In Python, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month
#         ### Assistant
#         """
#     )
# )