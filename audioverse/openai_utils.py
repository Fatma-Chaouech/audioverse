import openai
from audioverse.prompts.base import BasePrompt


def query_model(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message["content"]


def stream_query_model(prompt: BasePrompt):
    response_stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
        temperature=0.2,
        stream=True,
    )
    for response in response_stream:
        try:
            if (
                response["choices"][0]["finish_reason"] is None
                and response["choices"][0]["delta"]["content"] != ""
            ):
                yield response["choices"][0]["delta"]["content"]
        except Exception as e:
            raise ValueError("Error:", e)


def generate_embeddings(input):
    response = openai.Embedding.create(model="text-embedding-ada-002", input=input)
    try:
        embedding = response["data"][0]["embedding"]
        return embedding
    except KeyError:
        print("Error: " + str(response["error"]))
