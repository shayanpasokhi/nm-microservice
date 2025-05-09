from marshmallow import Schema, fields, validates, ValidationError

class ScanSchema(Schema):
    file_id = fields.Int(required=True)
    user_id = fields.Raw(required=True)
    path = fields.Str(required=True)

    @validates('user_id')
    def validate_user_id(self, value, **kwargs):
        if value in ('', None):
            return
        try:
            int_val = int(value)
        except (ValueError, TypeError):
            raise ValidationError('User ID is invalid')
        
    @validates('path')
    def validate_path(self, value, **kwargs):
        if len(value) == 0 or len(value) > 255:
            raise ValidationError('Path is invalid')
