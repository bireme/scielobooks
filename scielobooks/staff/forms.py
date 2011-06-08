from models import Monograph

import deform
import colander

class MemoryTmpStore(dict):
    def preview_url(self, name):
        return None


class MonographForm():

    tmpstore = MemoryTmpStore()

    base_schema = Monograph.get_schema()
    base_schema.add(colander.SchemaNode(
        colander.String(),
        name='publisher_url',
        missing=None))    
    base_schema.add(colander.SchemaNode(
        deform.FileData(),
        name='editorial_decision',
        widget=deform.widget.FileUploadWidget(tmpstore),
        missing=None))
    base_schema.add(colander.SchemaNode(
        deform.FileData(),
        name='toc',
        widget=deform.widget.FileUploadWidget(tmpstore),
        missing=None))

    base_schema['synopsis'].widget = deform.widget.TextAreaWidget(cols=80, rows=15)

    @classmethod
    def get_form(cls):
        return deform.Form(cls.base_schema, buttons=('submit',))


class PublisherForm():
    class Schema(colander.Schema):
        name = colander.SchemaNode(
            colander.String(),
            title='Publisher Name',
            description='Type the publisher name',
        )
        email = colander.SchemaNode(
            colander.String(),
            validator=colander.Email(),
            missing=None,
        )
        publisher_url = colander.SchemaNode(
            colander.String(),
            missing=None,
        )

    schema = Schema()

    @classmethod
    def get_form(cls):
        return deform.Form(cls.schema, buttons=('submit',))


class EvaluationForm():
    class Schema(colander.Schema):

        title = colander.SchemaNode(
            colander.String(),
        )
        isbn = colander.SchemaNode(
            colander.String(),
        )
        status = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(values=[('in_process','in process'),('approved','approved')],),
        )
        subject = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.TextAreaWidget(),
            missing=None,
        )
        publisher_catalog_url = colander.SchemaNode(
            colander.String(),
            missing=None,
        )
        publisher = colander.SchemaNode(
            colander.String(),
            missing=None,
        )

    schema = Schema()

    @classmethod
    def get_form(cls):
        return deform.Form(cls.schema, buttons=('submit',))

