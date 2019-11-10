from flask_restful import Resource, reqparse
from imageanalysis.facerecognition import facerecognition as fr
from flask_jwt_extended import jwt_required

# parser args
_image_parser = reqparse.RequestParser()
_image_parser.add_argument('image_to_Check',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )


class FaceRecognitionResource(Resource):

    @jwt_required
    def post(self):
        data = _image_parser.parse_args()
        imageLink=data["image_to_Check"]
        #print(data["image_to_Check"])
        #imageLink = "https://firebasestorage.googleapis.com/v0/b/banking-4ad45.appspot.com/o/67159828_3019225004784429_359839897726484480_o.jpg?alt=media&token=9781fe64-fcee-4715-b656-3ef3880a745d"
        response = fr.FaceRecognition.InitAndCompare(imageLink)

        return {"username": response}, 200


