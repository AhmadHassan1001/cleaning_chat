from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .guardrail_agent import GuardrailAgent

class AgentView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, format=None):
        agent=GuardrailAgent()
        print(request.data)
        answer=agent.get_answer(request.data['content'])
        return Response({"answer": answer}, status=status.HTTP_200_OK)