# TODO: Consider using serializers for data validation
class ValidatorMixin:
    def validate_data(self, data, **kwargs) -> dict:
        raise NotImplementedError("Override validate_data")

    def get_validated_data(self, data, **kwargs):
        validated_data = self.validate_data(data, **kwargs)
        if validated_data is None:
            raise ValueError("validate_data should return the validated data")
        return validated_data
