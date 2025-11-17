# Embedding
this function receives multiple lists of models and scores them according to their frequency and their position in each list:
```Python
def score_models(*lists):
    from collections import defaultdict

    scores = defaultdict(lambda: {'frequency': 0, 'rank_sum': 0, 'ranked_counts': 0})

    for model_list in lists:
        for rank, model in enumerate(model_list, start=1):  # rank starts at 1
            scores[model]['frequency'] += 1
            scores[model]['rank_sum'] += rank
            scores[model]['ranked_counts'] += 1

    # Total score: higher frequency, lower average rank better
    # Normalize rank so higher score = better rank (invert rank)
    final_scores = {}
    for model, stat in scores.items():
        avg_rank = stat['rank_sum'] / stat['ranked_counts']
        # Final score example: freq_weight = 5, rank weight is inverse avg_rank
        freq_weight = 5
        final_scores[model] = stat['frequency'] * freq_weight + (8 - avg_rank)  # 8: one above worst rank

    return final_scores

# Example usage with your lists:
NeuCLIR2023_Retrieval = [
    "jinaai/jina-embeddings-v3",
    "Alibaba-NLP/gte-multilingual-base",
    "PartAI/Tooka-SBERT-V2-Small",
    "PartAI/Tooka-SBERT-V2-Large",
    "intfloat/multilingual-e5-large",
    "intfloat/multilingual-e5-base",
    "openai/text-embedding-3-large"
]

MIRACL_Retrieval = [
    "intfloat/multilingual-e5-large",
    "intfloat/multilingual-e5-base",
    "jinaai/jina-embeddings-v3",
    "Alibaba-NLP/gte-multilingual-base",
    "PartAI/Tooka-SBERT-V2-Large",
    "PartAI/Tooka-SBERT-V2-Small",
    "openai/text-embedding-3-large"
]

Wikipedia_Multilingual_Retrieval = [
    "intfloat/multilingual-e5-large",
    "jinaai/jina-embeddings-v3",
    "intfloat/multilingual-e5-base",
    "PartAI/Tooka-SBERT-V2-Large",
    "PartAI/Tooka-SBERT-V2-Small",
    "openai/text-embedding-3-large",
    "Alibaba-NLP/gte-multilingual-base"
]

mteb_leaderboard_dev = [
    "google/embeddinggemma-300m",
    "bge-m3",
    "jinaai/jina-embeddings-v3",
    "gte-Qwen2-7B-instruct",
    "intfloat/multilingual-e5-large",
    "intfloat/multilingual-e5-base",
    "e5-mistral-7b-instruct",
    "Hakim"
]

FaMTEB_Paper = [
	"bge-m3" ,
	"jinaai/jina-embeddings-v3" ,
	"Alibaba-NLP/gte-multilingual-base" ,
	"intfloat/multilingual-e5-large" ,
	"intfloat/multilingual-e5-base" ,
	"bge-m3-unsupervised" ,
	"Tooka-SBERT" ,
	"paraphrase-multilingual-MiniLM-L12-v2" ,
	"LaBSE" ,
	"faBert" ,
	"TookaBERT-Base" ,
	"BERT-WLNI" ,
	"RoBERTa-WLNI" ,
	"ParsBERT" ,
	"sentence-transformer-parsbert-fa" ,
]


scores = score_models(NeuCLIR2023_Retrieval, MIRACL_Retrieval, Wikipedia_Multilingual_Retrieval, mteb_leaderboard_dev, FaMTEB_Paper)
for model, score in sorted(scores.items(), key=lambda x: -x[1]):
    print(f"{model}: {score:.2f}")

```

