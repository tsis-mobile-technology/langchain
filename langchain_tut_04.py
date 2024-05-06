"""
랭체인(langchain) + 정형데이터(CSV, Excel) - ChatGPT 기반 데이터분석 (4)
이번 포스팅에서는 랭체인(LangChain) 을 활용하여 정형데이터(CSV, Excel) 에 대한 ChatGPT 기반 질의응답을 통해 데이터 분석하는 방법 에 대해 알아보겠습니다.

이번 튜토리얼에서는 langchain 의 create_pandas_dataframe_agent() 을 통해 에이전트를 생성한 뒤, 생성된 에이전트에 자연어로 데이터에 대한 질의 응답 을 통해 원하는 분석 결과를 도출하는 방법에 대해 다루겠습니다.

한가지 흥미로운 사실은 자연어로 에이전트에 질문하면, 에이전트가 이를 pandas 문법을 변환하여 코드를 실행한 뒤, 결과를 다시 자연어로 반환해 준다는 점입니다. 에이전트가 답변을 도출하는 과정에서 실행한 pandas 코드도 확인 할 수 있습니다.

✔️ (이전글) LangChain 튜토리얼

랭체인(langchain)의 OpenAI GPT 모델(ChatOpenAI) 사용법
랭체인(langchain) + 허깅페이스(HuggingFace) 모델 사용법
랭체인(langchain) + 챗(chat) - ConversationChain, 템플릿 사용법
🌱 환경설정Permalink
라이브러리 설치

# 필요한 라이브러리 설치
# pip install langchain openai 
OPENAI API KEY 를 설정합니다.

# OPENAI_API
"""
import os

os.environ['OPENAI_API_KEY'] = 'sk-openai-api-key'
"""
🔥 데이터 로드Permalink
pandas를 활용하여 csv 파일을 DataFrame 으로 로드합니다.
"""
import pandas as pd

# csv 파일을 데이터프레임으로 로드
df = pd.read_csv('./titanic.csv')
df.head()
"""
survived	pclass	sex	age	sibsp	parch	fare	embarked	class	who	adult_male	deck	embark_town	alive	alone
0	0	3	male	22.0	1	0	7.2500	S	Third	man	True	NaN	Southampton	no	False
1	1	1	female	38.0	1	0	71.2833	C	First	woman	False	C	Cherbourg	yes	False
2	1	3	female	26.0	0	0	7.9250	S	Third	woman	False	NaN	Southampton	yes	True
3	1	1	female	35.0	1	0	53.1000	S	First	woman	False	C	Southampton	yes	False
4	0	3	male	35.0	0	0	8.0500	S	Third	man	True	NaN	Southampton	no	True
🔥 Pandas DataFrame AgentPermalink
"""
#from langchain.agents import create_pandas_dataframe_agent # langchain 0.0.6
from langchain_experimental.agents import create_pandas_dataframe_agent # langchain 0.0.7
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType


# 에이전트 생성
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, 
               model='gpt-3.5-turbo-16k'),        # 모델 정의
    df,                                    # 데이터프레임
    verbose=True,                          # 추론과정 출력
    agent_type=AgentType.OPENAI_FUNCTIONS, # AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
