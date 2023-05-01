

# Define helper functions
def correct_sentence_spelling(sentence_words):
    corrected_words = [spell.correction(word) for word in sentence_words]
    return corrected_words

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = correct_sentence_spelling(sentence_words)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

ERROR_THRESHOLD = 0.25

def find_most_similar_question(query, threshold=0.8):
    query_embedding = sbert_model.encode(query)
    max_similarity = 0
    most_similar_question = None

    for intent in physics['intents']:
        for question in intent['patterns']:
            question_embedding = sbert_model.encode(question)
            similarity = np.inner(query_embedding, question_embedding)

            if similarity > max_similarity and similarity >= threshold:
                max_similarity = similarity
                most_similar_question = question

    return most_similar_question

def classify(sentence):
    most_similar_question = find_most_similar_question(sentence)
    if most_similar_question is not None:
        results = model.predict([bow(most_similar_question, words)])[0]
    else:
        results = model.predict([bow(sentence, words)])[0]

    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    if results:
        while results:
            for i in physics['intents']:
                if i['tag'] == results[0][0]:
                    return random.choice(i['responses'])
            results.pop(0)
    return None

model.load("model.tflearn")