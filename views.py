from transformers import pipeline
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid
import time

# Initialize the summarization pipeline with the default model
summarizer = pipeline("summarization")

# Temporary in-memory store to track requests and their statuses
summaries = {}

# POST endpoint to summarize text
@api_view(['POST'])
def summarize_text(request):
    if 'text' not in request.data:
        return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    text = request.data['text']
    
    # Generate a unique ID for this summarization request
    summary_id = str(uuid.uuid4())
    
    # Save the initial status of the summarization request
    summaries[summary_id] = {'status': 'Processing', 'result': None, 'timestamp': time.time()}
    
    # Perform summarization in a separate process or thread (this could be optimized)
    # For now, we'll just simulate the summarization
    summary = summarizer(text, max_length=190, min_length=90, do_sample=False)
    
    # Update the status with the result
    summaries[summary_id]['status'] = 'Completed'
    summaries[summary_id]['result'] = summary[0]['summary_text']
    
    # Return the summary ID for status checking later
    return Response({"summary_id": summary_id}, status=status.HTTP_202_ACCEPTED)

# GET endpoint to check the status of the summarization
@api_view(['GET'])
def get_summary_status(request, summary_id):
    if summary_id not in summaries:
        return Response({"error": "Invalid summary ID"}, status=status.HTTP_404_NOT_FOUND)
    
    summary_info = summaries[summary_id]
    
    if summary_info['status'] == 'Completed':
        return Response({
            "status": summary_info['status'],
            "summary": summary_info['result'],
            "timestamp": summary_info['timestamp']
        })
    else:
        return Response({
            "status": summary_info['status'],
            "timestamp": summary_info['timestamp']
        })
