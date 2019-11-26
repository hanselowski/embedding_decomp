<img src="https://user-images.githubusercontent.com/29311022/27184688-27629126-51e3-11e7-9a23-276628da2430.png" height=70px/>
<img src="https://user-images.githubusercontent.com/29311022/27278631-2e19f99e-54e2-11e7-919c-f89ae0c90648.png" height=70px/>
<img src="https://user-images.githubusercontent.com/29311022/27184769-65c6583a-51e3-11e7-90e0-12a4bdf292e2.png" height=70px/>

## Repository for the paper: Analyzing Structures in the Semantic Vector Space: A Framework for Decomposing Word Embeddings



Link to the paper: [Analyzing Structures in the Semantic Vector Space: A Framework for Decomposing Word Embeddings](arxive/...)

Please use the following citation:
```
@inproceedings{hanselowski2019vedec,
          title={Analyzing Structures in the Semantic Vector Space: A Framework for Decomposing Word Embeddings},
          author={Hanselowski, Andreas and Gurevych, Iryna},
          booktitle={arxive/...},
          year={2019}
        }
```


Disclaimer:
> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.






### Download the word embeddings

Download pretrained GloVe Vectors
```bash
    wget http://nlp.stanford.edu/data/wordvecs/glove.6B.zip
    mkdir -p data/glove
    unzip glove.6B.zip -d data/glove
    gzip data/glove/*.txt
```
Download pretrained Word2Vec Vectors
```bash
    wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip
    mkdir -p data/word2vec
    
    wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec
    mkdir -p data/fasttext
    unzip wiki-news-300d-1M.vec.zip -d data/word2vec

```


### Run experiments

In order to run the experiments from the paper run the following jupyter botebooks: 



* Sem tree 

```bash
semantic_tree_model.ipynb
```

* Sem space networks

```bash
semantic_space_networks.ipynb
```

* Category completion

```bash
ssn_category_completion.ipynb
svm_category_completion.ipynb
```

* Word analogy

```bash
```




### Contacts:
  * hanselowski@gmail.com
  * https://www.informatik.tu-darmstadt.de/ukp/ukp_home/
  * https://www.tu-darmstadt.de    


### License:
  * Apache License Version 2.0

 

