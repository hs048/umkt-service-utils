"""CAS authentication middleware"""
import json
import jwt
import logging

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request as RESTRequest

__all__ = ["UMKTJWTMiddleware"]

from rest_framework.exceptions import APIException

# from umkt_service_utils.models import Lembaga

logger = logging.getLogger(__name__)


def create_response(request_id, code, message):
    """
    Function to create a response to be sent back via the API
    :param request_id:Id fo the request
    :param code:Error Code to be used
    :param message:Message to be sent via the APi
    :return:Dict with the above given params
    """

    try:
        req = str(request_id)
        data = {"data": message, "code": int(code), "request_id": req}
        return data
    except Exception as creation_error:
        logger.error(f'create_response:{creation_error}')

class UMKTJWTMiddleware(MiddlewareMixin):
    """Middleware that allows CAS authentication on admin pages"""

    def process_request(self, request):

        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else None
        """

        jwt_token = request.headers.get('authorization', None)
        logger.info(f"request received for endpoint {str(request.path)}")

        if jwt_token:
            # authenticate(request, jwt_token)
            try:
                url = 'https://api.umkt.ac.id/'

                payload = jwt.decode(jwt_token.split(' ')[1], algorithms=['HS256'],
                                     options=({"verify_signature": False, 'verify_exp': True}), )
                uniid = payload['user']
                try:
                    user = User.objects.get(username=uniid)
                except User.DoesNotExist:
                    if uniid[0].isdigit():
                        auth_url = url + 'managemen/mahasiswa/' + uniid
                    else:
                        auth_url = url + 'managemen/karyawan/' + uniid
                    headers = {"Authorization": jwt_token}
                    response = requests.get(auth_url, headers=headers)
                    if not response.status_code == 200:
                        res = response.json()
                        logger.info(f"Response {res}")
                        return HttpResponse(json.dumps(res), status=401)
                    data = response.json()
                    userdata = data['rows']['user'][0]
                    username = userdata['username']
                    user = User.objects.create(username=username, first_name=userdata['first_name'],
                                               last_name=userdata['last_name'], email=userdata['email'])
                request.user_umkt = user
                return None
            except jwt.ExpiredSignatureError:
                raise APIException(code=401, detail='Authentication token has expired')
            except (jwt.DecodeError, jwt.InvalidTokenError):
                raise APIException(code=401, detail='Authorization has failed, Please send valid token.')
        else:
            if isinstance(request, RESTRequest):
                raise APIException(code=401, detail='Authorization not found, Please send valid token in headers.')

        
