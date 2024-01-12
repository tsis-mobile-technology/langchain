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
model_path = expanduser("D:\\Programming\\llama.cpp\\models\\Code-34B-Python\\ggml-model-q4_k_m.gguf")
n_batch = 128
max_new_tokens = 512
temperature = 0.7
top_p = 0.95
top_k = 40
repetition_penalty = 1.1
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\M-WIZARD-13B\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\C-WIZARD-33B-Python\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\16K-Vicuna-13B\\ggml-model-q4_k_m.gguf")

callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])
n_gpu_layers = 40
# Change this value based on your model and your GPU VRAM pool.
  
llm = LlamaCpp(
    n_gpu_layers=n_gpu_layers,
	n_batch=n_batch,
    model_path=model_path,
    temp=temperature,
    max_new_tokens=max_new_tokens,
    ctx_size=4096,
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

print(
    chain.run("""### System Prompt
              Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:
        ### User Message
              In Python, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month
        ### Assistant
        """
    )
)
print(
    chain.run(text="""### System Prompt
        ### User Message
              Tell me more about other code.
        ### Assistant
        """
    )
)

# print(
#     chain.run(
#         text="""[INST] Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:
#         In Bash, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month
#         [/INST]"""
#     )
# )
# print(chain.run(text="[INST]\nTell me more about other code.[\INST]\n\n"))

# print(
#     chain.run(
#         text="[INST]\nWhat can I see in Vienna? Propose a few locations. Names only, no details.[\INST]\n\n"
#     )
# )
# print(chain.run(text="[INST]\nTell me more about #2.[\INST]\n\n"))

# print(
#     chain.run(
#         text="대한민국에 있는 유명한 산 이름을 10개 정도 나열해주세요."
#     )
# )
# print(chain.run(text="Tell me more about #2."))