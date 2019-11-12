import numpy as np
import operator

def length(v):
    return np.linalg.norm(v)

def unit(v):
    return v/length(v)

def cosine(a, b): 
    a_len = length(a)
    b_len = length(b)
    cos = np.dot(a, b)/(a_len*b_len)
    return cos

def find_sim(model, source, num):
    dist_dict = {}
    for i in range(100000):
        target_word = model.index2word[i]
        target = model[target_word]
        dist_dict[target_word] = np.dot(source, unit(target))
    sorted_keys = sorted(dist_dict.items(), key=operator.itemgetter(1))
    reversed_keys = reversed(sorted_keys)
    cnt = 0
    for k in reversed_keys:
        print(k)
        if cnt > num-2:
            break
        cnt += 1
    print('')
    return reversed_keys

def find_sim_cos(model, source, num):
    dist_dict = {}
    for i in range(100000):
        target_word = model.index2word[i]
        target = model[target_word]
        dist_dict[target_word] = cosine(source, unit(target))
    sorted_values = sorted(dist_dict.values())
    reversed_values = reversed(sorted_values)
    cnt = 0
    for v in reversed_values:
        print(list(dist_dict.keys())[list(dist_dict.values()).index(v)]+' '+str(v)) 
        if cnt > num-2:
            break
        cnt += 1
    print('')
    return reversed_values

def find_sim_cos(model, source, num, normalize = True):
    dist_dict = {}
    voc_size = 100000 # here change vocabulary size
    try: # handling differenence word2vec and other embeddings
        for i in range(voc_size):
            word = model.index2word[i]
            if normalize:
                instance = unit(model[word])
            else:
                instance = model[word]
            dist_dict[word] = cosine(source, instance)
    except:
        vocabulary = model.vocabulary.words
        for i in range(voc_size):
            if normalize:
                instance = unit(model[vocabulary[i]])
            else:
                instance = model[vocabulary[i]]
            dist_dict[vocabulary[i]] = cosine(source, instance)
    sorted_values = sorted(dist_dict.values())
    reversed_values = reversed(sorted_values)
    cnt = 0
    print(reversed_values)
    out_val = {}
    for v in reversed_values:
        key = list(dist_dict.keys())[list(dist_dict.values()).index(v)]
        val = str(v) 
        out_val[key] = val
        print(key+' '+val) 
        if cnt > num-2:
            break
        cnt += 1
    print('')
    return out_val        

def root_branches(dat):
    branchs = {}
    for i in range(len(dat)):
        for j in range(i+1, len(dat)):
            tree = Tree(model, [dat[i], dat[j]])
            branchs[str(i)+str(j)] = [tree.branches[0], tree.branches[1]]
    branchs_filt = []
    for i in range(len(dat)):
        branchs_tmp = []
        for k in branchs.keys():
            if   i == int(k[0]):
                branchs_tmp.append(branchs[k][0])
            elif i == int(k[1]):
                branchs_tmp.append(branchs[k][1])
        tree = Tree(model, dat[:2], vec_lst = branchs_tmp)     
        branchs_filt.append(tree.root)
    return branchs_filt 

def find_vecs(lst, model, normalize = False):
    print('support vectors:')
    sup_vecs = []  
    for w in lst: 
        if normalize:
            sup_vecs.append(unit(model[w]))
        else:
            sup_vecs.append(model[w])
        print(w)
    print('')
    return sup_vecs

def sort_disct(sup_vec_lens):
    sup_vec_sort = {}
    for key, value in sorted(sup_vec_lens.items(), key=lambda x:x[1]):
        sup_vec_sort[key] = value
    return sup_vec_sort

def min_proj_vec(a, b): 
    a_len = length(a)
    b_len = length(b)
    a_proj_vec = np.dot(a, b)/b_len
    b_proj_vec = np.dot(a, b)/a_len
    min_proj_vec = min(a_proj_vec,b_proj_vec)
    return min_proj_vec

