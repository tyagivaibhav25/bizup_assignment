from rest_framework import serializers


class apiSerailizer(serializers.Serializer):
   logo_border = serializers.CharField()
   dominant_color=serializers.CharField()
