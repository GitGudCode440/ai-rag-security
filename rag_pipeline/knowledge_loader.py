"""
Knowledge Base Loader
=====================
Simple script to load security knowledge from text files.

This module reads CVE, MITRE, and mitigation data for use in RAG pipeline.
"""

import os
from typing import List, Dict

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Knowledge base is one level up from rag_pipeline
KB_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "knowledge_base")


class KnowledgeBaseLoader:
    """
    Simple knowledge base loader for security documents.
    
    This class loads CVE, MITRE attack patterns, and mitigation strategies
    from text files and provides them in a structured format.
    """
    
    def __init__(self):
        """Initialize the knowledge base loader."""
        self.cve_data = []
        self.mitre_data = []
        self.mitigation_data = []
        
    def load_all(self):
        """
        Load all knowledge base files.
        
        This is the main function you'll call to load everything.
        """
        print("📚 Loading knowledge base...")
        
        # Load each type of data
        self.cve_data = self._load_file("cve_database.txt")
        print(f"  ✅ Loaded {len(self.cve_data)} CVE entries")
        
        self.mitre_data = self._load_file("mitre_attack_patterns.txt")
        print(f"  ✅ Loaded {len(self.mitre_data)} MITRE patterns")
        
        self.mitigation_data = self._load_file("mitigation_strategies.txt")
        print(f"  ✅ Loaded {len(self.mitigation_data)} mitigation strategies")
        
        print(f"📦 Total knowledge base entries: {self.get_total_count()}")
        
    def _load_file(self, filename: str) -> List[Dict[str, str]]:
        """
        Load a single knowledge base file.
        
        Args:
            filename: Name of the file to load from knowledge_base folder
            
        Returns:
            List of documents, each as a dictionary with 'content' and 'source'
        """
        filepath = os.path.join(KB_DIR, filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"  ⚠️ Warning: {filename} not found at {filepath}")
            return []
        
        documents = []
        
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by separator (---)
        entries = content.split('\n---\n')
        
        # Process each entry
        for i, entry in enumerate(entries):
            entry = entry.strip()
            if entry:  # Skip empty entries
                documents.append({
                    'content': entry,
                    'source': filename,
                    'id': f"{filename}_{i}"
                })
        
        return documents
    
    def get_all_documents(self) -> List[Dict[str, str]]:
        """
        Get all documents from all knowledge base files.
        
        Returns:
            Combined list of all CVE, MITRE, and mitigation documents
        """
        return self.cve_data + self.mitre_data + self.mitigation_data
    
    def get_cve_documents(self) -> List[Dict[str, str]]:
        """Get only CVE documents."""
        return self.cve_data
    
    def get_mitre_documents(self) -> List[Dict[str, str]]:
        """Get only MITRE attack pattern documents."""
        return self.mitre_data
    
    def get_mitigation_documents(self) -> List[Dict[str, str]]:
        """Get only mitigation strategy documents."""
        return self.mitigation_data
    
    def get_total_count(self) -> int:
        """Get total number of documents in knowledge base."""
        return len(self.cve_data) + len(self.mitre_data) + len(self.mitigation_data)
    
    def search_by_keyword(self, keyword: str) -> List[Dict[str, str]]:
        """
        Simple keyword search across all documents.
        
        Args:
            keyword: Word or phrase to search for (case-insensitive)
            
        Returns:
            List of documents containing the keyword
        """
        keyword = keyword.lower()
        results = []
        
        for doc in self.get_all_documents():
            if keyword in doc['content'].lower():
                results.append(doc)
        
        return results


# Example usage and testing
def main():
    """
    Test the knowledge base loader.
    
    This shows you how to use the KnowledgeBaseLoader class.
    """
    print("=" * 60)
    print("🔍 Knowledge Base Loader - Test Run")
    print("=" * 60)
    
    # Create loader instance
    kb = KnowledgeBaseLoader()
    
    # Load all data
    kb.load_all()
    
    print("\n" + "=" * 60)
    print("📊 Sample Data Preview")
    print("=" * 60)
    
    # Show first CVE entry
    if kb.get_cve_documents():
        print("\n🔴 Sample CVE Entry:")
        print("-" * 60)
        print(kb.get_cve_documents()[0]['content'][:200] + "...")
    
    # Show first MITRE pattern
    if kb.get_mitre_documents():
        print("\n🟠 Sample MITRE Pattern:")
        print("-" * 60)
        print(kb.get_mitre_documents()[0]['content'][:200] + "...")
    
    # Show first mitigation strategy
    if kb.get_mitigation_documents():
        print("\n🟢 Sample Mitigation Strategy:")
        print("-" * 60)
        print(kb.get_mitigation_documents()[0]['content'][:200] + "...")
    
    # Test keyword search
    print("\n" + "=" * 60)
    print("🔎 Testing Keyword Search: 'SQL'")
    print("=" * 60)
    results = kb.search_by_keyword("SQL")
    print(f"Found {len(results)} documents mentioning 'SQL'")
    
    print("\n✅ Knowledge base loaded successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
