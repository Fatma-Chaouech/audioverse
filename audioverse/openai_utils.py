import openai


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


def generate_embeddings(input):
    response = openai.Embedding.create(model="text-embedding-ada-002", input=input)
    try:
        embedding = response["data"][0]["embedding"]
        return embedding
    except KeyError:
        print("Error: " + str(response["error"]))
