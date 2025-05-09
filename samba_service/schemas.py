from marshmallow import Schema, fields, validates, ValidationError

class CreateFolderSchema(Schema):
    username = fields.Str(required=True)

    @validates('username')
    def validate_username(self, value, **kwargs):
        _len = len(value)
        if _len < 3 or _len > 64 or not value.isalnum():
            raise ValidationError('Username is invalid')
