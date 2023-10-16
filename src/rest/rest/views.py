from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os
from pymongo import MongoClient

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
# db = MongoClient("mongodb+srv://" + os.environ["CLUSTER_STRING"])['test_db']
db = MongoClient(mongo_uri)['test_db']
collection_name = db['adbrew_test']

class TodoListView(APIView):

    def get(self, request):
        # Implement this method - return all todo items from db instance above.
        todo_items = list(collection_name.find({}, {'description': 1}))
        todo_items = [{'_id': str(todo['_id']), 'description': todo['description']} for todo in todo_items]
        return Response(todo_items, status=status.HTTP_200_OK)
        
    def post(self, request):
        # Implement this method - accept a todo item in a mongo collection, persist it using db instance above.
        new_todo = {'description': request.data.get('description')}
        result = collection_name.insert_one(new_todo)
        response_data = {
            '_id': str(result.inserted_id),
            'message': 'TODO created successfully',
        }
        return Response(response_data, status=status.HTTP_200_OK)