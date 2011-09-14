from models import Monograph

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('scielobooks')

import datetime
import deform
import colander
from ..utilities import functions, isbn

def url_validate_factory(message=None):
    url_re = "^(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~\/|\/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:\/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|\/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$"
    return colander.Regex(url_re,message)

def isbn_validate_factory(message=None):
    def isbn_validator(node, value):
        if not isbn.isValidISBN(value):
            raise colander.Invalid(node,message)
    return isbn_validator

def year_validate_factory(message=None):
    def year_validator(node, value):
        try:
            i = int(value)
        except ValueError:
            raise colander.Invalid(node,message)
        if i < 100 or i > 9999:
            raise colander.Invalid(node,message)
    return year_validator

def integer_validate_factory(message=None):
    def year_validator(node, value):
        try:
            i = int(value)
        except ValueError:
            raise colander.Invalid(node,message)
        if i < 0:
            raise colander.Invalid(node,message)
    return year_validator

class MonographForm():

    @classmethod
    def get_form(cls, localizer):
        role_values = [('author','Author'),('translator','Translator'),('editor','Editor')]

        base_schema = Monograph.get_schema()
        base_schema['synopsis'].widget = deform.widget.TextAreaWidget(cols=80, rows=15)
        base_schema['individual_authors'].children[0].children[0].widget = deform.widget.SelectWidget(values=role_values)
        base_schema['corporate_authors'].children[0].children[0].widget = deform.widget.SelectWidget(values=role_values)

        #i18n
        base_schema.add(colander.SchemaNode(
            colander.String(),
            widget = deform.widget.HiddenWidget(),
            default= localizer.locale_name,
            name= '__LOCALE__',
        ))
        base_schema['title'].title = localizer.translate(_('Title'))
        base_schema['title'].description = localizer.translate(_('Title'))
        base_schema['isbn'].title = localizer.translate(_('ISBN'))
        base_schema['isbn'].description = localizer.translate(_('ISBN 13'))
        base_schema['isbn'].validator = isbn_validate_factory(localizer.translate(_('Invalid ISBN number')))
        base_schema['individual_authors'].title = localizer.translate(_('Individual author'))
        base_schema['individual_authors'].description = localizer.translate(_('Authors, translators, editors...'))
        base_schema['corporate_authors'].title = localizer.translate(_('Creators'))
        base_schema['corporate_authors'].description = localizer.translate(_('Authors, translators, editors...'))
        base_schema['publisher'].title = localizer.translate(_('Publisher'))
        base_schema['publisher'].description = localizer.translate(_('Select the publisher'))
        base_schema['publisher_url'].title = localizer.translate(_('Publisher\'s Catalog URL'))
        base_schema['publisher_url'].description = localizer.translate(_('URL to the refered book, at the publisher\'s catalog'))
        base_schema['publisher_url'].validator = url_validate_factory(localizer.translate(_('Invalid URL')))
        base_schema['language'].title = localizer.translate(_('Language'))
        base_schema['language'].description = localizer.translate(_('Book language'))
        base_schema['synopsis'].title = localizer.translate(_('Synopsis'))
        base_schema['synopsis'].description = localizer.translate(_('Short synopsis'))
        base_schema['year'].title = localizer.translate(_('Year'))
        base_schema['year'].description = localizer.translate(_('Publication year'))
        base_schema['year'].validator = year_validate_factory(message=localizer.translate(_('Invalid year format. Must be YYYY')))
        base_schema['city'].title = localizer.translate(_('City'))
        base_schema['city'].description = localizer.translate(_('City'))
        base_schema['country'].title = localizer.translate(_('Country'))
        base_schema['country'].description = localizer.translate(_('Country'))
        base_schema['pages'].title = localizer.translate(_('Pages'))
        base_schema['pages'].description = localizer.translate(_('Number of pages'))
        base_schema['pages'].validator = integer_validate_factory(message=localizer.translate(_('Invalid number of pages')))
        base_schema['primary_descriptor'].title = localizer.translate(_('Primary Descriptor'))
        base_schema['primary_descriptor'].description = localizer.translate(_('Primary Descriptor'))
        base_schema['primary_descriptor'].widget = deform.widget.TextAreaWidget(cols=60, rows=7)
        base_schema['edition'].title = localizer.translate(_('Edition'))
        base_schema['edition'].description = localizer.translate(_('Edition'))
        base_schema['collection'].title = localizer.translate(_('Collection'))
        base_schema['collection'].description = localizer.translate(_('Collection'))
        base_schema['format'].title = localizer.translate(_('Format'))
        base_schema['format']['height'].title = localizer.translate(_('Height'))
        base_schema['format']['height'].validator = integer_validate_factory(message=localizer.translate(_('Invalid height')))
        base_schema['format']['width'].title = localizer.translate(_('Width'))
        base_schema['format']['width'].validator = integer_validate_factory(message=localizer.translate(_('Invalid width')))
        base_schema['book'].title = localizer.translate(_('Book'))
        base_schema['book'].description = localizer.translate(_('Book'))
        base_schema['serie'].title = localizer.translate(_('Serie'))
        base_schema['serie'].description = localizer.translate(_('serie'))
        base_schema['use_licence'].title = localizer.translate(_('Use Licence'))
        base_schema['use_licence'].description = localizer.translate(_('Use Licence'))
        base_schema['pdf_file'].title = localizer.translate(_('Book in PDF'))
        base_schema['pdf_file'].description = localizer.translate(_('Full book PDF'))
        base_schema['cover'].title = localizer.translate(_('Book Cover'))
        base_schema['cover'].description = localizer.translate(_('Book cover in high resolution'))
        base_schema['toc'].title = localizer.translate(_('Table of Contents'))
        base_schema['toc'].description = localizer.translate(_('TOC in PDF'))
        base_schema['editorial_decision'].title = localizer.translate(_('Editorial Decision'))
        base_schema['editorial_decision'].description = localizer.translate(_('Editorial Decision in PDF'))

        btn_cancel = deform.form.Button(name='btn_cancel', title=localizer.translate(_('Cancel')),
                               type='submit', value='cancel', disabled=False)
        btn_submit = deform.form.Button(name='btn_submit', title=localizer.translate(_('Submit')),
                               type='submit', value='submit', disabled=False)

        return deform.Form(base_schema, buttons=(btn_cancel, btn_submit,))


