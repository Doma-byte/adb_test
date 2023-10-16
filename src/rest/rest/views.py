from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


try:
    # mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
    db = MongoClient("mongodb+srv://" + os.environ["CLUSTER_STRING"])['test_db']
    # db = MongoClient(mongo_uri)['test_db']
    collection_name = db['adbrew_test']
except ConnectionFailure as e:
    logging.error(f'MongoDB connection error: {e}')
    collection_name = None

class TodoListView(APIView):
    def get(self, request):
        if collection_name is None:
            return Response({'error': 'MongoDB connection error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            todo_items = list(collection_name.find({}, {'description': 1}))
            todo_items = [{'_id': str(
                todo['_id']), 'description': todo['description']} for todo in todo_items]
            return Response(todo_items, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if collection_name is None:
                return Response({'error': 'MongoDB connection error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

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
