from marshmallow import Schema, fields, validates, ValidationError

class ScanSchema(Schema):
    file_id = fields.Int(required=True)
    user_id = fields.Raw(required=True)
    path = fields.Str(required=True)
    filename = fields.Str(required=True)
    push_req = fields.Boolean(required=True)
    username = fields.Str(required=True)

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
        
    @validates('filename')
    def validate_filename(self, value, **kwargs):
        if len(value) == 0 or len(value) > 256:
            raise ValidationError('Filename is invalid')
        
    @validates('push_req')
    def validate_push_req(self, value, **kwargs):
        if not isinstance(value, bool):
            raise ValidationError('Push Req is invalid')
        
    @validates('username')
    def validate_username(self, value, **kwargs):
        if value in ('', None):
            return
        _len = len(value)
        if _len < 3 or _len > 64 or not value.isalnum():
            raise ValidationError('Username is invalid')
