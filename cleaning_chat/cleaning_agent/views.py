from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AgentView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, format=None):
        return Response(request.data)