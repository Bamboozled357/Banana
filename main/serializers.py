from rest_framework import serializers

from main.models import Publication, Comment


class PublicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ('id', 'title', 'text', 'user')
        # exclude = ('id', 'creation_date')


class PublicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep


class CommentSerializer(serializers.ModelSerializer):
    publication = serializers.PrimaryKeyRelatedField(write_only=True,
                                                     queryset=Publication.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'publication', 'text', 'user')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class CreatePublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

