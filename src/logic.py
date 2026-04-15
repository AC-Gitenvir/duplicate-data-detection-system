import hashlib
from rapidfuzz import fuzz

def preprocess(df):
    df = df.fillna("")
    return df.astype(str)

def find_exact_duplicates(df):
    df = preprocess(df)

    df['hash'] = df.apply(
        lambda row: hashlib.md5(''.join(row.values).encode()).hexdigest(),
        axis=1
    )

    return df[df.duplicated('hash', keep=False)]

def find_fuzzy_duplicates(df, threshold=85):
    df = preprocess(df)

    records = df.apply(lambda row: ' '.join(row.values), axis=1).tolist()
    results = []

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            score = fuzz.ratio(records[i], records[j])
            if score > threshold:
                results.append((records[i], records[j], score))

    return results

def remove_duplicates(df):
    df = preprocess(df)
    return df.drop_duplicates()