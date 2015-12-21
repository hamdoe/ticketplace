from flask.ext.admin.base import BaseView, expose
from flask.ext.admin.contrib.sqla.view import ModelView
from flask.helpers import url_for
from jinja2 import Markup
from ticketplace.models import Content


class CompanyView(ModelView):
    """ Admin view for `Company` """
    can_view_details = True
    column_list = ['company_id', 'company_name', 'id', 'represent_name', 'represent_phone', 'represent_email',
                   'manager_name', 'manager_phone', 'manager_email', 'note']
    column_searchable_list = [column for column in column_list if column not in ['company_id']]


class ContentView(ModelView):
    """ Admin view for `Content` """
    can_view_details = True
    column_list = ['content_id', 'name', 'company.company_name', 'original_price', 'price', 'content_start_date',
                   'content_end_date', 'manager_name', 'manager_phone', 'manager_email', 'inquire_number', 'status',
                   'note']
    column_searchable_list = [column for column in column_list if column not in ['content_id', 'company']]


class ContentImageView(ModelView):
    """ Admin view for `Content` """

    def _list_thumbnail(view, context, model, name):
        image_path = getattr(model, name)
        if not image_path:
            return ''

        def download(path):
            """ path를 받아 S3버킷에서의 url을 리턴 """
            if not path:
                """ Return default image if path is not supplied. """
                return url_for('static', filename='imgs/poster1.jpg')
            return 'https://ticketplace.s3.amazonaws.com/uploads/' + path

        return Markup('<img style="max-width:100%%;max-height:100%%;" src="%s">' % download(image_path))

    column_formatters = {
        'background_image': _list_thumbnail,
        'index_image': _list_thumbnail,
        'main_image': _list_thumbnail,
        'thumbnail_image': _list_thumbnail,
    }

    can_view_details = True
    can_create = False
    can_delete = False

    column_list = ['content_id', 'name', 'background_image', 'index_image', 'main_image', 'thumbnail_image']

    @expose('/upload/<content_id>')
    def upload(self, content_id):
        content = Content.query.get(content_id)
        return self.render('admin/upload.html', content=content)


