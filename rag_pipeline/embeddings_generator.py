"""
Embeddings Generator
====================
Converts security knowledge documents into AI-searchable embeddings.

WHAT ARE EMBEDDINGS?
--------------------
Embeddings are like "fingerprints" or "coordinates" for text.
Instead of matching exact words, AI can understand meaning.

Example:
- "SQL injection" and "database attack" have similar embeddings
- Even though the words are different, AI knows they're related

This helps find relevant security info even when exact words don't match!
"""

from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np

# Model we'll use - it's pre-trained and ready to go!
# 'all-MiniLM-L6-v2' is:
# - Small and fast
# - Good quality embeddings
# - Perfect for beginners and hackathons
MODEL_NAME = 'all-MiniLM-L6-v2'


class EmbeddingsGenerator:
    """
    Simple embeddings generator for security documents.
    
    This class takes text and converts it into numbers (embeddings)
    that AI can understand and compare.
    """
    
    def __init__(self):
        """
        Initialize the embeddings model.
        
        First time running this will download the model (~80MB).
        After that, it's cached and loads quickly.
        """
        print("🤖 Loading embeddings model...")
        print(f"   Model: {MODEL_NAME}")
        
        # Load the pre-trained model
        self.model = SentenceTransformer(MODEL_NAME)
        
        print("   ✅ Model loaded successfully!")
        print(f"   Embedding size: {self.model.get_sentence_embedding_dimension()} dimensions")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Convert a single piece of text into an embedding.
        
        Args:
            text: The text to convert (e.g., a CVE description)
            
        Returns:
            A numpy array of numbers representing the text
            
        Example:
            >>> gen = EmbeddingsGenerator()
            >>> embedding = gen.generate_embedding("SQL injection attack")
            >>> print(embedding.shape)
            (384,)  # 384 numbers representing this text
        """
        # The model does all the magic here!
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Convert multiple texts into embeddings at once.
        
        This is faster than calling generate_embedding() one by one.
        
        Args:
            texts: List of texts to convert
            
        Returns:
            2D numpy array where each row is one text's embedding
            
        Example:
            >>> texts = ["SQL injection", "XSS attack", "Buffer overflow"]
            >>> embeddings = gen.generate_embeddings_batch(texts)
            >>> print(embeddings.shape)
            (3, 384)  # 3 texts, each with 384 numbers
        """
        print(f"🔄 Generating embeddings for {len(texts)} documents...")
        
        # Batch processing is much faster!
        embeddings = self.model.encode(texts, 
                                       convert_to_numpy=True,
                                       show_progress_bar=True)
        
        print(f"   ✅ Generated {len(embeddings)} embeddings")
        return embeddings
    
    def embed_documents(self, documents: List[Dict[str, str]]) -> List[Dict]:
        """
        Add embeddings to knowledge base documents.
        
        Takes documents from KnowledgeBaseLoader and adds embeddings to them.
        
        Args:
            documents: List of dicts with 'content', 'source', 'id'
            
        Returns:
            Same documents but with 'embedding' added to each
            
        Example:
            >>> from knowledge_loader import KnowledgeBaseLoader
            >>> kb = KnowledgeBaseLoader()
            >>> kb.load_all()
            >>> gen = EmbeddingsGenerator()
            >>> docs_with_embeddings = gen.embed_documents(kb.get_all_documents())
        """
        if not documents:
            print("⚠️ No documents to embed!")
            return []
        
        print(f"\n📊 Processing {len(documents)} knowledge base documents...")
        
        # Extract just the text content
        texts = [doc['content'] for doc in documents]
        
        # Generate all embeddings at once (faster!)
        embeddings = self.generate_embeddings_batch(texts)
        
        # Add embeddings back to the documents
        embedded_docs = []
        for i, doc in enumerate(documents):
            doc_copy = doc.copy()
            doc_copy['embedding'] = embeddings[i]
            embedded_docs.append(doc_copy)
        
        print(f"✅ All documents now have embeddings!\n")
        return embedded_docs
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate how similar two embeddings are.
        
        Returns a score from -1 to 1:
        - 1.0 = Very similar
        - 0.0 = Not related
        - -1.0 = Opposite (rare)
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score (cosine similarity)
        """
        # Cosine similarity - standard way to compare embeddings
        from numpy.linalg import norm
        
        similarity = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
        return float(similarity)


# Example usage and testing
def main():
    """
    Test the embeddings generator.
    
    This shows you how embeddings work with simple examples.
    """
    print("=" * 70)
    print("🧪 Embeddings Generator - Test Run")
    print("=" * 70)
    
    # Create generator
    gen = EmbeddingsGenerator()
    
    print("\n" + "=" * 70)
    print("📝 Testing with Sample Security Texts")
    print("=" * 70)
    
    # Sample texts
    texts = [
        "SQL injection vulnerability in login form",
        "Database attack through malicious SQL commands",
        "Brute force password attack on SSH service",
        "Cross-site scripting in web application"
    ]
    
    # Generate embeddings
    embeddings = gen.generate_embeddings_batch(texts)
    
    print(f"\n✅ Generated embeddings shape: {embeddings.shape}")
    print(f"   ({embeddings.shape[0]} documents × {embeddings.shape[1]} dimensions)")
    
    # Test similarity
    print("\n" + "=" * 70)
    print("🔍 Testing Similarity Scores")
    print("=" * 70)
    
    sim1_2 = gen.calculate_similarity(embeddings[0], embeddings[1])
    sim1_3 = gen.calculate_similarity(embeddings[0], embeddings[2])
    
    print(f"\nText 1: '{texts[0]}'")
    print(f"Text 2: '{texts[1]}'")
    print(f"Similarity: {sim1_2:.3f} (should be HIGH - both about SQL)")
    
    print(f"\nText 1: '{texts[0]}'")
    print(f"Text 3: '{texts[2]}'")
    print(f"Similarity: {sim1_3:.3f} (should be LOWER - different attacks)")
    
    print("\n" + "=" * 70)
    print("💡 What This Means:")
    print("=" * 70)
    print("Higher similarity = More related topics")
    print("This is how RAG finds relevant security knowledge!")
    print("=" * 70)


if __name__ == "__main__":
    main()
