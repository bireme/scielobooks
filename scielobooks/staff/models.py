from isis import model
import deform
import urllib2


class Monograph(model.CouchdbDocument):
    title = model.TextProperty(required=True)
    isbn = model.TextProperty(required=True)
    creators = model.MultiCompositeTextProperty(subkeys=['role','full_name', 'link_resume'])
    publisher = model.TextProperty(required=True)
    publisher_url = model.TextProperty()
    language = model.TextProperty(choices=(('pt', 'portugues'), ('en', 'ingles')))
    synopsis = model.TextProperty()
    year = model.TextProperty()
    pages = model.TextProperty()
    edition = model.TextProperty()
    collection = model.TextProperty()
    format = model.CompositeTextProperty(subkeys=['height', 'width'])
    book = model.TextProperty()
    serie = model.TextProperty()
    pdf_file = model.FileProperty()
    cover = model.FileProperty()
    toc = model.FileProperty()
    editorial_decision = model.FileProperty()

    cover_thumbnail = model.FileProperty()
    visible = model.BooleanProperty()
    creation_date = model.TextProperty()
    created_by = model.TextProperty() #TODO

    class Meta:
        hide = ('cover_thumbnail', 'visible', 'creation_date', 'created_by')


class Part(model.CouchdbDocument):
    title = model.TextProperty(required=True)
    order = model.TextProperty()
    creators = model.MultiCompositeTextProperty(required=False, subkeys=['full_name', 'role'])
    pages = model.CompositeTextProperty(subkeys=['initial','final',])
    pdf_file = model.FileProperty()

    monograph = model.TextProperty(required=False)

    class Meta:
        hide = ('monograph',)
