# -*- coding:utf-8 -*-
import gradio as gr

# ChatGPT 设置
initial_prompt = "You are a helpful assistant."
API_URL = "https://api.openai.com/v1/chat/completions"
BALANCE_API_URL="https://api.openai.com/dashboard/billing/credit_grants"
HISTORY_DIR = "history"
TEMPLATES_DIR = "templates"

# 错误信息
standard_error_msg = "☹️发生了错误："  # 错误信息的标准前缀
error_retrieve_prompt = "请检查网络连接，或者API-Key是否有效。"  # 获取对话时发生错误
connection_timeout_prompt = "连接超时，无法获取对话。"  # 连接超时
read_timeout_prompt = "读取超时，无法获取对话。"  # 读取超时
proxy_error_prompt = "代理错误，无法获取对话。"  # 代理错误
ssl_error_prompt = "SSL错误，无法获取对话。"  # SSL 错误
no_apikey_msg = "API key长度不是51位，请检查是否输入正确。"  # API key 长度不足 51 位
no_input_msg = "请输入对话内容。"  # 未输入对话内容

max_token_streaming = 3500  # 流式对话时的最大 token 数
timeout_streaming = 30  # 流式对话时的超时时间
max_token_all = 3500  # 非流式对话时的最大 token 数
timeout_all = 200  # 非流式对话时的超时时间
enable_streaming_option = True  # 是否启用选择选择是否实时显示回答的勾选框
HIDE_MY_KEY = False  # 如果你想在UI中隐藏你的 API 密钥，将此值设置为 True
CONCURRENT_COUNT = 100 # 允许同时使用的用户数量

SIM_K = 5
INDEX_QUERY_TEMPRATURE = 1.0

title = """<h1 align="left" style="min-width:200px; margin-top:0;">ChatGPT实验室</h1>"""
description = """\
<div align="center" style="margin:16px 0">
此App使用 `gpt-3.5-turbo` 大语言模型
</div>
"""

summarize_prompt = "你是谁？我们刚才聊了什么？"  # 总结对话时的 prompt

MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    #"gpt-4",
    #"gpt-4-0314",
    #"gpt-4-32k",
    #"gpt-4-32k-0314",
]  # 可选的模型

REPLY_LANGUAGES = [
    "中文",
    "English",
    "日本語",
    "Español",
    "Français",
    "Deutsch",
    "跟随问题语言（不稳定）"
]


WEBSEARCH_PTOMPT_TEMPLATE = """\
Web search results:

{web_results}
Current date: {current_date}

Instructions: Using the provided web search results, write a comprehensive reply to the given query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.
Query: {query}
Reply in {reply_language}
"""

PROMPT_TEMPLATE = """\
Context information is below.
---------------------
{context_str}
---------------------
Current date: {current_date}.
Using the provided context information, write a comprehensive reply to the given query.
Make sure to cite results using [number] notation after the reference.
If the provided context information refer to multiple subjects with the same name, write separate answers for each subject.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
Reply in {reply_language}
"""

REFINE_TEMPLATE = """\
The original question is as follows: {query_str}
We have provided an existing answer: {existing_answer}
We have the opportunity to refine the existing answer
(only if needed) with some more context below.
------------
{context_msg}
------------
Given the new context, refine the original answer to better
Reply in {reply_language}
If the context isn't useful, return the original answer.
"""

ALREADY_CONVERTED_MARK = "<!-- ALREADY CONVERTED BY PARSER. -->"

small_and_beautiful_theme = gr.themes.Soft(
        primary_hue=gr.themes.Color(
            c50="#02C160",
            c100="rgba(2, 193, 96, 0.2)",
            c200="#02C160",
            c300="rgba(2, 193, 96, 0.32)",
            c400="rgba(2, 193, 96, 0.32)",
            c500="rgba(2, 193, 96, 1.0)",
            c600="rgba(2, 193, 96, 1.0)",
            c700="rgba(2, 193, 96, 0.32)",
            c800="rgba(2, 193, 96, 0.32)",
            c900="#02C160",
            c950="#02C160",
        ),
        secondary_hue=gr.themes.Color(
            c50="#576b95",
            c100="#576b95",
            c200="#576b95",
            c300="#576b95",
            c400="#576b95",
            c500="#576b95",
            c600="#576b95",
            c700="#576b95",
            c800="#576b95",
            c900="#576b95",
            c950="#576b95",
        ),
        neutral_hue=gr.themes.Color(
            name="gray",
            c50="#f9fafb",
            c100="#f3f4f6",
            c200="#e5e7eb",
            c300="#d1d5db",
            c400="#B2B2B2",
            c500="#808080",
            c600="#636363",
            c700="#515151",
            c800="#393939",
            c900="#272727",
            c950="#171717",
        ),
        radius_size=gr.themes.sizes.radius_sm,
    ).set(
        button_primary_background_fill="#06AE56",
        button_primary_background_fill_dark="#06AE56",
        button_primary_background_fill_hover="#07C863",
        button_primary_border_color="#06AE56",
        button_primary_border_color_dark="#06AE56",
        button_primary_text_color="#FFFFFF",
        button_primary_text_color_dark="#FFFFFF",
        button_secondary_background_fill="#F2F2F2",
        button_secondary_background_fill_dark="#2B2B2B",
        button_secondary_text_color="#393939",
        button_secondary_text_color_dark="#FFFFFF",
        # background_fill_primary="#F7F7F7",
        # background_fill_primary_dark="#1F1F1F",
        block_title_text_color="*primary_500",
        block_title_background_fill="*primary_100",
        input_background_fill="#F6F6F6",
    )
