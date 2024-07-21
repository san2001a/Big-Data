import csv

def read_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def preprocess_data(data):
    transactions = []
    for row in data:
        transaction = set()
        for item in row:
            transaction.add(item)
        transactions.append(transaction)
    return transactions

def generate_candidate_itemsets(itemsets, k):
    candidates = set()
    for itemset1 in itemsets:
        for itemset2 in itemsets:
            union = itemset1.union(itemset2)
            if len(union) == k and len(itemset1.intersection(itemset2)) == k - 2:
                candidates.add(union)
    return candidates

def generate_frequent_itemsets(transactions, min_support):
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
        frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}
    frequent_itemsets = {frozenset([item]): count for item, count in frequent_items.items()}
    k = 2
    while True:
        candidates = generate_candidate_itemsets(frequent_itemsets.keys(), k)
        frequent_itemsets_k = {}
        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    if candidate in frequent_itemsets_k:
                        frequent_itemsets_k[candidate] += 1
                    else:
                        frequent_itemsets_k[candidate] = 1
        frequent_itemsets_k = {itemset: count for itemset, count in frequent_itemsets_k.items() if count >= min_support}
        if not frequent_itemsets_k:
            break
        frequent_itemsets.update(frequent_itemsets_k)
        k += 1
    
    return frequent_itemsets

def generate_pairs(frequent_itemsets):
    pairs = set()
    for itemset in frequent_itemsets:
        if len(itemset) == 2:
            pairs.add(itemset)
    return pairs

def generate_frequent_pairs(transactions, frequent_itemsets, min_support):
    pairs = generate_pairs(frequent_itemsets)
    frequent_pairs = {}
    for pair in pairs:
        count = 0
        for transaction in transactions:
            if pair.issubset(transaction):
                count += 1
        if count >= min_support:
            frequent_pairs[pair] = count
    return frequent_pairs

def generate_triples(frequent_pairs):
    triples = set()
    for pair1 in frequent_pairs:
        for pair2 in frequent_pairs:
            if pair1 != pair2 and pair1.intersection(pair2):
                triple = pair1.union(pair2)
                if len(triple) == 3:
                    triples.add(triple)
    return triples

def generate_frequent_triples(transactions, frequent_pairs, min_support):
    triples = generate_triples(frequent_pairs)
    frequent_triples = {}
    for triple in triples:
        count = 0
        for transaction in transactions:
            if triple.issubset(transaction):
                count += 1
        if count >= min_support:
            frequent_triples[triple] = count
    return frequent_triples

def confidence_based_top_rules(frequent_triples, frequent_itemsets):
    rules = []
    for triple, support in frequent_triples.items():
        A, B, C = triple
        AB = frozenset([A, B])
        AC = frozenset([A, C])
        BC = frozenset([B, C])
        try:
            confidence_AB_C = support / frequent_itemsets[AB]
        except KeyError:
            confidence_AB_C = 0
        try:
            confidence_AC_B = support / frequent_itemsets[AC]
        except KeyError:
            confidence_AC_B = 0
        try:
            confidence_BC_A = support / frequent_itemsets[BC]
        except KeyError:
            confidence_BC_A = 0
        
        # Append rules
        rules.append(((A, B), C, confidence_AB_C))
        rules.append(((A, C), B, confidence_AC_B))
        rules.append(((B, C), A, confidence_BC_A))
    
    # Sort rules based on confidence
    sorted_rules = sorted(rules, key=lambda x: x[2], reverse=True)
    return sorted_rules[:5]

def interest_based_top_rules(triples, frequent_itemsets, total_transactions):
    rules = []
    for triple, support in triples.items():
        A, B, C = triple
        AB = frozenset([A, B])
        AC = frozenset([A, C])
        BC = frozenset([B, C])
        try:
            confidence_AB_C = support / frequent_itemsets[AB]
        except KeyError:
            confidence_AB_C = 0
        try:
            confidence_AC_B = support / frequent_itemsets[AC]
        except KeyError:
            confidence_AC_B = 0
        try:
            confidence_BC_A = support / frequent_itemsets[BC]
        except KeyError:
            confidence_BC_A = 0
        
        transactions_with_C = sum(1 for transaction in transactions if C in transaction)
        transactions_with_B = sum(1 for transaction in transactions if B in transaction)
        transactions_with_A = sum(1 for transaction in transactions if A in transaction)
        
        interest_AB_C = confidence_AB_C - (transactions_with_C / total_transactions)
        interest_AC_B = confidence_AC_B - (transactions_with_B / total_transactions)
        interest_BC_A = confidence_BC_A - (transactions_with_A / total_transactions)
        
        # Append rules
        rules.append(((A, B), C, interest_AB_C))
        rules.append(((A, C), B, interest_AC_B))
        rules.append(((B, C), A, interest_BC_A))
    
    # Sort rules based on interest score
    sorted_rules = sorted(rules, key=lambda x: x[2], reverse=True)
    return sorted_rules[:5]

