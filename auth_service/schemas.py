from marshmallow import Schema, fields, validates, ValidationError

class AuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def validate_username(self, value, **kwargs):
        _len = len(value)
        if _len < 3 or _len > 64 or not value.isalnum():
            raise ValidationError('Username is invalid')

    @validates('password')
    def validate_password(self, value, **kwargs):
        if len(value) < 6:
            raise ValidationError('Password is invalid')
        
class CheckUsernameSchema(Schema):
    username = fields.Str(required=True)

    @validates('username')
    def validate_username(self, value, **kwargs):
        _len = len(value)
        if _len < 3 or _len > 64 or not value.isalnum():
            raise ValidationError('Username is invalid')
