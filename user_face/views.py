from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import json
from face_recognition import load_image_file, face_locations, face_encodings, face_distance
from .models import User
from .serializers import UserSerializer
from numpy import fromstring
# Create your views here.

class UserViewSet(ModelViewSet):
    serializer_class    = UserSerializer
    queryset            = User.objects.all()
    lookup_field        = 'id'

    def create(self, request):
        # print(request.body)
        try:
            form            = request.data
            user_id         = form['id']
            username        = form['username']
            user_img        = form['img']
            det_img         = load_image_file(user_img)
            face_location   = face_locations(det_img)
            print(face_location)
            if len(face_location)!=1:
                return Response('Please select an image with only the examinee present!', status=406)
            user_encoding   = face_encodings(det_img)[0]
            new_user        = User.objects.create(id=user_id, username=username, img=user_img, face_encoding=user_encoding)
            new_user.save()
            return Response('User image saved')
        except:
            return Response('An error occured, please try again later', status=404)

    def Update(self, request, pk=None):
        try:
            form                = request.data
            user_id             = form['id']
            username            = form['username']
            user_img            = form['img']
            det_img             = load_image_file(user_img)
            face_location       = face_locations(det_img)
            if len(face_location!=1):
                return Response('Please select an image with only the examinee present!', status=406)
            user_encoding       = face_encodings(det_img)[0]
            user                = User.objects.filter(id=pk)
            user.username       = username
            user.img            = user_img
            user.face_encoding  = user_encoding
            user.save()
            return Response('User image saved')
        except:
            return Response('An error occured, please try again later', staus=400)

    @action(detail=True, methods=['GET'])
    def recognize(self, request, id):
        try:
            form            = request.data
            user_id         = id
            image           = form['img']
            cur_user        = User.objects.get(id=user_id)
            det_img         = load_image_file(image)
            cur_encodings      = face_encodings(det_img)
            face_encoding   = cur_user.face_encoding[1:-1]
            face_encoding   = fromstring(face_encoding, dtype=float, sep=' ')
            known_face_encodings    = [
                    face_encoding
            ]
            faces           = []
            TOLERANCE       = 0.55
            for encoding in cur_encodings:
                face_distances  = face_distance(known_face_encodings, encoding)
                for dis in face_distances:
                    if dis<=TOLERANCE:
                        faces.append(user_id)
                    else:
                        faces.append('unknown')
            return Response({
                'num of faces': len(cur_encodings),
                'examinee_present': user_id in faces,
                'faces': faces,
            })
        except:
            return Response('An unexpected error occured, please try again later', status=400)
        
