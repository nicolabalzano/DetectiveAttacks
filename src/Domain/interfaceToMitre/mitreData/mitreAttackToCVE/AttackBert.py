from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.domain.Singleton import singleton


@singleton
class AttackBert:

    def __init__(self):
        self.model = SentenceTransformer('basel/ATTACK-BERT')

    def check_similarity(self, sentence1: str, sentence2: str):
        embeddings = self.model.encode([sentence1, sentence2])
        cosine_similarity_number = cosine_similarity([embeddings[0]], [embeddings[1]])
        return cosine_similarity_number[0][0]