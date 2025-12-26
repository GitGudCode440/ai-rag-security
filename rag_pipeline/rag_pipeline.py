"""
RAG Pipeline - Complete System
===============================
Main RAG pipeline that combines everything together.

This is the MAIN file you'll use to:
1. Load knowledge base
2. Generate embeddings
3. Store in vector database
4. Retrieve relevant context for alerts

SIMPLE 3-STEP USAGE:
-------------------
1. Initialize: rag = RAGPipeline()
2. Build knowledge base: rag.build_knowledge_base()
3. Get context: context = rag.get_context_for_alert("SQL injection detected")
"""

from knowledge_loader import KnowledgeBaseLoader
from embeddings_generator import EmbeddingsGenerator
from vector_store import RAGVectorStore
from typing import List, Dict


class RAGPipeline:
    """
    Complete RAG pipeline for security threat analysis.
    
    This brings together all the pieces:
    - Knowledge base loading
    - Embeddings generation
    - Vector storage
    - Context retrieval
    """
    
    def __init__(self, rebuild: bool = False):
        """
        Initialize the RAG pipeline.
        
        Args:
            rebuild: If True, rebuild vector store from scratch
        """
        print("=" * 70)
        print("🚀 Initializing RAG Pipeline for Security Threat Prioritizer")
        print("=" * 70)
        
        # Initialize components
        self.kb_loader = KnowledgeBaseLoader()
        self.embeddings_gen = EmbeddingsGenerator()
        self.vector_store = RAGVectorStore()
        
        # Track if knowledge base is loaded
        self.kb_loaded = False
        
        # Rebuild if requested
        if rebuild:
            print("\n🔄 Rebuild mode: Will recreate vector store")
    
    def build_knowledge_base(self, force_rebuild: bool = False) -> None:
        """
        Build the complete knowledge base with embeddings.
        
        This loads all documents, generates embeddings, and stores them.
        Only needs to be run once (or when you update the knowledge base).
        
        Args:
            force_rebuild: If True, rebuild even if data already exists
        """
        print("\n" + "=" * 70)
        print("🏗️ Building Knowledge Base")
        print("=" * 70)
        
        # Check if already loaded
        current_count = self.vector_store.collection.count()
        if current_count > 0 and not force_rebuild:
            print(f"✅ Knowledge base already loaded ({current_count} documents)")
            print("   Use force_rebuild=True to rebuild from scratch")
            self.kb_loaded = True
            return
        
        # Step 1: Load knowledge base files
        print("\n📚 Step 1/3: Loading knowledge base files...")
        self.kb_loader.load_all()
        documents = self.kb_loader.get_all_documents()
        
        if not documents:
            print("❌ No documents found! Check your knowledge base files.")
            return
        
        # Step 2: Generate embeddings
        print("\n🤖 Step 2/3: Generating embeddings...")
        embedded_docs = self.embeddings_gen.embed_documents(documents)
        
        # Step 3: Store in vector database
        print("\n💾 Step 3/3: Storing in vector database...")
        
        if force_rebuild and current_count > 0:
            self.vector_store.clear_collection()
        
        embeddings = [doc['embedding'] for doc in embedded_docs]
        self.vector_store.add_documents(documents, embeddings)
        
        self.kb_loaded = True
        
        print("\n" + "=" * 70)
        print("✅ Knowledge Base Built Successfully!")
        print("=" * 70)
        stats = self.vector_store.get_stats()
        print(f"📊 Total documents indexed: {stats['total_documents']}")
        print(f"💾 Stored at: {stats['storage_path']}")
        print("=" * 70)
    
    def get_context_for_alert(self, alert_summary: str, top_k: int = 3) -> List[Dict]:
        """
        Get relevant security context for an alert.
        
        THIS IS THE MAIN FUNCTION Member 3 will use!
        
        Args:
            alert_summary: Description of the security alert
            top_k: Number of relevant documents to retrieve
            
        Returns:
            List of relevant CVE/MITRE/mitigation documents
            
        Example:
            >>> rag = RAGPipeline()
            >>> rag.build_knowledge_base()
            >>> context = rag.get_context_for_alert(
            ...     "Multiple failed SSH login attempts from external IP",
            ...     top_k=3
            ... )
            >>> # Returns top 3 most relevant security documents
        """
        if not self.kb_loaded and self.vector_store.collection.count() == 0:
            print("⚠️ Knowledge base not loaded! Run build_knowledge_base() first.")
            return []
        
        print(f"\n🔍 Searching for context: '{alert_summary[:60]}...'")
        
        # Use the vector store's search_by_text method
        results = self.vector_store.search_by_text(
            alert_summary,
            self.embeddings_gen,
            top_k=top_k
        )
        
        print(f"   ✅ Found {len(results)} relevant documents")
        
        return results
    
    def get_formatted_context(self, alert_summary: str, top_k: int = 3) -> str:
        """
        Get context as formatted text (ready for LLM).
        
        This returns a nicely formatted string that Member 3 can
        directly pass to the LLM for analysis.
        
        Args:
            alert_summary: Description of the security alert
            top_k: Number of documents to retrieve
            
        Returns:
            Formatted string with all relevant context
        """
        results = self.get_context_for_alert(alert_summary, top_k)
        
        if not results:
            return "No relevant security context found."
        
        # Format as text
        context_text = "RELEVANT SECURITY KNOWLEDGE:\n"
        context_text += "=" * 70 + "\n\n"
        
        for i, result in enumerate(results, 1):
            context_text += f"[Document {i} - Source: {result['source']}]\n"
            context_text += result['content']
            context_text += "\n\n" + "-" * 70 + "\n\n"
        
        return context_text
    
    def test_retrieval(self, query: str) -> None:
        """
        Test the RAG pipeline with a sample query.
        
        Useful for debugging and demonstrations.
        """
        print("\n" + "=" * 70)
        print("🧪 Testing RAG Retrieval")
        print("=" * 70)
        print(f"Query: '{query}'")
        print("=" * 70)
        
        context = self.get_formatted_context(query, top_k=3)
        print(context)


# Example usage
def main():
    """
    Full RAG pipeline demonstration.
    
    This shows the complete workflow from setup to retrieval.
    """
    print("=" * 70)
    print("🎯 RAG Pipeline - Full Demonstration")
    print("=" * 70)
    
    # Initialize pipeline
    rag = RAGPipeline()
    
    # Build knowledge base (only needed once)
    rag.build_knowledge_base()
    
    # Test with sample security alerts
    test_queries = [
        "Multiple failed login attempts detected on SSH port 22",
        "Suspicious SQL query with UNION SELECT statement",
        "Unexpected outbound data transfer to unknown IP address"
    ]
    
    print("\n" + "=" * 70)
    print("🔍 Testing Context Retrieval for Sample Alerts")
    print("=" * 70)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}/3: {query}")
        print('=' * 70)
        
        # Get context
        context_docs = rag.get_context_for_alert(query, top_k=2)
        
        # Show results
        for j, doc in enumerate(context_docs, 1):
            print(f"\n   📄 Result {j}:")
            print(f"   Source: {doc['source']}")
            print(f"   Preview: {doc['content'][:150]}...")
            if doc['distance'] is not None:
                similarity = 1 - doc['distance']
                print(f"   Similarity: {similarity:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ RAG Pipeline Test Complete!")
    print("=" * 70)
    print("\n💡 Next Step: Member 3 will use get_context_for_alert()")
    print("   to get relevant context for LLM threat analysis")
    print("=" * 70)


if __name__ == "__main__":
    main()
