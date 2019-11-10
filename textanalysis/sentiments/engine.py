from textblob import TextBlob


class SentimentAnalysis:

    text = ""
    response = []

    def __init__(self, text):
        self.text= text

    @classmethod
    def analyzesSmallBody(cls,text):
        response = []
        sentiment = TextBlob(text)
        item = {"item": text, "polarity_value": sentiment.polarity, "subjectivity_value": sentiment.subjectivity}
        response.append(item)
        return response

    @classmethod
    def analzeLargeBody(cls,text):

        # Import the movie reviews corpus
        with open("/Users/USER/PycharmProjects/AgiEngine/textanalysis/texttemp.txt", 'w+') as fh:
             fh.writelines(text)
             reviews = fh.readlines()
             print(reviews[:3])

        response = []
        for review in reviews:
            sentiment = TextBlob(review)
            item = {"item": review, "polarity_value": sentiment.polarity, "subjectivity_value":sentiment.subjectivity}
            response.append(item)

        for review in reviews:
            # Find sentiment of a review
            sentiment = TextBlob(review)
            # Print individual sentiments
            print('{:40} :   {: 01.2f}    :   {:01.2f}'.format(review[:40]
                                                               , sentiment.polarity, sentiment.subjectivity))
        return response



