# coding: utf-8
import json
import re

file = open("ry_tweets.json")
tweets = json.load(file)
file.close()

N = 5
counts = {"tweet":0, "ry":0, "last_ry":0, "sentence":0}
ngrams = {}
for i in range(1, N+1):
    ngrams[i] = {}

def get_ry_index(text):
    indices = []
    for i in range(0, len(text)):
        if text[i:i+3] != "(ry":
            continue

        indices.append(i)
        counts["ry"] += 1
        if i+3 == len(text):
            counts["last_ry"] += 1
        elif text[i+3] in [" ", ".", "#", "【", "」","　","｣", "←", "…"] or i+4 == len(text) or i+5 == len(text):
            counts["last_ry"] += 1
        # else:
        #     print(text)

    return indices

def count_ngrams (text, indices):
    for index in indices:
        for i in range(1, N+1):
            if index-i < 0:
                break
            chars = text[index-i:index]
            if chars in ngrams[i]:
                ngrams[i][chars] += 1
            else:
                ngrams[i][chars] = 1

def analysis_sentences(tweets):
    for tweet in tweets:
        counts["tweet"] += 1
        sentences = tweet["text"].split("\n")
        for sentence in sentences:
            text = re.sub(r'\(+ry', '(ry', sentence)
            counts["sentence"] += 1

            ry_indices = get_ry_index(text)
            count_ngrams(text, ry_indices)

analysis_sentences(tweets)

output_count = 20
output = [""] * output_count
for i in range(1, N+1):
    count = 0
    print("**************", i, "**************")
    for chars, num in sorted(ngrams[i].items(), key=lambda x:x[1], reverse=True):
        # print(chars, num)
        output[count] += "|" + chars + "(ry|" + str(num)
        count += 1
        if count > output_count - 1:
            break

for key, value in counts.items():
    print(key, value)

# for line in output:
#     print(line + "|")