def lift_based_top_rules(frequent_triples, frequent_itemsets):
    rules = []
    for triple, support in frequent_triples.items():
        A, B, C = triple
        AB = frozenset([A, B])
        AC = frozenset([A, C])
        BC = frozenset([B, C])
        Ap = frozenset([A])
        Bp = frozenset([B])
        Cp = frozenset([C])
        
        try:
            lift_AB_C = support  / (frequent_itemsets[AB] * frequent_itemsets[Cp])
        except KeyError:
            lift_AB_C = 0
        try:
            lift_AC_B = support  / (frequent_itemsets[AC] * frequent_itemsets[Bp])
        except KeyError:
            lift_AC_B = 0
        try:
            lift_BC_A = support  / (frequent_itemsets[BC] * frequent_itemsets[Ap])
        except KeyError:
            lift_BC_A = 0
        
        # Append rules
        rules.append(((A, B), C, lift_AB_C))
        rules.append(((A, C), B, lift_AC_B))
        rules.append(((B, C), A, lift_BC_A))
    
    # Sort rules based on lift score
    sorted_rules = sorted(rules, key=lambda x: x[2], reverse=True)
    return sorted_rules[:5]


if __name__ == "__main__":
    min_support_items = 200
    min_support_pairs = 100
    min_support_triples = 75
    
    # Read the dataset
    data = read_data("store.csv")
    
    # Preprocess the data
    transactions = preprocess_data(data)
    
    # Generate frequent itemsets
    frequent_itemsets = generate_frequent_itemsets(transactions, min_support_items)
    
    # Sort and print the 10 most frequent items
    sorted_frequent_items = sorted(frequent_itemsets.items(), key=lambda x: x[1], reverse=True)[:10]
    print("10 most frequent items:")
    for itemset, support in sorted_frequent_items:
        print(f"{set(itemset)}: {support}")
    
    # Generate frequent pairs
    frequent_pairs = generate_frequent_pairs(transactions, frequent_itemsets, min_support_pairs)
    
    # Sort and print the 10 most frequent pairs of items
    sorted_frequent_pairs = sorted(frequent_pairs.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n10 most frequent pairs of items:")
    for pair, support in sorted_frequent_pairs:
        print(f"{set(pair)}: {support}")
    
    # Generate frequent triples
    frequent_triples = generate_frequent_triples(transactions, frequent_pairs, min_support_triples)
    
    # Sort and print the 10 most frequent triples of items
    sorted_frequent_triples = sorted(frequent_triples.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n10 most frequent triples of items:")
    for triple, support in sorted_frequent_triples:
        print(f"{set(triple)}: {support}")

    # Generate association rules based on confidence
    top_5_rules = confidence_based_top_rules(frequent_triples, frequent_itemsets)
    print('\n')
    print("Top 5 association rules based on confidence:")
    for rule in top_5_rules:
        antecedent, consequent, confidence = rule
        print(f"{antecedent} -> {consequent}: {confidence}")

    # Generate association rules based on interest
    total_transactions = len(transactions)
    top_5_rules_interest_new = interest_based_top_rules(frequent_triples, frequent_itemsets, total_transactions)
    print('\n')
    print("Top 5 association rules based on interest:")
    for rule in top_5_rules_interest_new:
        antecedent, consequent, interest = rule
        print(f"{antecedent} -> {consequent}: {interest}")

    # Generate association rules based on lift 
    total_transactions = len(transactions)
    top_5_rules_lift = lift_based_top_rules(frequent_triples, frequent_itemsets)
    print('\n')
    print("Top 5 association rules based on lift:")
    for rule in top_5_rules_lift:
        antecedent, consequent, lift = rule
        print(f"{antecedent} -> {consequent}: {lift}")

    print('\n')