import openai
import os

# set your OpenAI Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_memory(memory_list, memory_type):
    summarized_memory = []
    for item in memory_list:
        # 使用OpenAI模型生成摘要
        summary_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 使用更便宜的模型进行摘要
            messages=[
                {"role": "system", "content": f"请对以下{memory_type}进行摘要："},
                {"role": "user", "content": item}
            ]
        )
        summarized_memory.append(summary_response.choices[0].message['content'].strip())
    return summarized_memory

def get_openai_response(short_term_memory, long_term_memory, dynamic_memory, query, query_result):
    # 生成摘要
    short_term_memory_summary = summarize_memory(short_term_memory, "短期记忆")
    long_term_memory_summary = summarize_memory(long_term_memory, "长期记忆")
    dynamic_memory_summary = summarize_memory(dynamic_memory, "动态记忆")

    # 转换摘要为字符串
    short_term_memory_str = "\n".join(short_term_memory_summary)
    long_term_memory_str = "\n".join(long_term_memory_summary)
    dynamic_memory_str = "\n".join(dynamic_memory_summary)

    # 组合所有信息
    messages = [
        {"role": "system", "content": "You are an AI assistant helping a patient post-discharge."},
        {"role": "user", "content": "Short Term Memory includes but not limited to physical index records, symptoms, diet, medication, and exercise records, all data will be stored for ten days.\nShort Term Memory:\n" + short_term_memory_str},
        {"role": "user", "content": "Long-term memory is used to store important documents provided by doctors, pharmacists, etc. This information will be retained throughout the discharge rehabilitation care period.\nLong Term Memory:\n" + long_term_memory_str},
        {"role": "user", "content": "Dynamic memory is used to record the patient’s past fifteen interactions, which can provide reference for subsequent questions.\nDynamic Memory:\n" + dynamic_memory_str},
        {"role": "user", "content": "The query result is the result of indexing the query in the vector database after embedding the query, which can be used for reference.\nQuery Results:\n" + str(query_result)},
        {"role": "user", "content": "Please combine the above information to answer the patient's query.\nQuery:\n" + query},
        {"role": "user", "content": "Please give patient feedback based on the query."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-32k",  # 选择模型
        messages=messages,
    )

    return response.choices[0].message['content'].strip()

# 示例数据
short_term_memory = ["症状记录：头痛，头晕，服用药物：阿司匹林，饮食：低盐饮食"]
long_term_memory = ["医生提供的文件：出院记录，药物说明"]
dynamic_memory = ["上次询问关于药物剂量的问题", "之前的反馈记录：患者症状有所改善"]
query = "我今天感到头痛，请问应该怎么办？"
query_result = ["参考结果：可能与高血压有关，建议继续服用降压药"]

# 获取OpenAI响应
response = get_openai_response(short_term_memory, long_term_memory, dynamic_memory, query, query_result)
print(response)
通过这种方式，可以减少传递给模型的token数量，同时保留重要信息，提高回答的有效性。

用英语生成里面的全部内容
ChatGPT
Here is the English version of the code with all the content translated:

python
Copy code
import openai
import os

# set your OpenAI Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_memory(memory_list, memory_type):
    summarized_memory = []
    for item in memory_list:
        # Use OpenAI model to generate a summary
        summary_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a cheaper model for summarization
            messages=[
                {"role": "system", "content": f"Please summarize the following {memory_type}:"},
                {"role": "user", "content": item}
            ]
        )
        summarized_memory.append(summary_response.choices[0].message['content'].strip())
    return summarized_memory

def get_openai_response(short_term_memory, long_term_memory, dynamic_memory, query, query_result):
    # Generate summaries
    short_term_memory_summary = summarize_memory(short_term_memory, "short-term memory")
    long_term_memory_summary = summarize_memory(long_term_memory, "long-term memory")
    dynamic_memory_summary = summarize_memory(dynamic_memory, "dynamic memory")

    # Convert summaries to strings
    short_term_memory_str = "\n".join(short_term_memory_summary)
    long_term_memory_str = "\n".join(long_term_memory_summary)
    dynamic_memory_str = "\n".join(dynamic_memory_summary)

    # Combine all information
    messages = [
        {"role": "system", "content": "You are an AI assistant helping a patient post-discharge."},
        {"role": "user", "content": "Short Term Memory includes but not limited to physical index records, symptoms, diet, medication, and exercise records, all data will be stored for ten days.\nShort Term Memory:\n" + short_term_memory_str},
        {"role": "user", "content": "Long-term memory is used to store important documents provided by doctors, pharmacists, etc. This information will be retained throughout the discharge rehabilitation care period.\nLong Term Memory:\n" + long_term_memory_str},
        {"role": "user", "content": "Dynamic memory is used to record the patient’s past fifteen interactions, which can provide reference for subsequent questions.\nDynamic Memory:\n" + dynamic_memory_str},
        {"role": "user", "content": "The query result is the result of indexing the query in the vector database after embedding the query, which can be used for reference.\nQuery Results:\n" + str(query_result)},
        {"role": "user", "content": "Please combine the above information to answer the patient's query.\nQuery:\n" + query},
        {"role": "user", "content": "Please give patient feedback based on the query."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Choose your model
        messages=messages,
    )

    return response.choices[0].message['content'].strip()
