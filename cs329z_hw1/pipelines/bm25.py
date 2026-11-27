import heapq
import math

from tqdm import tqdm

from cs329z_hw1.tokenizer import tokenize

class BM25_Index(): 
    def __init__(self, tokenizer, k1 = 1.5, b = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.tf_index = dict() # {term -> {doc_id, count}}
        self.avg_doc_length = 0
        self.docs_length = list() # hold the list of the length of each doc
        self.tokenizer = tokenizer
    
    def add_doc(self, docs): 
        for doc_i in tqdm(range(len(docs)), desc="Index doc"): 
            # Step 1. tokenize doc into tokens
            start_id = len(self.docs_length) # First id of the batch start from the last
            tokens = self.tokenizer(docs[doc_i])
            for token in tokens: 
                if token not in self.tf_index: 
                    self.tf_index[token] = {}
                # Step 2. for each token, update tf_index
                self.tf_index[token][start_id] = self.tf_index[token].get(start_id, 0) + 1
            self.docs_length.append(len(tokens))
            start_id +=1 # update doc id
        
        # Step 3. update avg_doc_length
        self.avg_doc_length = int(sum(self.docs_length) / len(self.docs_length))
        return self
    
    # calculate the idf of a certain token
    def _idf_lucence(self, token): 
        # ln ((N - n_t + 0.5)/(n_t + 0.5) + 1)
        N = len(self.docs_length)
        n_t = len(self.tf_index.get(token, {})) # number of times taken
        return math.log((N - n_t + 0.5)/(n_t + 0.5) + 1)        
    
    # calculate the tf of the token to a doc. 
    def _tf(self, token, doc_id): 
        idf_score = self._idf_lucence(token)
        f_t_f = self.tf_index.get(token, {}).get(doc_id, 0)
        doc_len_norm = 1-self.b+self.b*self.docs_length[doc_id]/self.avg_doc_length
        t_f_score = f_t_f*(self.k1+1) / (f_t_f+self.k1*doc_len_norm)
        return idf_score * t_f_score
    
    # calculate the bm25 score of the full query
    def _tf_query(self, query: str, doc_id): 
        query_tokens = self.tokenizer(query)
        checked_tokens = set()
        bm25_score = 0 
        for token in query_tokens: 
            if token not in checked_tokens: 
                bm25_score += self._tf(token, doc_id)
                checked_tokens.add(token)
        return bm25_score
    
    def search(self, query: str, k: int) -> list[tuple[int, float]]:
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
        score_dict = dict()
        for doc_i in range(len(self.docs_length)): 
            doc_i_score = self._tf_query(query, doc_id=doc_i)
            if doc_i_score != 0: 
                score_dict[doc_i] = doc_i_score
        top_k = heapq.nlargest(k, score_dict.items(), key=lambda score_dict: score_dict[1])
        return top_k
        
    
    
    

    
    