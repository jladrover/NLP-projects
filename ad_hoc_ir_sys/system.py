import nltk, string
import re, math
nltk.download('punkt')
nltk.download('stopwords')
from collections import defaultdict, Counter
from nltk.stem.porter import *


#brought stop words from stop_words.py
stop_words_closed = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or']

def calc_feature_vectors(filtered_queries):
    doc_frequency = defaultdict(int)
    query_vectors, total_queries = [], len(filtered_queries)

    for query in filtered_queries:
        unique_terms = set(term.lower() for term in query)
        for term in unique_terms:
            doc_frequency[term] += 1
    
    for query in filtered_queries: # calc TFIDF for each query
        term_tf_idf = defaultdict(float)
        for term in query:
            normalized_term = term.lower()
            term_count = query.count(normalized_term)
            tf = term_count / len(query)  
            idf = math.log(total_queries / (doc_frequency[normalized_term] + 1))  
            tf_idf_score = tf * idf
            term_tf_idf[normalized_term] = round(tf_idf_score, 3)  
        
        query_vector = [term_tf_idf[term.lower()] for term in query if term.lower() in term_tf_idf]
        query_vectors.append(query_vector)

    return query_vectors

def calc_doc_vectors(clean_abstracts, clean_queries):
    abstract_tfidf_score = []
    word_map = Counter()

    for abstract in clean_abstracts:
        word_map.update(term.lower() for term in abstract)
    word_map = dict(word_map)

    for abstract in clean_abstracts:
        abstract_tfidf_score.append(defaultdict(int))
        match = []

        for a in abstract:
            if a.lower() not in match:
                match.append(a.lower())
                abstract_tfidf_score[-1][a.lower()] = 1
            else:
                abstract_tfidf_score[-1][a.lower()] += 1
            tf = float(abstract_tfidf_score[-1][a.lower()])/float(len(abstract))
            idf = math.floor(math.log(1400 / float(word_map[a.lower()])) * 1000) / 1000
            abstract_tfidf_score[-1][a.lower()] = math.floor(idf * tf * 1000) / 1000

    stemmer = PorterStemmer()
    query_feature_vectors = []
    for query in clean_queries:
        query_vector = []
        for abstract_tfidf in abstract_tfidf_score:
            abstract_vector = []
            for term in query:
                stemmed_term = stemmer.stem(term)
                tfidf_score = abstract_tfidf.get(term, abstract_tfidf.get(stemmed_term, 0))
                abstract_vector.append(tfidf_score)
            query_vector.append(abstract_vector)
        query_feature_vectors.append(query_vector)

    return query_feature_vectors
    

def calc_cosine_sim(query, abstract): # b representing queries
    ab, b_mag, a_mag = 0, 0, 0
    for b, a in zip(query, abstract):
        if a is not None:
            ab += (b*a)
            b_mag, a_mag = b_mag + b ** 2, a_mag + a ** 2

    b_mag, a_mag = math.sqrt(b_mag), math.sqrt(a_mag)
    if b_mag * a_mag != 0:
        cosine_similarity = math.floor(ab / (a_mag*b_mag) * 1000) / 1000
    else:
        cosine_similarity = 0

    return cosine_similarity

def get_abstracts(f):
    abstracts, reached_abstract = [], False
    abs_stem = []
    for q in f:
        if q[:2] in ['.I']: 
            abstracts.append(abs_stem)
            abs_stem, reached_abstract = [], False
        elif q[:2] in ['.W']:
            reached_abstract = True
        elif reached_abstract:
            tokens = nltk.word_tokenize(q)
            for t in tokens:
                if t not in stop_words_closed:
                    abs_stem.append(t)
    return abstracts


def main():
    file1, file2 = open("./cran_data/cran.qry", "r"), open("./cran_data/cran.all.1400", "r")
    qry_content = file1.read()
    filtered_queries, sentences = [], nltk.word_tokenize(qry_content)
    for word in sentences:
        if word.isdigit() and len(word) == 3 and word not in string.punctuation:
            filtered_queries.append([])
        elif not re.search(r'\d|\W', word) and word not in string.punctuation:
            filtered_queries[-1].append(word)

    qry_vec = calc_feature_vectors(filtered_queries)
    processed_abstracts = get_abstracts(file2)
    abst_vec = calc_doc_vectors(processed_abstracts, filtered_queries) #

    similarity_results = []
    for query_idx, single_qry in enumerate(qry_vec): # calc cosine similarity between query/abstract vectors
        similarity_results.append([])
        for abst_idx, single_abst in enumerate(abst_vec[query_idx]):
            cos_sim = calc_cosine_sim(single_qry, single_abst)
            if cos_sim != 0:
                similarity_results[-1].append([query_idx, abst_idx, cos_sim])

    sorted_similarities = []
    for sim_list in similarity_results: # sort results based on similarity scores
        sim_list.sort(key=lambda x: x[2], reverse=True)
        sorted_similarities.append(sim_list)
        with open('output.txt','w') as output:
            for list in sorted_similarities: 
                for t in list:                 
                    query, abstract, cosine_similarity_score = 1 + t[0], 1 + t[1], t[2]
                    output.write(f"{query} {abstract} {cosine_similarity_score}\n")

main()