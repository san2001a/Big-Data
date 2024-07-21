import random
from hazm import Normalizer, Stemmer, word_tokenize, stopwords_list
import itertools
import os

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[2:]  
    return [line.strip() for line in lines]

def preprocess_data(lines):
    preprocessed_lines = []
    stemmer = Stemmer()
    normalizer = Normalizer()
    for line in lines:
        normalized_text = normalizer.normalize(line)
        tokens = word_tokenize(normalized_text)
        tokens = [token for token in tokens if token not in stopwords_list()]
        tokens = [stemmer.stem(token) for token in tokens]
        preprocessed_lines.append(tokens)
    return preprocessed_lines

def split_data(data, split_ratio=0.8):
    split_index = int(len(data) * split_ratio)
    training_data = data[:split_index]
    testing_data = data[split_index:]
    return training_data, testing_data

def generate_candidates(data, itemset_size):
    candidates = set()
    for transaction in data:
        transaction_candidates = itertools.combinations(transaction, itemset_size)
        for candidate in transaction_candidates:
            candidates.add(frozenset(candidate))
    return candidates

def count_support(data, candidates):
    support_count = {}
    for transaction in data:
        for candidate in candidates:
            if candidate.issubset(transaction):
                support_count[candidate] = support_count.get(candidate, 0) + 1
    return support_count

def calculate_support(data, frequent_itemsets):
    support_counts = {}
    for transaction in data:
        for itemset in frequent_itemsets:
            if itemset in transaction:
                support_counts[itemset] = support_counts.get(itemset, 0) + 1
    return support_counts

def prune_infrequent(candidates, support_count, min_support, prev_support_counts=None):
    frequent_itemsets = set()
    for candidate in candidates:
        candidate_support = 0
        if prev_support_counts:
            for item in candidate:
                subset = candidate - frozenset([item])
                candidate_support += prev_support_counts.get(subset, 0)
        else:
            candidate_support = support_count[candidate]
        if candidate_support >= min_support:
            frequent_itemsets.add(candidate)
    return frequent_itemsets

def apriori_and_support(data, min_supports):
    frequent_itemsets = {}
    prev_support_counts = None
    max_itemset_size = max(min_supports.keys())
    for itemset_size, min_support in min_supports.items():
        if itemset_size > max_itemset_size:
            break
        candidates = generate_candidates(data, itemset_size)
        support_count = count_support(data, candidates)
        if prev_support_counts:
            frequent_itemsets_update = prune_infrequent(candidates, support_count, min_support, prev_support_counts)
        else:
            frequent_itemsets_update = prune_infrequent(candidates, support_count, min_support)
        if not frequent_itemsets_update:
            break
        frequent_itemsets[itemset_size] = frequent_itemsets_update
        prev_support_counts = support_count
    support_counts = calculate_support(data, frequent_itemsets)
    return frequent_itemsets, support_counts

def print_line_with_tokens(line, tokens):
    print("Original line:", line)
    print("Tokens:", tokens)
    print()

def average_support(support_counts):
    total_support = sum(support_counts.values())
    total_unique_words = len(support_counts)
    return total_support / total_unique_words

def count_word_occurrences(data):
    word_counts = {}
    for transaction in data:
        for word in transaction:
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def generate_association_rules(frequent_itemsets, support_counts, min_confidence, poet_name, itemset_size):
    association_rules = []
    itemsets = frequent_itemsets.get(itemset_size, set())
    for itemset in itemsets:
        rule_support = support_counts.get(itemset, None)
        if rule_support is None:
            # print(f"Support count not available for itemset {itemset}. Skipping...")
            continue
        for i in range(1, itemset_size):
            antecedents = itertools.combinations(itemset, i)
            for antecedent in antecedents:
                consequent = itemset.difference(antecedent)
                antecedent = frozenset(antecedent)
                consequent = frozenset(consequent)
                antecedent_support = support_counts.get(antecedent, None)
                if antecedent_support is None:
                    print(f"Support count not available for antecedent {antecedent}. Skipping...")
                    continue
                confidence = rule_support / antecedent_support
                if confidence >= min_confidence:
                    rule_text = f"Rule: {antecedent} => {consequent}, Confidence: {confidence}, Poet: {poet_name}"
                    association_rules.append(rule_text)
    return association_rules