def find_sim_set(source, lst, model, self_token):
    cos_dict = {}
    for w in lst:
        target = model[w]
        cos = cosine(source, target)
        cos_dict[w] = cos 
    cos_dict_sort = sort_disct(cos_dict)
    sorted_keys = list(cos_dict_sort.keys())
    sorted_values = list(cos_dict_sort.values())
    reversed_keys = reversed(sorted_keys)
    reversed_values = reversed(sorted_values)
    word = list(reversed_keys)[0]
    if list(reversed_values)[0] > 0.9 and not self_token==word:
        print('nearest vector in set: ')
        print(word)
    else:
        print('no match found')
    print('')
    
def hyper_test(v, h):
    cos = cosine(v, h)
    thresh = np.linalg.norm(h)
    v_proj = np.linalg.norm(v)*cos
    allowance = 0.000001 # hack to include support vectors 
    instance = 0
    if thresh - allowance < v_proj:
        instance = 1
    return instance

def find_insts(model, source, normalize = False, voc_size = 10000):
    print('instances of the source:')
    words = []
    try: # handling differenence word2vec and other embeddings
        for i in range(voc_size):
            word = model.index2word[i]
            if normalize:
                instance = unit(model[word])
            else:
                instance = model[word]
            sub_inst = hyper_test(instance, source)
            if sub_inst == 1:
                words.append(word)
    except:
        vocabulary = model.vocabulary.words
        for i in range(voc_size):
            if normalize:
                instance = unit(model[vocabulary[i]])
            else:
                instance = model[vocabulary[i]]
            
            sub_inst = hyper_test(instance, source)
            if sub_inst == 1:
                words.append(vocabulary[i]) 
                    
    len_dict = {}
    for w in words:
        if normalize:
            w_vec = unit(model[w])
        else:
            w_vec = model[w]
        inst_len = length(w_vec)
        cos = cosine(source, w_vec)
        inst_len_trunk = cos * inst_len
        len_dict[w] = inst_len_trunk
    sorted_keys = sorted(len_dict.items(), key=operator.itemgetter(1))
    reversed_keys = reversed(sorted_keys)
    
    cnt = 0
    lst_out = []
    for k in reversed_keys:
        print(k)
        lst_out.append(k[0].lower())
        if cnt > 1000:
            break
        cnt += 1
    print('')
    return lst_out

''' delete
def find_insts(model, source):
    print('instances of the source:')
    words = []

    try: # handling differenence word2vec and other embeddings
        for i in range(11000):
            word = model.index2word[i]
            instance = model[word]
            sub_inst = hyper_test(instance, source)
            if sub_inst == 1:
                words.append(word)
    except:
        vocabulary = model.vocabulary.words
        for i in range(11000):
            instance = model[vocabulary[i]]
            sub_inst = hyper_test(instance, source)
            if sub_inst == 1:
                words.append(vocabulary[i]) 
                    
    len_dict = {}
    for w in words:
        w_vec = model[w]
        inst_len = length(w_vec)
        cos = cosine(source, w_vec)
        inst_len_trunk = cos * inst_len
        len_dict[w] = inst_len_trunk
    sorted_keys = sorted(len_dict.items(), key=operator.itemgetter(1))
    reversed_keys = reversed(sorted_keys)
    cnt = 0
    lst_out = []
        
    for k in reversed_keys:
        # print(k)
        lst_out.append(k[0])
        if cnt > 1000:
            break
        cnt += 1
    print('')
    return lst_out

    
def find_insts_norm(model, source):
    print('instances of the source:')
    words = []

    try: # handling differenence word2vec and other embeddings
        for i in range(11000):
            word = model.index2word[i]
            instance = model[word]
            sub_inst = hyper_test(instance, source)
            if sub_inst == 1:
                words.append(word)
    except:
        vocabulary = model.vocabulary.words
        for i in range(11000):
            instance = model[vocabulary[i]]
            sub_inst = hyper_test(instance, source)
            if sub_inst == 1:
                words.append(vocabulary[i]) 
                
    len_dict = {}
    for w in words:
        w_vec = model[w]
        inst_len = length(w_vec)
        cos = cosine(source, w_vec)
        inst_len_trunk = cos * inst_len
        len_dict[w] = inst_len_trunk
    sorted_keys = sorted(len_dict.items(), key=operator.itemgetter(1))
    reversed_keys = reversed(sorted_keys)
    cnt = 0
    for k in reversed_keys:
        print(k)
        if cnt > 50:
            break
        cnt += 1
    print('')
'''