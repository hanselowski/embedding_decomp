import numpy as np
import operator
from utils.methods import length, unit, cosine, find_vecs, sort_disct

class Tree:
    """Semantic tree class"""
        
    def __init__(self, model, word_lst, vec_lst = None, normalize = False):
        self.normalize = normalize
        if vec_lst == None: 
            self.vec_lst = find_vecs(word_lst, model, normalize)
            self.word_lst = word_lst
        else:
            self.vec_lst = vec_lst
            self.word_lst = word_lst
        
        self.model = model
        self.root()
        self.root_unit()
        self.find_branches()
        
    def root(self):
        v = self.model['dummy']
        H = [0]*v.shape[0]
        for vec in self.vec_lst:
            H = H + vec
        h_u = unit(H)

        sup_vec_lens = {}
        indzs = range(len(self.word_lst))
        for i in indzs: 
            w = self.word_lst[i]
            v = self.vec_lst[i]
            v_len = length(v)
            cos = cosine(v, H)
            h_len = v_len*cos
            sup_vec_lens[w] = h_len
        self.sup_vec_sort = sort_disct(sup_vec_lens)
        self.len = list(self.sup_vec_sort.values())[0]
        self.root = self.len * h_u
        
    def root_unit(self):
        v = self.model['dummy']
        H = [0]*v.shape[0]
        for vec in self.vec_lst:
            H = H + unit(vec)
        h_u = unit(H)

        sup_vec_lens = {}
        indzs = range(len(self.word_lst))
        for i in indzs: 
            w = self.word_lst[i]
            v = self.vec_lst[i]
            v_len = length(v)
            cos = cosine(v, H)
            h_len = v_len*cos
            sup_vec_lens[w] = h_len
        self.sup_vec_sort = sort_disct(sup_vec_lens)
        self.len = list(self.sup_vec_sort.values())[0]
        self.root = self.len * h_u
        
    def subvec_properties(self):
        output = 'sup. vec. order: '
        for key in self.sup_vec_sort.keys():
            val = sup_vec_sort[key]
            output = output + ' ' + key + ' ' + str(val) + '; '
        # print(output)
        
    def hyper_test(self, v, h):
        cos = cosine(v, h)
        thresh = np.linalg.norm(h)
        v_proj = np.linalg.norm(v)*cos
        allowance = 0.0000000001 # allowance to include support vectors 
        instance = 0
        if thresh - allowance < v_proj:
            instance = 1
        return instance
    
    def find_insts(self):
        print('instances of the source:')
        words = []
        voc_size = 11000 # here change vocabulary size
        try: # handling differenence word2vec and other embeddings
            for i in range(voc_size):
                word = self.model.index2word[i]
                if self.normalize:
                    instance = unit(self.model[word])
                else:
                    instance = self.model[word]
                sub_inst = self.hyper_test(instance, self.root)
                if sub_inst == 1:
                    words.append(word)
        except:
            vocabulary = model.vocabulary.words
            for i in range(voc_size):
                if self.normalize:
                    instance = unit(model[vocabulary[i]])
                else:
                    instance = model[vocabulary[i]]

                sub_inst = hyper_test(instance, self.root)
                if sub_inst == 1:
                    words.append(vocabulary[i]) 
                
        len_dict = {}
        for w in words:
            if self.normalize:
                w_vec = self.model[w]
            else:
                w_vec = unit(self.model[w])
            inst_len = length(w_vec)
            cos = cosine(self.root, w_vec)
            inst_len_root = cos * inst_len
            len_dict[w] = inst_len_root
        sorted_keys = sorted(len_dict.items(), key=operator.itemgetter(1))
        reversed_keys = reversed(sorted_keys)
        cnt = 0
        for k in reversed_keys:
            print(k)
            if cnt > 50:
                break
            cnt += 1
        print('')
        
    def find_branches(self):
        branches = []
        for v in self.vec_lst:
            branches.append(v - self.root)
        self.branches = branches
    
    def branch_instances(self, ind):
        vec = self.branches[ind]
        print('instances of the branch:', self.word_lst[ind])
        for i in range(11000):
            word = self.model.index2word[i]
            instance = self.model[word]
            sub_inst = self.hyper_test(instance, vec)
            if sub_inst == 1:
                print(word)
        print('')
        
    # public methods ------------------------------------------
    def find_hypernym(lst, model):
        sup_vecs = find_vecs(lst, model)
        h = Hypernym(model, sup_vecs)
        h.find_insts()
        find_sim(h.vec, model)
        return h
        
    def find_hyphypernym(lst_1, lst_2, model):
        sup_vecs = find_vecs(lst_1, model)
        h_1 = Hypernym(model, sup_vecs)

        sup_vecs = find_vecs(lst_2, model)
        h_2 = Hypernym(model, sup_vecs)

        sup_vecs = [h_1.root, h_2.root]
        h_super = Hypernym(model, sup_vecs)
        h_super.find_insts()

        find_sim(h_super.vec, model)
        find_sim(h_1.root - h_super.root, model)
        find_sim(h_2.root - h_super.root, model)
        
        return h_1, h_2, h_super
    
    