# 질의
agent.run('데이터의 행과 열의 갯수는 어떻게 돼?')
"""
Entering new AgentExecutor chain...
Invoking: `python_repl_ast` with `{'query': 'df.shape'}`


(891, 15)데이터프레임 `df`는 891개의 행과 15개의 열로 구성되어 있습니다.

Finished chain.
'데이터프레임 `df`는 891개의 행과 15개의 열로 구성되어 있습니다.'

"""
# 질의
agent.run('남자 승객의 생존율을 어떻게 돼? %로 알려줘')
"""
Entering new AgentExecutor chain...Thought: To find the survival rate of male passengers, I need to filter the dataframe for rows where 'sex' is 'male', then calculate the mean of the 'survived' column. This will give the proportion of male passengers who survived, which I can then multiply by 100 to get a percentage.
Action: python_repl_ast
Action Input: male_survival_rate = df[df['sex'] == 'male']['survived'].mean() * 100
Observation: 
Thought:Now I need to print the survival rate to see the result.
Action: python_repl_ast
Action Input: print(male_survival_rate)
Observation: 18.890814558058924

Thought:I now know the final answer
Final Answer: 남자 승객의 생존율은 약 18.89%입니다.

Finished chain.
'남자 승객의 생존율은 약 18.89%입니다.'

"""
# 질의
agent.run('나이가 15세 이하인 승객중 1,2등급에 탑승한 남자 승객의 생존율은 어떻게 돼? %로 알려줘')
"""
Entering new AgentExecutor chain...
Invoking: `python_repl_ast` with `{'query': "df_child_male = df[(df['age'] <= 15) & (df['sex'] == 'male') & (df['pclass'].isin([1, 2]))]\nchild_male_survival_rate = df_child_male['survived'].mean() * 100\nchild_male_survival_rate"}`


100.0나이가 15세 이하인 승객 중 1,2등급에 탑승한 남자 승객의 생존율은 100%입니다.

Finished chain.
'나이가 15세 이하인 승객 중 1,2등급에 탑승한 남자 승객의 생존율은 100%입니다.'
🔥 2개 이상의 DataFramePermalink
2개 이상의 데이터프레임에 기반한 LLM 기반 질의를 할 수 있습니다. 2개 이상의 데이터프레임 입력시 [] 로 묶어주면 됩니다.


"""
# 샘플 데이터프레임 생성
df1 = df.copy()
df1 = df1.fillna(0)
df1.head()
"""
survived	pclass	sex	age	sibsp	parch	fare	embarked	class	who	adult_male	deck	embark_town	alive	alone
0	0	3	male	22.0	1	0	7.2500	S	Third	man	True	0	Southampton	no	False
1	1	1	female	38.0	1	0	71.2833	C	First	woman	False	C	Cherbourg	yes	False
2	1	3	female	26.0	0	0	7.9250	S	Third	woman	False	0	Southampton	yes	True
3	1	1	female	35.0	1	0	53.1000	S	First	woman	False	C	Southampton	yes	False
4	0	3	male	35.0	0	0	8.0500	S	Third	man	True	0	Southampton	no	True
"""
# 에이전트 생성
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, 
               model='gpt-4-0613'),
               [df, df1], 
               verbose=True
)

# 질의
agent.run('나이 컬럼의 나이의 평균차이는 어떻게 돼? %로 구해줘.')
"""
Entering new AgentExecutor chain...Thought: To find the average age difference between the two dataframes, I need to calculate the average age in each dataframe and then find the difference. I will then convert this difference to a percentage.

Action: python_repl_ast
Action Input: df1['age'].mean()
Observation: 29.69911764705882
Thought:The average age in df1 is approximately 29.7. Now I will calculate the average age in df2.

Action: python_repl_ast
Action Input: df2['age'].mean()
Observation: 23.79929292929293
Thought:The average age in df2 is approximately 23.8. Now I will calculate the difference between the two averages.

Action: python_repl_ast
Action Input: abs(df1['age'].mean() - df2['age'].mean())
Observation: 5.899824717765892
Thought:The difference in average age between df1 and df2 is approximately 5.9. Now I will convert this difference to a percentage of the average age in df1.

Action: python_repl_ast
Action Input: (abs(df1['age'].mean() - df2['age'].mean()) / df1['age'].mean()) * 100
Observation: 19.865319865319858
Thought:The percentage difference in average age between df1 and df2 is approximately 19.87%.

Final Answer: The average age difference between the two dataframes is approximately 19.87%.

Finished chain.
'The average age difference between the two dataframes is approximately 19.87%.'
"""

