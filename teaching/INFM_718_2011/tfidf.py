from dumbo import *
from math import log

def word_mapper(key, value):
    for word in value.split():
        yield (key, word), 1

@primary
def doc_total_mapper(key, value):
    doc = key[0]
    yield doc, value

@secondary
def doc_term_mapper(key, value):
    doc, word = key
    yield doc, (word, value)

@primary
def doc_freq_mapper(key, value):
    word = value[0]
    yield word, 1

@secondary
def term_freq_mapper(key, value):
    word = value[0]
    tf = value[1]
    doc = key
    yield word, (doc, tf)

class Reducer(JoinReducer):
    def __init__(self):
        self.sum = 0
    def primary(self, key, values):
        self.sum = sum(values)

class Combiner(JoinCombiner):
    def primary(self, key, values):
        yield key, sum(values)

class TermFrequencyReducer(Reducer):
    def secondary(self, key, values):
        for (doc, n) in values:
            yield key, (doc, float(n) / self.sum)

class TfIdfReducer(Reducer):
    def __init__(self):
        Reducer.__init__(self)
        self.doccount = float(self.params["doccount"])
    def secondary(self, key, values):
        idf = log(self.doccount / self.sum)
        for (doc, tf) in values:
            yield (key, doc), tf * idf

def runner(job):
    job.additer(word_mapper, sumreducer, combiner=sumreducer)
    multimapper = MultiMapper()
    multimapper.add("", doc_total_mapper)
    multimapper.add("", doc_term_mapper)
    job.additer(multimapper, TermFrequencyReducer, Combiner)
    multimapper = MultiMapper()
    multimapper.add("", doc_freq_mapper)
    multimapper.add("", term_freq_mapper)
    job.additer(multimapper, TfIdfReducer, Combiner)
if __name__ == "__main__":
    main(runner)
