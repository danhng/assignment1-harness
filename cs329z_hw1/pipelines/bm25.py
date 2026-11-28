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
        self.idf_cache = {}
        self.docs_length_norm = {}
    
    def add_doc(self, docs): 
        # todo reset caches
        self.idf_cache = {}
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
        self.avg_doc_length = math.ceil(sum(self.docs_length) / len(self.docs_length))
        
        # Step 4: Update doc length norm cache
        for doc_i in range(len(docs)):
            self.docs_length_norm[doc_i] = 1-self.b+self.b*self.docs_length[doc_i]/self.avg_doc_length
        return self
    
    # calculate the idf of a certain token
    def _idf_lucence(self, token): 
        if (token in self.idf_cache): 
            return self.idf_cache[token]
        # ln ((N - n_t + 0.5)/(n_t + 0.5) + 1)
        N = len(self.docs_length)
        n_t = 0
        if token in self.tf_index: 
            n_t = len(self.tf_index[token]) # number of times taken
        idf_score = math.log((N - n_t + 0.5)/(n_t + 0.5) + 1)        
        self.idf_cache[token] = idf_score
        return idf_score
    
    # calculate the tf of the token to a doc. 
    def _tf(self, token, doc_id): 
        # if self.avg_doc_length == 0:
        #   return 0
        # if ((token, doc_id) in self.tf_cache): 
            # return self.tf_cache[(token, doc_id)]
        idf_score = self._idf_lucence(token)
        f_t_f = self.tf_index.get(token, {}).get(doc_id, 0)
        doc_len_norm = self.docs_length_norm[doc_id]
        t_f_score = f_t_f*(self.k1+1) / (f_t_f+self.k1*doc_len_norm)
        return idf_score * t_f_score
        # self.tf_cache[(token, doc_id)] = score
    
    # calculate the bm25 score of the full query
    def _tf_query(self, tokens, doc_id): 
        checked_tokens = set()
        bm25_score = 0 
        for token in tokens: 
            if token not in checked_tokens: 
                bm25_score += self._tf(token, doc_id)
                checked_tokens.add(token)
        return bm25_score
    
    def _get_relevant_docs(self, tokens): 
        docs = set()
        for token in tokens: 
          docs.update(set(self.tf_index.get(token, {})))
        return docs
      
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
        tokens = self.tokenizer(query)
        # for doc_i in self._get_relevant_docs(tokens): 
        #     doc_i_score = self._tf_query(tokens, doc_id=doc_i)
        #     if doc_i_score != 0: 
        #         score_dict[doc_i] = doc_i_score
        # top_k = heapq.nlargest(k, score_dict.items(), key=lambda score_dict: (score_dict[1], -1 * score_dict[0]))
        
        for token in tokens: 
            for doc_id in self.tf_index.get(token, {}).keys():
                checked_tokens = set()
                if token not in checked_tokens: 
                    tf_score_token = self._tf(token, doc_id)
                    if tf_score_token != 0:
                        score_dict[doc_id] = score_dict.get(doc_id, 0) + tf_score_token
                    checked_tokens.add(token)
        top_k = heapq.nlargest(k, score_dict.items(), key=lambda score_dict: (score_dict[1], -1 * score_dict[0]))
        return top_k
        
    
    
    

    
    