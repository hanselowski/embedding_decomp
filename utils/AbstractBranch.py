import numpy as np
import operator
from utils.Methods import length, unit, cosine, find_vecs, sort_disct, find_sim_cos, find_insts
from utils.Tree import Tree

def findIndx(alst, blst):
    olst = []
    for a in alst:
        record = 1 
        for b in blst:
            if a == b:
                record = 0
        if record:
            olst.append(a)
            
    for b in blst:
        record = 1 
        for a in alst:
            if a == b:
                record = 0
        if record:
            olst.append(b)
    return olst  

def abstractBranches(model, vec):

    print('abstractBrances start')
    # git binary trees
    roots = []
    ind1 = []
    for i in range(len(vec)):
        for j in range(i+1,len(vec)):
            ind1.append([i,j])
            # print([i,j])
            tree_obj = Tree(model, [vec[i], vec[j]], [unit(model[vec[i]]), unit(model[vec[j]])])
            roots.append(tree_obj.root)

    # get binary trees of binary trees 
    print('get binary trees of binary trees ')
    trees = []
    tree_roots = []
    ind2 = []
    names = []
    for i in range(len(roots)):
        for j in range(i+1,len(roots)):   
            cur_ind = findIndx(ind1[i], ind1[j])

            if len(cur_ind) < 3:
                tree_obj = Tree(model, ['root1', 'root2'], [roots[i], roots[j]])
                trees.append(tree_obj)
                tree_roots.append(tree_obj.root)
                ind2.append(cur_ind)
                names.append(str(cur_ind[0])+'_'+str(cur_ind[1]))
                
    # add up the branches and compute the average abstract barnch
    print('compute branches')
    branches = []
    for i in range(len(vec)):
        key_pos = []
        biv = []
        for l in range(len(ind2)):
            for j in range(len(ind2[l])): # length should be two anyway
                if i == ind2[l][j]:
                    key_pos.append(l)
                    biv.append(j)
                        
        # print('next summation: ')
        sum_vec = np.zeros(len(model[vec[0]]))
        for l in range(len(key_pos)):
            sum_vec = sum_vec + trees[key_pos[l]].branches[biv[l]]

        branches.append(sum_vec/len(key_pos))
    root_out = Tree(model, names, tree_roots)
    return root_out, branches

def root_branches(model, dat):
    """
    Method to identify abstract branches
    """
    print('dat',dat)
    branchs = {}
    for i in range(len(dat)):
        for j in range(i+1, len(dat)):
            tree = Tree(model, [dat[i], dat[j]], [model[dat[i].lower()], model[dat[j].lower()]])
            branchs[str(i)+' '+str(j)] = [tree.branches[0], tree.branches[1]]
    branchs_filt = []

    for i in range(len(dat)):
        branchs_tmp = []
        for k in branchs.keys():
            key_lst = k.split(' ')
            if   i == int(key_lst[0]):
                branchs_tmp.append(branchs[k][0])
            elif i == int(key_lst[1]):
                branchs_tmp.append(branchs[k][1])

        tree = Tree(model, dat[:len(branchs_tmp)], branchs_tmp) 
        branchs_filt.append(tree.root)

    return branchs_filt