class PublisherForm():
    @classmethod
    def get_form(cls, localizer):
        class Schema(colander.Schema):
            name = colander.SchemaNode(
                colander.String(),
                title=localizer.translate(_('Publisher Name')),
                description=localizer.translate(_('Publisher name')),
            )
            email = colander.SchemaNode(
                colander.String(),
                validator=colander.Email(),
                missing=None,
                title=localizer.translate(_('E-mail')),
                description=localizer.translate(_('Contact e-mail')),
            )
            publisher_url = colander.SchemaNode(
                colander.String(),
                validator=url_validate_factory(message=localizer.translate(_('Invalid URL'))),
                missing=None,
                title=localizer.translate(_('Institutional Site')),
                description=localizer.translate(_('URL to publisher\'s institutional site')),
            )
            __LOCALE__ = colander.SchemaNode(
                colander.String(),
                widget = deform.widget.HiddenWidget(),
                default= localizer.locale_name,
            )
        schema = Schema()

        btn_cancel = deform.form.Button(name='btn_cancel', title=localizer.translate(_('Cancel')),
                               type='submit', value='cancel', disabled=False)
        btn_submit = deform.form.Button(name='btn_submit', title=localizer.translate(_('Submit')),
                               type='submit', value='submit', disabled=False)

        return deform.Form(schema, buttons=(btn_cancel, btn_submit,))


class EvaluationForm():
    @classmethod
    def get_form(cls, localizer):
        class Schema(colander.Schema):
            title = colander.SchemaNode(
                colander.String(),
                title=localizer.translate(_('Book Title')),
                description=localizer.translate(_('Book title without abbreviations')),
            )
            isbn = colander.SchemaNode(
                colander.String(),
                validator=isbn_validate_factory(message=localizer.translate(_('Invalid ISBN number'))),
                title=localizer.translate(_('ISBN')),
                description=localizer.translate(_('ISBN 13')),
            )
            subject = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.TextAreaWidget(),
                missing=None,
                title=localizer.translate(_('Subject')),
                description=localizer.translate(_('Subject key-words, separated by semi-colons ";"')),
            )
            publisher_catalog_url = colander.SchemaNode(
                colander.String(),
                missing=None,
                validator=url_validate_factory(message=localizer.translate(_('Invalid URL'))),
                title=localizer.translate(_('Publisher\'s Catalog URL')),
                description=localizer.translate(_('URL to the refered book, at the publisher\'s catalog')),
            )
            publisher = colander.SchemaNode(
                colander.String(),
                missing=None,
                title=localizer.translate(_('Publisher')),
                description=localizer.translate(_('Publisher name')),
            )
            __LOCALE__ = colander.SchemaNode(
                colander.String(),
                widget = deform.widget.HiddenWidget(),
                default= localizer.locale_name,
            )
        schema = Schema()

        btn_cancel = deform.form.Button(name='btn_cancel', title=localizer.translate(_('Cancel')),
                               type='submit', value='cancel', disabled=False)
        btn_submit = deform.form.Button(name='btn_submit', title=localizer.translate(_('Submit')),
                               type='submit', value='submit', disabled=False)

        return deform.Form(schema, buttons=(btn_cancel, btn_submit,))

class MeetingForm():
    @classmethod
    def get_form(cls, localizer, default_css=None, **kwargs):
        class Schema(colander.Schema):
            date = colander.SchemaNode(
                    colander.Date(),
                    validator=colander.Range(
                        min=datetime.date.today(),
                        min_err='${val} is earlier than earliest date ${min}'
                        ),
                    title=localizer.translate(_('Meeting Date')),
                    description=localizer.translate(_('Select the meeting date')),
            )
            description = colander.SchemaNode(
                colander.String(),
                missing=None,
                title=localizer.translate(_('Description')),
                description=localizer.translate(_('Short description about the meeting')),
            )
            __LOCALE__ = colander.SchemaNode(
                colander.String(),
                widget = deform.widget.HiddenWidget(),
                default= localizer.locale_name,
            )
        schema = Schema()

        btn_cancel = deform.form.Button(name='btn_cancel', title=localizer.translate(_('Cancel')),
                               type='submit', value='cancel', disabled=False)
        btn_submit = deform.form.Button(name='btn_submit', title=localizer.translate(_('Submit')),
                               type='submit', value='submit', disabled=False)

        form = deform.Form(schema, buttons=(btn_cancel, btn_submit,))
        #functions.customize_form_css_class(form, default_css, **kwargs)
        return form
