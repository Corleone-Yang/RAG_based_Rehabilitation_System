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
        model="gpt-4-32k",  # Choose your model
        messages=messages,
    )

    return response.choices[0].message['content'].strip()
