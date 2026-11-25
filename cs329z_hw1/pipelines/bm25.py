from cs329z_hw1.tokenizer import tokenize

def run_bm25_build(docs: list[str]):
    """Problem (bm25).

    Build and return a BM25 index over ``docs``. Document ids are list
    positions. Tokenize with ``cs329z_hw1.tokenizer.tokenize``. A document
    with no tokens is still a document (it counts in N and in the average
    length). The returned object is opaque to the tests; they only pass it
    back to ``run_bm25_search``. The index over the archive must build in
    under 15 seconds.
    """
    raise NotImplementedError


def run_bm25_search(index, query: str, k: int) -> list[tuple[int, float]]:
    """Problem (bm25).

    Return the top-k ``(doc_id, score)`` pairs for ``query`` as
    ``(int, float)`` tuples, best first, ties broken by lower doc_id (the
    document's position in the ``docs`` list given to ``run_bm25_build``).

    Rules the tests check:
    * Scores follow the handout's formula (k1 = 1.5, b = 0.75, Lucene IDF)
      to within 1e-6. The query is tokenized like the documents, and a term
      repeated in the query counts once.
    * A document that shares no term with the query is never returned, so
      the list may be shorter than k. A query with no tokens, or whose terms
      occur in no document, returns [].
    * A search reads only the index entries of the query's terms: 20 ms per
      query on average over the archive, and 2 ms for a term that occurs in
      3 of 200,000 documents.
    """
    raise NotImplementedError


class BM25_Index(): 
    def __init__(self, tokenizer, k1 = 1.5, b = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.tf_index = dict() # {term -> (doc_id, count)}
        self.avg_doc_length = 0
        self.docs = list()
        self.tokenizer = tokenizer
    
    def add_doc(self, docs): 
        
        for doc_i in range(len(docs)): 
            # Step 1. tokenize doc into tokens
            tokens = tokenize(docs[doc_i])
        
        # Step 2. for each token, update tf_index
        # Step 3. update avg_doc_length
        return self
    
    