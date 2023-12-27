from werkzeug.routing import BaseConverter


class SlugConverter(BaseConverter):

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value.replace(' ', '_')
