import pinecone


class PineconeVectorDB:
    def __init__(self, api_key, environment):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = None

    def create_pinecone_index(self, index_name, dimension):
        self.index = pinecone.create_index(index_name, dimension=dimension)
        return self.index

    def get_pinecone_index(self, index_name):
        if index_name in pinecone.list_indexes():
            self.index = pinecone.Index(index_name)
        return self.index

    def embeddings_to_pinecone(self, id_embeddings, index):
        index.upsert(items=id_embeddings)
