from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """
    BaseSerializer is a base class for serializers that provides common fields for model serialization.

    Attributes:
        id (CharField): A read-only field representing the identifier of the model.
        created_at (DateTimeField): A read-only field representing the creation timestamp.
        updated_at (DateTimeField): A read-only field representing the last update timestamp.
    """
    id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)