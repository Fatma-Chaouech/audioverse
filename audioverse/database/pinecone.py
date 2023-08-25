import pinecone


class PineconeVectorDB:
    def __init__(self, api_key, environment):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = None

    def create_pinecone_index(self, index_name, dimension):
        pinecone.create_index(index_name, dimension=dimension)
        self.index = pinecone.Index(index_name)
        return self.index

    def get_pinecone_index(self, index_name):
        if index_name in pinecone.list_indexes():
            self.index = pinecone.Index(index_name)
        return self.index

    def has_embeddings(self):
        return (
            self.index and self.index.describe_index_stats()["total_vector_count"] != 0
        )
    
    def has_index(self):
        return self.index is not None

    def embeddings_to_pinecone(self, id_embeddings, index):
        index.upsert(vectors=id_embeddings)
