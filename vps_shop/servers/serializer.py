from rest_framework import serializers

from .models import Vps


class VpsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vps
        fields = ("uid",
                  "name",
                  "user",
                  "cpu_cores",
                  "ram",
                  "storage",
                  "ip_address_private",
                  "ip_address_public",
                  "mac_address",
                  "created_at",
                  "updated_at")


#Realise for model-non Django
# class VpsSerializer(serializers.Serializer):
#
#     uid = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=60)
#     user_id = serializers.CharField(allow_blank=True)
#     cpu_cores = serializers.IntegerField(max_value=32, min_value=1)
#     ram = serializers.IntegerField(max_value=32, min_value=1)
#     storage = serializers.IntegerField(max_value=1024, min_value=15),
#     ip_address_private = serializers.IPAddressField(protocol='IPv4', allow_null=True)
#     ip_address_public = serializers.IPAddressField(protocol='IPv4', allow_null=True)
#     mac_address = serializers.CharField(read_only=True)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         return Vps.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.cpu_cores = validated_data.get('cpu_cores', instance.cpu_cores)
#         instance.ram = validated_data.get('ram', instance.ram)
#         instance.storage = validated_data.get('storage', instance.storage)
#         instance.ip_address_private = validated_data.get('ip_address_private', instance.ip_address_private)
#         instance.ip_address_public = validated_data.get('ip_address_public', instance.ip_address_public)
#         instance.mac_address = validated_data.get('mac_address', instance.mac_address)
#         instance.updated_at = validated_data.get('updated_at', instance.updated_at)
#
#         instance.save()
#         return instance




# class VpsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vps
#         fields = ('name', 'cpu_cores', 'ram', 'storage')