FaMTEB Paper: 
```python


FaMTEB_DataSets = """
SynPerQARetrieval 20.36 26.59 25.02 42.94 24.95 52.45 53.99 26.88 65.02 77.44 85.59 87.35 85.14 86.27 85.4
SynPerChatbotTopicsRetrieval 2.38 3.52 4.23 0.05 0.15 12.28 6.2 0.16 10.76 28.07 15.37 11.82 10.59 19.18 18.75
SynPerChatbotRAGTopicsRetrieval 4.33 4.59 4.72 0.09 1.19 16.39 12.1 0.45 18.93 30.97 20.11 19.24 13.22 19.91 24.26
SynPerChatbotRAGFAQRetrieval 6.76 7.46 6.37 10.02 5.09 19.22 18.82 12.24 24.3 31.47 28.49 23.48 30.84 32.04 47.46
PersianWebDocumentRetrieval 12.61 8.14 12.55 7.95 10.04 14.31 28.21 10.85 43.9 44.15 46.72 46.76 38.18 44.09 40.32
NeuCLIR2022Retrieval 1.33 3.9 3.23 2.92 0.38 19.78 2.56 0.02 26.96 36.67 9.75 5.3 12.12 15.48 18.25
NeuCLIR2023Retrieval 6.6 5.27 5.02 12.1 1.86 26.34 21.52 4.63 36.47 50.93 46.1 46.67 46.53 52.2 51.45
WikipediaRetrievalMultilingual (fa) 35.63 37.34 41.29 63.67 48.41 62.15 67.06 46.14 79.02 84.94 88.11 90.4 91.19 89.32 89.02
MIRACLRetrieval (fa) 1.95 4.34 4.35 8.24 4.52 13.33 10.53 2.21 21.32 53.89 57.48 59.01 39.93 60.9 55.21
ClimateFEVER-Fa 1.13 2.68 2.15 5.06 2.05 12.23 3.73 0.39 9.47 18.83 12.6 12.75 16.41 24.31 29.87
FEVER-Fa 0.7 1.11 1.42 1.7 0.59 18 7 0.41 8.44 61.33 48.05 41.56 44.74 55.99 63.75
DBPedia-Fa 1.92 1.13 2.19 2.87 1.92 11.53 10.78 1.2 13.77 29.2 28.74 30.36 22.47 29.85 31.84
HotpotQA-Fa 0.22 0.85 0.85 6.52 3.37 12.39 11.94 2.33 16.44 49.04 55.33 60.15 39.24 56.54 51.43
MSMARCO-Fa 1.04 1.5 1.34 2.02 1.14 7.89 6.43 1.23 9.33 23.33 26.88 30.92 21.38 29.09 29.85
NQ-Fa 0.62 1.88 1.75 3.49 1.27 11.49 7.88 1.08 11.97 38.8 39.84 44.82 26.69 46.62 50.33
ArguAna-Fa 20.59 18.77 14.94 22.24 21.8 36.45 36.13 27.51 31.88 50.4 43.19 45.5 55.28 50.4 34.88
CQADupstackRetrieval-Fa 2.46 4.89 4.45 9.46 4.49 18.35 16.65 3.09 18.09 26.03 29.87 31.59 32.45 31.72 27.91
FiQA2018-Fa 0.87 2.61 2.22 3.1 1.58 10.31 6.35 1.82 11.22 26.47 23.17 30.15 27.39 30.38 34.43
NFCorpus-Fa 5.36 3.45 4 7.14 3.36 14.83 15.52 4.86 19.7 25.61 25.47 28.59 28.28 29.47 28.21
QuoraRetrieval-Fa 47.21 46.38 47.38 52.45 49.29 73.61 72.52 51.72 76.67 77.99 77.26 79.96 80.14 82.18 59.44
SCIDOCS-Fa 1.85 2.94 1.66 3.74 1.56 9.28 5.8 1.97 9.07 12.72 11.76 11.58 13.55 14.56 14.52
SciFact-Fa 5.95 6.48 7.75 18.86 10.33 31.54 34.57 13.54 37.19 56.15 57.79 59.69 57.76 60.52 61.51
Touche2020-Fa 1.44 7.04 5.46 2.14 1.14 16.47 4.59 1.42 13.22 24.69 22.48 26.19 16.15 22.87 26
"""

FaMTEB_Models = """
sentence-transformer-parsbert-fa
RoBERTa-WLNI
BERT-WLNI
faBert
ParsBERT
paraphrase-multilingual-MiniLM-L12-v2
LaBSE
TookaBERT-Base
Tooka-SBERT
Alibaba-NLP/gte-multilingual-base
intfloat/multilingual-e5-base
intfloat/multilingual-e5-large
bge-m3-unsupervised
bge-m3
jinaai/jina-embeddings-v3
"""


def parse_famteb_data(FaMTEB_DataSets, FaMTEB_Models):
    model_names = [name.strip()
                   for name in FaMTEB_Models.strip().split('\n') if name.strip()]
    table = []
    dataset_lines = [line.strip()
                     for line in FaMTEB_DataSets.strip().split('\n') if line.strip()]
    for line in dataset_lines:
        parts = line.split()
        # Skip tokens that aren't floats (like '(fa)')
        dataset = parts[0]
        scores = []
        for x in parts[1:]:
            try:
                scores.append(float(x))
            except ValueError:
                continue
        row = {'dataset': dataset}
        for mname, score in zip(model_names, scores):
            row[mname] = score
        table.append(row)
    return table, model_names


def calculate_average_accuracy(table, model_names):
    averages = {}
    for m in model_names:
        values = [row[m] for row in table if m in row]
        averages[m] = sum(values) / len(values)
    return averages


table, model_names = parse_famteb_data(FaMTEB_DataSets, FaMTEB_Models)
averages = calculate_average_accuracy(table, model_names)
ranking = sorted(averages.items(), key=lambda item: item[1])
ranking.reverse()

for i in ranking:
    print(i)

print("[")
for i in ranking:
    print(f'"{i[0]}" ,')
print("]")


```

```pwsh
('bge-m3', 42.77782608695652)
('jinaai/jina-embeddings-v3', 42.35173913043479)
('Alibaba-NLP/gte-multilingual-base', 41.70086956521739)
('intfloat/multilingual-e5-large', 40.16695652173913)
('intfloat/multilingual-e5-base', 39.13695652173913)
('bge-m3-unsupervised', 36.942173913043476)
('Tooka-SBERT', 26.65826086956522)
('paraphrase-multilingual-MiniLM-L12-v2', 22.635652173913044)
('LaBSE', 20.038260869565217)
('faBert', 12.555217391304348)
('TookaBERT-Base', 9.397826086956522)
('BERT-WLNI', 8.884347826086957)
('RoBERTa-WLNI', 8.82)
('ParsBERT', 8.716521739130433)
('sentence-transformer-parsbert-fa', 7.97)
[
"bge-m3" ,
"jinaai/jina-embeddings-v3" ,
"Alibaba-NLP/gte-multilingual-base" ,
"intfloat/multilingual-e5-large" ,
"intfloat/multilingual-e5-base" ,
"bge-m3-unsupervised" ,
"Tooka-SBERT" ,
"paraphrase-multilingual-MiniLM-L12-v2" ,
"LaBSE" ,
"faBert" ,
"TookaBERT-Base" ,
"BERT-WLNI" ,
"RoBERTa-WLNI" ,
"ParsBERT" ,
"sentence-transformer-parsbert-fa" ,
]
```
