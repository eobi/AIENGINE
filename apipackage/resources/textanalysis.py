from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from textanalysis.sentiments import engine as eng
# parser args
_text_parser = reqparse.RequestParser()
_text_parser.add_argument('textBody',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
_text_parser.add_argument('islarge',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )


class TextAnalysisResource(Resource):

    @jwt_required
    def get(self):
        data = _text_parser.parse_args()
        textBody = data["textBody"]
        if data["islarge"] == "1":
            response = eng.SentimentAnalysis.analzeLargeBody(textBody)
            return {"response": response}, 200

        response = eng.SentimentAnalysis.analyzesSmallBody(textBody)
        return {"response": response}, 200


