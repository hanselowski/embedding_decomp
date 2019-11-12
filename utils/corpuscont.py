# corpus operations

def store_corpus(corp, names, path):
    text_file = open(path, "w")
    cnt = 0
    for cc in corp:
        text_file.write(names[cnt]+':'+'\n')
        for c in cc:
            text_file.write(c+'\n')
        cnt += 1
    text_file.close()
    
def retrieve_corpus(path, lower_case = False):
    with open(path) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    cats, cat = [], []
    for row in content:
        if ":" in row and len(cat) > 0: 
            cats.append(cat)
            # print('')
            # print(cat)
            cat = []
        elif ":" not in row:
            # print(row)
            if lower_case:
                cat.append(row.lower())
            else:
                cat.append(row)
        cur_entry = row[0]
    cats.append(cat)
    return cats