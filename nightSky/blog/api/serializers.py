
from rest_framework import serializers
from blog.models import Post, Comment
from authentication.api.serializers import UserSerializerMinimal

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerMinimal(read_only=True)
    timestamp = serializers.CharField(read_only=True, source="get_jalali_date")
    
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ("text", "user", "score", "timestamp", "post")
        
        
        
    def create(self , validated_data):
        user = self.context["request"].user
        
        comment = Comment(
            text = validated_data["text"],
            post = validated_data["post"],
            user = user,
        )
        
        comment.save()
        
        return comment


class PostSerializerMinimal(serializers.ModelSerializer):
    timestamp = serializers.CharField(read_only=True, source="get_jalali_date")
    class Meta:
        model = Post
        fields = ("title", "description", "image", "timestamp")
        
        
class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(read_only=True, many=True)
    comments = serializers.SerializerMethodField()
    timestamp = serializers.CharField(read_only=True, source="get_jalali_date")
    
    def get_comments(self, obj):
        return CommentSerializer(obj.comments.filter(status=Comment.StatusChoice.ACCEPTED).order_by('-timestamp'), many=True).data
    
    class Meta:
        model = Post
        fields = ("title", "description", "image", "timestamp", "comments")
        
        
