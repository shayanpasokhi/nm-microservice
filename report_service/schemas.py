from marshmallow import Schema, fields, validates, ValidationError

class AddReportSchema(Schema):
    file_id = fields.Int(required=True)
    user_id = fields.Raw(required=True)
    scanner = fields.Str(required=True)

    @validates('user_id')
    def validate_user_id(self, value, **kwargs):
        if value in ('', None):
            return
        try:
            int_val = int(value)
        except (ValueError, TypeError):
            raise ValidationError('User ID is invalid')
        
    @validates('scanner')
    def validate_scanner(self, value, **kwargs):
        if len(value) == 0 or len(value) > 255:
            raise ValidationError('Scanner is invalid')
        
class UpdateReportSchema(Schema):
    report_id = fields.Int(required=True)
    result = fields.Str(required=True)
    scanned_at = fields.Str(required=True)

    @validates('scanned_at')
    def validate_scanned_at(self, value, **kwargs):
        if len(value) == 0:
            raise ValidationError('Scanned At is invalid')
