import random



class LSH():

    def __init__(self, ):
        pass



    def fit(self, corpus : list[str]):
        shingles = self.create_shingles(corpus)
        vocab, inv_vocab = self.create_vocab(shingles)

        pass

    def create_shingles(self, corpus:list[str], shingle_length: int = 2) -> list[set[str]]:
        shingles = []
        for text in corpus:
            sample_shingles = set()
            for start_pos in range(len(text) - shingle_length):
                sample_shingles.add(text[start_pos:shingle_length+start_pos])
            shingles.append(sample_shingles)
        return shingles


    def create_vocab(self, shingles: list[set]) -> tuple[dict[str,int],dict[int, str]]:
        all_shingles = set().union(shingles)
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

    
    
    def create_minhash_order(self, vocab_size: int) -> list[int]:
        minhash_order = random.choice()
    