import face_recognition
import urllib.request
import random
import os


class FaceRecognition:

    def __init__(self, image_link):

        self.image_link = image_link

    @classmethod
    def InitAndCompare(cls,imageLink):

        # generate a random name for the downloaded image
        name = random.randrange(1, 1000000000)
        fullname = str(name) + ".jpg"

        # Load the known images
        image_of_person_1 = face_recognition.load_image_file("../imageanalysis/facerecognition/obi.jpg")
        image_of_person_2 = face_recognition.load_image_file("../imageanalysis/facerecognition/koku.jpg")
        image_of_person_3 = face_recognition.load_image_file("../imageanalysis/facerecognition/person_3.jpg")

        # Get the face encoding of each person. This can fail if no one is found in the photo.
        person_1_face_encoding = face_recognition.face_encodings(image_of_person_1)[0]
        person_2_face_encoding = face_recognition.face_encodings(image_of_person_2)[0]
        person_3_face_encoding = face_recognition.face_encodings(image_of_person_3)[0]

        # Create a list of all known face encodings
        known_face_encodings = [
            person_1_face_encoding,
            person_2_face_encoding,
            person_3_face_encoding
        ]

        urllib.request.urlretrieve(imageLink, fullname)

        # Load the image we want to check
        unknown_image = face_recognition.load_image_file(fullname)

        # Get face encodings for any people in the picture
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        # There might be more than one person in the photo, so we need to loop over each face we found

        for unknown_face_encoding in unknown_face_encodings:

            # Test if this unknown face encoding matches any of the three people we know
            results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance=0.6)

            name = "Unknown"

            if results[0]:
                name = "Obi Ebuka David"
            elif results[1]:
                name = "Adedotun Koku"
            elif results[2]:
                name = "Anita Joxy"

            FaceRecognition.deleteImageFile(fullname)
            return name


    @classmethod
    def deleteImageFile(cls,file):
        if os.path.exists(file):
            os.remove(file)
        else:
            print("The file does not exist")








