
from time import sleep

from django.core.cache import cache
from django.forms import model_to_dict
from django.http import HttpResponse
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.decorators.http import require_POST
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView
from rest_framework import serializers, status, viewsets

from .models import Vps
from rest_framework import generics

from .permissions import IsOwnerCreateReadUpdateDelete
from .serializer import VpsSerializer
from .utils import generate_random_mac_address


### DRF(API) ###


class VpsViewSet(viewsets.ModelViewSet):
    # queryset = Vps.objects.all()
    serializer_class = VpsSerializer
    permission_classes = [IsOwnerCreateReadUpdateDelete]
    def get_queryset(self):
        return Vps.objects.filter(user=self.request.user)

    # lookup_field = 'uid'

    @action(methods=['get'], detail=False)
    def get_mac_address(self, request, pk=None):
        pk = request.query_params.get('pk')
        if pk:
            vpsList = Vps.objects.get(uid=pk)
            map_mac = {vpsList.name: vpsList.mac_address}
            return Response(map_mac)

        vpsList = Vps.objects.all()
        map_mac = {'mac address': {vps.name: vps.mac_address for vps in vpsList}}
        return Response(map_mac)

    # @action(methods=['get'], detail=False)
    # def get_mac_address(self, request):
    #     vpsList = Vps.objects.all()
    #     map_mac = {'mac address': {vps.name: vps.mac_address for vps in vpsList}}
    #     return Response(map_mac)


# class VpsAPIList(generics.ListCreateAPIView):
#     queryset = Vps.objects.all()
#     serializer_class = VpsSerializer
#
# class VpsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Vps.objects.all()
#     serializer_class = VpsSerializer
#     lookup_field = 'uid'


# class VpsAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         if kwargs.get('uid', None):
#             try:
#                 vps_list = Vps.objects.get(uid=kwargs.get('uid'))
#                 return Response({'vps_list': VpsSerializer(vps_list).data})
#             except:
#                 return Response({'error': 'Vps does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             vps_list = Vps.objects.all()
#             return Response({'vps_list':VpsSerializer(vps_list, many=True).data})
#
#     def post(self, request):
#         serializers = VpsSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({f'vps_{request.data['name']}':serializers.data})
#
#     def put(self, request, *args, **kwargs):
#         uid = kwargs.get('uid', None)
#         if not uid:
#             return Response({'error': 'Method PUT in not allowed'})
#
#         try:
#             instance = Vps.objects.get(uid=uid)
#         except:
#             return Response({'error': 'Objects not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializers = VpsSerializer(data=request.data, instance=instance)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({'vps': serializers.data})
#
#     def delete(self, request, *args, **kwargs):
#         uid = kwargs.get('uid', None)
#         if not uid:
#             return Response({'error': 'Method DELETE in not allowed'})
#         try:
#             instance = Vps.objects.get(uid=uid)
#         except:
#             return Response({'error': 'Objects not found'}, status=status.HTTP_404_NOT_FOUND)
#         instance.delete()
#         return Response({'vps': f'Delete vps from uid {uid}'})


# class VpsAPIView(APIView):
#     def get(self, request):
#         vps_list = Vps.objects.all().values()
#         return Response({'vps': list(vps_list)})
#
#     def post(self, request):
#         vps_new = Vps.objects.create(
#             name=request.data['name'],
#             user_id=request.data['user_id'],
#             cpu_cores=request.data['cpu_cores'],
#             ram=request.data['ram'],
#             storage=request.data['storage'],
#             mac_address=request.data['mac_address']
#         )
#
#         return Response({'vps': model_to_dict(vps_new)})


# class VpsAPIView(generics.ListAPIView):
#     queryset = Vps.objects.all()
#     serializer_class = VpsSerializer






### classic views


menu = ['About', 'View VPS templates', 'Construction VPS', 'Status']

vps = [
    {'uid': 1, 'name': 'vps_1', 'cpu': 2, 'ram': 2, 'storage': 40},
    {'uid': 2, 'name': 'vps_2', 'cpu': 1, 'ram': 1, 'storage': 20}
    ]

app_page = [
    {'page':'home', 'url': 'home'},
    {'page':'about', 'url': 'about'},
    ]

def index(request):

    return render(request, 'servers/index.html')


def vps_collection(request):
    contents = {
        'app_page': app_page,
        'vps_collection': vps
    }
    return render(request, 'servers/vps_collection.html', contents)

def vps_target(request, uid:int):
    _vps = next((item for item in vps if item['uid'] == uid), None)
    contents = {
        'vps_target': _vps
    }
    return render(request, 'servers/vps.html', contents)


def about(request):
    return render(request, 'servers/about.html', {'title':'About'})


