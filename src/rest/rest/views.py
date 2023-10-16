import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .database import DatabaseManager

class TodoListView(APIView):
    def __init__(self, db_uri='mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]):
        super().__init__()
        self.db_manager = DatabaseManager(db_uri)
        self.db_manager.connect()

    def get(self, request):
        collection_name = self.db_manager.get_collection()
        if collection_name is None:
            return Response({'error': 'MongoDB connection error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            todo_items = list(collection_name.find({}, {'description': 1}))
            todo_items = [{'_id': str(todo['_id']), 'description': todo['description']} for todo in todo_items]
            return Response(todo_items, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        collection_name = self.db_manager.get_collection()
        if collection_name is None:
            return Response({'error': 'MongoDB connection error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            new_todo = {'description': request.data.get('description')}
            result = collection_name.insert_one(new_todo)
            if result.acknowledged:
                response_data = {
                    '_id': str(result.inserted_id),
                    'message': 'TODO created successfully',
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Insertion not acknowledged'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
