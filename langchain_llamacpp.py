from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
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

# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\13B-Chat\\ggml-model-q4_k_m.gguf")
model_path = expanduser("D:\\Programming\\llama.cpp\\models\\16K-Vicuna-13B\\ggml-model-q4_k_m.gguf")
# model_path = expanduser("D:\\Programming\\llama.cpp\\models\\M-SOLAR-10.7B-V1\\ggml-model-q4_k_m.gguf")

n_gpu_layers = 400
# Change this value based on your model and your GPU VRAM pool.
n_batch = 512  
llm = LlamaCpp(
    # n_gpu_layers=n_gpu_layers,
	# n_batch=n_batch,
    model_path=model_path,
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    # callback_manager=callback_manager, 
    verbose=True, # Verbose is required to pass to the callback manager
    streaming=False,
)
model = Llama2Chat(llm=llm)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = LLMChain(llm=model, prompt=prompt_template, memory=memory)

print(
    chain.run(
        text="What can I see in Vienna? Propose a few locations. Names only, no details."
    )
)
print(chain.run(text="Tell me more about #2."))