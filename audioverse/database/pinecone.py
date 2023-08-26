import pinecone
from audioverse.decorators import simple_exception_catch_decorator


class PineconeVectorDB:
    def __init__(self, api_key, environment):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = None

    def create_pinecone_index(self, index_name, dimension):
        self.index = pinecone.Index(index_name, dimension=dimension)
        return self.index

    def get_pinecone_index(self):
        return self.index

    def has_embeddings(self, index_name):
        return (
            self.has_index(index_name)
            and self.index.describe_index_stats()["total_vector_count"] != 0
        )

    def has_index(self, index_name):
        if index_name in pinecone.list_indexes():
            self.index = pinecone.Index(index_name)
            return True
        return False

    @simple_exception_catch_decorator
    def embeddings_to_pinecone(self, id_embeddings):
        self.index.upsert(vectors=id_embeddings)