def save_rules_to_file(association_rules, poet_name, output_folder):
    filename = f"{poet_name}_rules.txt"
    filepath = os.path.join(output_folder, filename)
    with open(filepath, "w") as file:
        for rule_text in association_rules:
            file.write(rule_text + "\n")
    print(f"Association rules for {poet_name} saved to {filepath}")

file1 = read_file('saadi.txt')
# file2 = read_file('rumi.txt')
# file3 = read_file('ferdousi.txt')
# file4 = read_file('hafez.txt')
# file4 = read_file('khayyam.txt')

random.shuffle(file1)
# random.shuffle(file2)
# random.shuffle(file3)
# random.shuffle(file4)
# random.shuffle(file5)

preprocessed_file1 = preprocess_data(file1)
# preprocessed_file2 = preprocess_data(file2)
# preprocessed_file2 = preprocess_data(file3)
# preprocessed_file2 = preprocess_data(file4)
# preprocessed_file2 = preprocess_data(file5)

training_data_file1, testing_data_file1 = split_data(preprocessed_file1)
# training_data_file2, testing_data_file2 = split_data(preprocessed_file2)
# training_data_file2, testing_data_file2 = split_data(preprocessed_file3)
# training_data_file2, testing_data_file2 = split_data(preprocessed_file4)
# training_data_file2, testing_data_file2 = split_data(preprocessed_file4)

# Example of one entry after preprocess
# print("saadi:")
# print_line_with_tokens(file1[0], preprocessed_file1[0])
# print("rumi:")
# print_line_with_tokens(file2[0], preprocessed_file2[0])

# support_counts_file1 = count_support(training_data_file1)
# support_counts_file2 = count_support(training_data_file2)
# support_counts_file3 = count_support(training_data_file3)
# support_counts_file4 = count_support(training_data_file4)
# support_counts_file4 = count_support(training_data_file5)

# Print all of the words with their supports
# print("Support Counts for saadi:", support_counts_file1)
# print("Support Counts for rumi:", support_counts_file2)

# Calculate average support for each dataset
# average_support_file1 = average_support(support_counts_file1)
# print("Average Support for saadi:", average_support_file1)
# average_support_file2 = average_support(support_counts_file2)
# print("Average Support for rumi:", average_support_file2)

# Number of words all over the file
# words_counts_file1 = count_word_occurrences(training_data_file1)
# all_word_counts_file1 = sum(1 for count in words_counts_file1.values() if count > 0)
# print("Number of words in saadi file:", all_word_counts_file1)
# words_counts_file2 = count_word_occurrences(training_data_file2)
# all_word_counts_file2 = sum(1 for count in words_counts_file2.values() if count > 0)
# print("Number of words in saadi file:", all_word_counts_file2)

# find freq items given the threshold
# min_support_threshold_saadi = 8
# words_with_min_support_file1 = sum(1 for count in words_counts_file1.values() if count >= min_support_threshold_saadi)
# print("Number of words in saadi file with support more than 8:", words_with_min_support_file1)
# min_support_threshold_rumi = 10
# words_with_min_support_file2 = sum(1 for count in words_counts_file2.values() if count >= min_support_threshold_rumi)
# print("Number of words in rumi file with support more than 10:", words_with_min_support_file2)

# min_supports = {1: 8, 2: 6} 
# frequent_itemsets, support_counts = apriori_with_support(training_data_file1, min_supports)
# print("Frequent Itemsets:", frequent_itemsets)

min_supports = {1: 10, 2: 8, 3: 6, 4: 4}

# Find frequent itemsets of sizes 1, 2, and 3
frequent_itemsets, support_counts = apriori_and_support(training_data_file1, min_supports)

# print("Frequent Itemsets (Size 1):", frequent_itemsets.get(1, set()))
# print("Frequent Itemsets (Size 2):", frequent_itemsets.get(2, set()))
# print("Frequent Itemsets (Size 3):", frequent_itemsets.get(3, set()))
# print("Frequent Itemsets (Size 4):", frequent_itemsets.get(4, set()))

# poem_files = {frozenset([word]): "saadismpl" for word in frequent_itemsets.get(1, set())}
# output_folder = "./"

# Example of a min confidence
min_confidence = 0.5
itemset_size = 2 
association_rules = generate_association_rules(frequent_itemsets, support_counts, min_confidence, 'saadi', itemset_size)
save_rules_to_file(association_rules, 'saadi', '/Users/sana/Desktop')
