from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model() 


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def SaveScore(request):
    user = request.user
    if user.player:
        data = request.data.copy()
        data['player'] = user.id
        serializer = ScoreSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            if instance.level == 10:
                Winners.objects.create(player=instance.player)
            return JsonResponse({
                "status_code" : 200,
                "Message" : "You score has been updated successfully"
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)