from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.models.db_models import KnowledgeArticle
from backend.app.core.logging_config import logger


class RAGService:
    @staticmethod
    def search_knowledge_base(db: Session, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant knowledge base articles using TF-IDF vector embedding similarity search.
        """
        articles = db.query(KnowledgeArticle).all()
        if not articles:
            logger.warning("Knowledge Base is empty.")
            return []

        # Prepare corpus
        doc_texts = [f"{a.title} {a.category} {a.content}" for a in articles]
        doc_texts.append(query)  # Add user query at index -1

        # Calculate TF-IDF Embeddings
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(doc_texts)

        # Query vector is the last item
        query_vector = tfidf_matrix[-1]
        doc_vectors = tfidf_matrix[:-1]

        # Calculate Cosine Similarity Scores
        similarity_scores = cosine_similarity(query_vector, doc_vectors)[0]

        # Rank articles by similarity
        ranked_indices = similarity_scores.argsort()[::-1]

        results = []
        for idx in ranked_indices[:top_k]:
            score = float(similarity_scores[idx])
            # Only return articles above a minimal similarity threshold
            if score > 0.05:
                article = articles[idx]
                results.append({
                    "id": article.id,
                    "title": article.title,
                    "category": article.category,
                    "content": article.content,
                    "relevance_score": round(score, 4)
                })

        logger.info(f"Retrieved {len(results)} relevant KB articles for query: '{query[:30]}...'")
        return results