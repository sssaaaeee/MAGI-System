import openai
import os
from typing import List

# OpenAI APIキーの設定
# sk-proj-RGOJuLUQbLrn1bdUDxtTT3BlbkFJi63IbTrAvVi1EoOCxnHa
openai.api_key = os.getenv("OPENAI_API_KEY")

# 各人格のプロンプトを定義
def melchior_prompt(data: str) -> str:
    return f"You are Melchior, the scientist. Analyze the following data and provide your decision: {data}"

def balthazar_prompt(data: str) -> str:
    return f"You are Balthazar, the mother. Consider the following data with empathy and provide your decision: {data}"

def casper_prompt(data: str) -> str:
    return f"You are Casper, the woman. Evaluate the following data and provide your decision: {data}"

# ChatGPT APIを呼び出す関数
def get_chatgpt_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# MAGIシステムクラス
class MAGISystem:
    def __init__(self):
        self.prompts = {
            "melchior": melchior_prompt,
            "balthazar": balthazar_prompt,
            "casper": casper_prompt
        }

    def make_decision(self, input_data: str) -> str:
        decisions = []
        for key, prompt_func in self.prompts.items():
            prompt = prompt_func(input_data)
            decision = get_chatgpt_response(prompt)
            decisions.append(decision)
            print(f"{key.capitalize()} Decision: {decision}")  # 各人格の決定を表示
        return self.majority_vote(decisions)

    def majority_vote(self, decisions: List[str]) -> str:
        decision_counts = {decision: decisions.count(decision) for decision in set(decisions)}
        majority_decision = max(decision_counts, key=decision_counts.get)
        return majority_decision

# MAGIシステムのインスタンスを作成
magi = MAGISystem()

# 意見を求めるデータ
input_data = "we should prepare for the next attack"

# MAGIシステムからの意思決定を取得
decision = magi.make_decision(input_data)
print("MAGI System Final Decision:", decision)
