from rest_framework import serializers


class SummarizationSerializer(serializers.Serializer):
    text = serializers.CharField()
    method = serializers.ChoiceField(choices=["stuff", "map_reduce", "refine"], default="stuff")

class SentimentRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    
class KeywordRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    count = serializers.IntegerField(required=False, default=5)

class TextClassificationSerializer(serializers.Serializer):
    text = serializers.CharField()
    categories = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

class LanguageDetectionSerializer(serializers.Serializer):
    text = serializers.CharField()

class TextTranslationSerializer(serializers.Serializer):
    text = serializers.CharField()
    target_language = serializers.CharField()
    source_language = serializers.CharField(required=False, default="auto")

class QuestionAnsweringSerializer(serializers.Serializer):
    question = serializers.CharField()
    context = serializers.CharField(required=False, allow_blank=True)

class ContentGenerationSerializer(serializers.Serializer):
    prompt_text = serializers.CharField()
    content_type = serializers.ChoiceField(
        choices=["email", "story", "blog", "social_media", "product_description", "general"],
        default="general"
    )
    max_length = serializers.IntegerField(required=False, default=500, min_value=50, max_value=2000)