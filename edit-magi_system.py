from openai import OpenAI
import os
from typing import List

client = OpenAI()

# 適用したAPIキーの確認コマンド
# echo $OPENAI_API_KEY

# プログラム実行コマンド
# python edit-magi_system.py


# 各人格のプロンプトを定義
def melchior_prompt(data: str) -> str:
    return f"You are Melchior, the scientist. Analyze the following data and provide your decision: {data}"

def balthazar_prompt(data: str) -> str:
    return f"You are Balthazar, the mother. Consider the following data with empathy and provide your decision: {data}"

def casper_prompt(data: str) -> str:
    return f"You are Casper, the woman. Evaluate the following data from a romantic point of view and provide your decision: {data}"

# 各人格の回答を統合するプロンプトを定義
def integrative_prompt(data: str) -> str:
    return f"You are a general-purpose artificial intelligence called MAGI. Make the best decision by complementing each other with the following three opinions derived from different thoughts: {data}"

# ChatGPT APIを呼び出す関数
def get_chatgpt_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "日本語で答えてください"}, # 日本語ユーザに対応
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# MAGIシステムクラス
class MAGISystem:
    def __init__(self):
        self.prompts = {
            "melchior": melchior_prompt,    # メルキオール：科学者としての思考
            "balthazar": balthazar_prompt,  # バルタザール：母親としての思考
            "casper": casper_prompt         # カスパー：女性としての思考
        }

    def make_decision(self, input_data: str) -> str:
        decisions = []
        for key, prompt_func in self.prompts.items(): # 各人格の決定を全て生成するまで繰り返し
            prompt = prompt_func(input_data)          # 質問を各人格の仕様に合わせる->prompt
            decision = get_chatgpt_response(prompt)   # 回答decisionを生成
            decisions.append(decision)                # decision->配列decisions
            print(f"\n{key.capitalize()} Decision: {decision} \n")  # 各人格の決定を表示
        return self.majority_vote(decisions)

    def majority_vote(self, decisions: List[str]) -> str:
        decisions_str = "\n".join(decisions)                    # 各回答を連結->decisions_str
        final_prompt = integrative_prompt(decisions_str)        # 統合のための質問->final_prompt
        answer_decision = get_chatgpt_response(final_prompt)    # 最終的な回答->answer_decision
        return answer_decision

# MAGIシステムのインスタンスを作成
magi = MAGISystem()

# 意見を求めるデータ
input_data = input("\n\nMAGI chat : ")

# MAGIシステムからの意思決定を取得
decision = magi.make_decision(input_data)
print(f"\n\nMAGI System Final Decision: {decision}\n\n")
