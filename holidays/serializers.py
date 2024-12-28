from rest_framework import serializers

class HolidaysSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=5000)
    date = serializers.DateField()

    def to_representation(self, instance):
        return {
            'name': instance['name'],
            'description': instance.get('description', ''),
            'date': instance['date']['iso'],
        }