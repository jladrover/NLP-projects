import operator
from collections import defaultdict

def merge_pos(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as output:
        for line in f1:
            output.write(line)
        for line in f2:
            output.write(line)

def generate_output_file(output):
    with open("submission.pos", "w") as f:
        for line in output:
            if line[0] == "":
                f.write("\n")
            else:
                f.write(f"{line[0]}\t{line[1]}\n")
   
def max_prob(pos, probability, prev_tag, prob_map):
    key = (prev_tag, pos)
    prior_prob = prob_map.get(pos, {}).get(key, 1.0)
    combined_prob = probability * prior_prob
    return [pos, combined_prob]

def system():
    count_map, likelihood_map = defaultdict(int), {}
    total_words = 0

    with open("combined_corpus.pos") as file1:
        for line in file1:
            parts = line.strip().split("\t")
            if len(parts) <= 1:
                continue

            word, pos = parts
            count_map[pos] += 1
            total_words += 1

        for pos, count in count_map.items():
            likelihood_map[pos] = count / total_words


    count_pos_map = defaultdict(lambda: defaultdict(int))
    likelihood_words_map = {}

    with open("combined_corpus.pos") as file1:
        for line in file1:
            parts = line.strip().split("\t")
            if len(parts) <= 1:
                continue
            word, pos = parts
            count_pos_map[word][pos] += 1

    for word, pos_counts in count_pos_map.items():
        total_counts = sum(pos_counts.values())
        likelihoods = {pos: count / total_counts for pos, count in pos_counts.items()}
        if len(likelihoods) == 1:
            likelihood_words_map[word] = {next(iter(likelihoods.keys())): 1.0}
        else:
            likelihood_words_map[word] = likelihoods

    bigram_count_map = defaultdict(int)
    bigram_prob_map = {}

    with open("combined_corpus.pos", "r") as file1:
        lines = file1.read().splitlines()
        total_bigrams = 0

        for curr_line, next_line in zip(lines, lines[1:]):
            curr_parts, next_parts = curr_line.split("\t"), next_line.split("\t")
            if len(curr_parts) < 2 or len(next_parts) < 2:
                continue

            current_pos, next_pos = curr_parts[1], next_parts[1]
            bigram_count_map[(current_pos, next_pos)] += 1
            total_bigrams += 1

    for b, count in bigram_count_map.items():
        bigram_prob_map[b] = count / total_bigrams

    prev_map = {} # prev pos probability map
    for key, value in bigram_prob_map.items():
        if key[1] not in prev_map: # checking if curr pos in map
            prev_map[key[1]] = {}
            for k, v in bigram_prob_map.items():
                if k[1] == key[1]:
                    prev_map[key[1]][k] = v

    with open("WSJ_23.words", "r+") as f:
        lines = [line.rstrip() for line in f]

    output = []
    if lines:
        highest_prob_first = max(likelihood_map.items(), key=operator.itemgetter(1))[0]
        output.append([lines[0], highest_prob_first])
    for word in lines[1:]:
        try:
            word_pos = list(likelihood_words_map.get(word, {}).items())

            if len(word_pos) == 1:
                output.append([word, word_pos[0][0]])
                continue

            prev_pos_tag = output[-1][1]
            phrase = (None, 0) 
            pos_candidates = word_pos if word_pos else likelihood_map.items()

            for pos, val in pos_candidates:
                maximum = max_prob(pos, val, prev_pos_tag, prev_map)
                if maximum[1] > phrase[1]:
                    phrase = maximum
            output.append([word, phrase[0]])

        except KeyError:
            prev_pos_tag = output[-1][1]
            max_val, phrase = 0, []

            for k, v in likelihood_map.items():
                maximum = max_prob(k, v, prev_pos_tag, prev_map)
                if maximum[1] > max_val:
                    max_val = maximum[1]
                    phrase = maximum

            output.append([word, phrase[0]])

    generate_output_file(output)

merge_pos("WSJ_02-21.pos", "WSJ_24.pos", "combined_corpus.pos") #for final system
system()