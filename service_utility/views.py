from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from service_utility.serializers import GroupSerializers


UTI = ['hs048','shs500','shw929','hendras']

@api_view(['GET','POST'])
def group_list(request):
    if request.user.username in UTI:
        if request.method == "GET":
            group = Group.objects.all()
            serializer = GroupSerializers(group, many=True)
            content = {
				'message':'success',
				'records':group.count(),
				'rows':serializer.data
			}
            status_code = status.HTTP_200_OK
        elif request.method == "POST":
            serializer = GroupSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                content = {
                    'message':'success',
                    'rows':serializer.data
                }
                status_code = status.HTTP_201_CREATED
            else:
                content = {
                    'message':'success',
                    'rows':serializer.errors
                }
                status_code = status.HTTP_400_BAD_REQUEST
    else:
        content = {
			'message':'anda tidak berhak untuk mengakses funsi ini',
		}
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(content, status_code)


@api_view(['GET','PUT','DELETE'])
def group_detil(request, name):
    if request.user.username in UTI:
        try:
            group = Group.objects.get(name=name)
        except Group.DoesNotExist:
            content = {
                'message' : 'data not found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = GroupSerializers(group)
            content = {
				'message':'success',
				'rows':serializer.data
			}
            status_code = status.HTTP_200_OK

        elif request.method == "PUT":
            serializer = GroupSerializers(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                content = {
                    'message':'success change data',
				    'rows':serializer.data
                }
                status_code = status.HTTP_200_OK
            else:
                content = {
                    'message':'success change data',
				    'rows':serializer.errors
                }
                status_code = status.HTTP_400_BAD_REQUEST
        elif request.method == "DELETE":
             group.delete()
             content = {
                'message':'success delete data',
             }
             status_code=status.HTTP_204_NO_CONTENT
    else:
        content = {
			'message':'anda tidak berhak untuk mengakses funsi ini',
		}
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(content, status_code)
