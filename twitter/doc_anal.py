#! /usr/bin/python3

import mysql.connector
import MeCab

def extract_keywords(text):
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text)
    keywords = []

    while node:
        if node.feature.split(',')[0] == u'名詞':
            keywords.append(node.surface)

        node = node.next

    word_count = {}

    word_list = list(set(keywords))
    for w in word_list:
        word_count[w] = keywords.count(w)

    return word_count


if __name__ == '__main__':
    text = "すもももももももものうち"
    print(extract_keywords(text))
