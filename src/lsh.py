import random



class LSH():

    def __init__(self, signature_length=100, band_size = 2):
        self.signature_length = signature_length
        self.band_size = band_size
        if signature_length % band_size != 0:
            raise ValueError("Signature length should be divisible by band_size")
        self.num_bands = signature_length // band_size
        


    def fit(self, samples : list[str]):
        shingles = self.create_shingles(samples)
        vocab, inv_vocab = self.create_vocab(shingles)
        one_hot_encoded_samples = self.one_hot_encode(shingles, vocab)
        self.minhashes = self.create_minhashes(len(vocab), self.signature_length)
        signatures = self.compress_to_signatures(one_hot_encoded_samples)
        self.hash_tables = self.create_bands_and_hash(signatures)
    
    def create_shingles(self, samples:list[str], shingle_length: int = 2) -> list[set[str]]:
        shingles = []
        for text in samples:
            sample_shingles = set()
            for start_pos in range(len(text) - shingle_length):
                sample_shingles.add(text[start_pos:shingle_length+start_pos])
            shingles.append(sample_shingles)
        return shingles


    def create_vocab(self, shingles: list[set[str]]) -> tuple[dict[str,int],dict[int, str]]:
        all_shingles = set().union(*shingles)
        vocab = {}
        inv_vocab = {}
        for i,shingle in enumerate(all_shingles):
            vocab[shingle] = i
            inv_vocab[i] = shingle
        return vocab, inv_vocab

    def one_hot_encode(self, shingle: set[str]|list[set[str]], vocab: dict[str,int]) -> list[int] | list[list[int]] :

        if isinstance(shingle, list):
            encoded_shigles = []
            for sample in shingle:
                encoded_shingle = self.__one_hot_encode_single(sample, vocab)
                encoded_shigles.append(encoded_shingle)
            return encoded_shigles
            
        elif isinstance(shingle, set):
            encoded_shingle = self.__one_hot_encode_single(shingle, vocab)
            return encoded_shingle
        else:
            raise TypeError("Wrong type, shigle should be set[str] | list[set[str]] got %s", type(shingle))


    def __one_hot_encode_single(self, shingle: set[str]|list[set[str]], vocab: dict[str,int]):
        encoded_shingle = [0]*len(vocab)
        for chunk in shingle:
            position = vocab[chunk]
            encoded_shingle[position] = 1
        return encoded_shingle

    
    
    def create_minhashes(self, vocab_size: int, signature_length: int) -> list[int]:
        minhashes = []
        for _ in range(signature_length):
            minhash = list(range(vocab_size))
            random.shuffle(minhash) 
            minhashes.append(minhash)
        return minhashes
    
    def compress_to_signatures(self, one_hot_encoded_samples: list[list[int]]) -> list[list[int]]:
        signatures = []  
        
        for sample in one_hot_encoded_samples:
            signature = []
            for minhash in self.minhashes:
                for idx in minhash:
                    if sample[idx] == 1:
                        signature.append(idx)
                        break
            signatures.append(signature)

        return signatures
    
    def create_bands_and_hash(self, signatures: list[list[int]]):
        
        # Create hash tables
        hash_tables = [{} for _ in range(self.num_bands)]
        
        for doc_id, signature in enumerate(signatures):
            # Split into bands and hash
            for band_num in range(self.num_bands):
                band = signature[band_num * self.band_size : (band_num + 1) * self.band_size]
                # No actual hashing since it is quite redudndant for python
                # Though we can hash the tuple here
                key = tuple(band)
                
                # Store in hash table
                hash_tables[band_num].setdefault(key, []).append(doc_id) 
        return hash_tables
                
    def find_candidates(self):
        candidates = set()
        
        for hash_table in self.hash_tables:
            for bucket in hash_table.values():
                # If more than one band hash is in the hash table -> match
                if len(bucket) > 1:  
                    for i in range(len(bucket)):
                        for j in range(i + 1, len(bucket)):
                            candidates.add(tuple(sorted([bucket[i], bucket[j]])))
        
        return candidates