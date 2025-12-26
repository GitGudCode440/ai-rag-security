"""
RAG Vector Store
================
Stores embeddings in ChromaDB for fast similarity search.

WHAT IS A VECTOR STORE?
-----------------------
A vector store is like a special database for embeddings.
Instead of searching by exact words, it searches by MEANING.

Think of it like this:
- Normal database: "Find rows where name = 'SQL injection'"
- Vector database: "Find documents SIMILAR to this alert"

WHY ChromaDB?
-------------
- Easy to use (perfect for beginners)
- Works locally (no cloud needed)
- Fast similarity search
- Hackathon-friendly!
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os

# Directory to store ChromaDB data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "chroma_db")


class RAGVectorStore:
    """
    Simple vector store for security knowledge using ChromaDB.
    
    This class stores embeddings and retrieves relevant documents
    based on similarity to a query.
    """
    
    def __init__(self, collection_name: str = "security_knowledge"):
        """
        Initialize the vector store.
        
        Args:
            collection_name: Name for your knowledge collection
        """
        print("💾 Initializing ChromaDB vector store...")
        
        # Create directory if it doesn't exist
        os.makedirs(CHROMA_DB_DIR, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection_name = collection_name
        
        # Try to get existing collection, or create new one
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"   ✅ Loaded existing collection: '{collection_name}'")
            print(f"   📊 Current documents: {self.collection.count()}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Security knowledge base for RAG"}
            )
            print(f"   ✅ Created new collection: '{collection_name}'")
    
    def add_documents(self, documents: List[Dict], embeddings: List) -> None:
        """
        Add documents with their embeddings to the vector store.
        
        Args:
            documents: List of dicts with 'content', 'source', 'id'
            embeddings: List of embedding arrays matching the documents
            
        Example:
            >>> store = RAGVectorStore()
            >>> store.add_documents(embedded_docs, embeddings)
        """
        if not documents or not embeddings:
            print("⚠️ No documents to add!")
            return
        
        print(f"\n📥 Adding {len(documents)} documents to vector store...")
        
        # Prepare data for ChromaDB
        ids = [doc['id'] for doc in documents]
        contents = [doc['content'] for doc in documents]
        metadatas = [{'source': doc['source']} for doc in documents]
        
        # Convert embeddings to list format (ChromaDB requirement)
        embeddings_list = [emb.tolist() if hasattr(emb, 'tolist') else emb 
                          for emb in embeddings]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=contents,
            embeddings=embeddings_list,
            metadatas=metadatas
        )
        
        print(f"   ✅ Added successfully!")
        print(f"   📊 Total documents in store: {self.collection.count()}")
    
    def search(self, query_embedding, top_k: int = 3) -> List[Dict]:
        """
        Search for similar documents using a query embedding.
        
        Args:
            query_embedding: Embedding of the search query
            top_k: How many top results to return (default: 3)
            
        Returns:
            List of relevant documents with similarity scores
            
        Example:
            >>> # Get embedding for alert
            >>> alert_embedding = gen.generate_embedding("SQL injection detected")
            >>> # Search vector store
            >>> results = store.search(alert_embedding, top_k=3)
        """
        # Convert to list if needed
        query_emb_list = (query_embedding.tolist() 
                         if hasattr(query_embedding, 'tolist') 
                         else query_embedding)
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_emb_list],
            n_results=top_k
        )
        
        # Format results nicely
        formatted_results = []
        
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'source': results['metadatas'][0][i]['source'],
                    'id': results['ids'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def search_by_text(self, query_text: str, embeddings_gen, top_k: int = 3) -> List[Dict]:
        """
        Search using plain text (convenience method).
        
        This automatically generates the embedding for you.
        
        Args:
            query_text: The text to search for
            embeddings_gen: EmbeddingsGenerator instance
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
            
        Example:
            >>> from embeddings_generator import EmbeddingsGenerator
            >>> gen = EmbeddingsGenerator()
            >>> store = RAGVectorStore()
            >>> results = store.search_by_text("brute force attack", gen, top_k=3)
        """
        # Generate embedding for the query
        query_embedding = embeddings_gen.generate_embedding(query_text)
        
        # Search
        return self.search(query_embedding, top_k)
    
    def clear_collection(self) -> None:
        """
        Clear all documents from the collection.
        
        Use this if you want to rebuild the vector store from scratch.
        """
        print(f"🗑️ Clearing collection '{self.collection_name}'...")
        
        # Delete and recreate
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Security knowledge base for RAG"}
        )
        
        print("   ✅ Collection cleared!")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        return {
            'collection_name': self.collection_name,
            'total_documents': self.collection.count(),
            'storage_path': CHROMA_DB_DIR
        }


# Example usage and testing
def main():
    """
    Test the vector store with sample data.
    """
    print("=" * 70)
    print("🧪 RAG Vector Store - Test Run")
    print("=" * 70)
    
    # Import dependencies
    from embeddings_generator import EmbeddingsGenerator
    
    # Create components
    gen = EmbeddingsGenerator()
    store = RAGVectorStore()
    
    # Sample security documents
    sample_docs = [
        {
            'id': 'test_1',
            'content': 'SQL injection vulnerability allows attackers to execute malicious database commands',
            'source': 'test_cve.txt'
        },
        {
            'id': 'test_2',
            'content': 'Brute force attack uses automated tools to guess passwords',
            'source': 'test_mitre.txt'
        },
        {
            'id': 'test_3',
            'content': 'Cross-site scripting enables injection of malicious scripts into web pages',
            'source': 'test_cve.txt'
        }
    ]
    
    print("\n" + "=" * 70)
    print("📊 Generating Embeddings for Sample Documents")
    print("=" * 70)
    
    # Generate embeddings
    embeddings = gen.generate_embeddings_batch([doc['content'] for doc in sample_docs])
    
    # Clear any existing data
    store.clear_collection()
    
    # Add to vector store
    store.add_documents(sample_docs, embeddings)
    
    print("\n" + "=" * 70)
    print("🔍 Testing Similarity Search")
    print("=" * 70)
    
    # Test query
    query = "database attack with SQL commands"
    print(f"\nQuery: '{query}'")
    print("\nTop 3 similar documents:")
    print("-" * 70)
    
    results = store.search_by_text(query, gen, top_k=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Source: {result['source']}")
        print(f"   Content: {result['content'][:80]}...")
        if result['distance'] is not None:
            score = 1 - result['distance']  # Convert distance to similarity
            print(f"   Similarity: {score:.3f}")
    
    # Show stats
    print("\n" + "=" * 70)
    print("📈 Vector Store Statistics")
    print("=" * 70)
    stats = store.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Vector store test complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
