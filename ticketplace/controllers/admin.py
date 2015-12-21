import boto3
from flask.ext.admin.base import BaseView, expose
from flask.ext.admin.contrib.sqla.view import ModelView
from flask.ext.wtf.file import FileField
from flask.ext.wtf.form import Form
from flask.globals import request, current_app
from flask.helpers import url_for, flash
from jinja2 import Markup
from ticketplace.models import Content
from ticketplace.utils import kst_now
from werkzeug.utils import redirect, secure_filename
from wtforms.fields.simple import SubmitField


class FileForm(Form):
    file = FileField('Your File')
    submit = SubmitField('Submit')


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

    column_sortable_list = ['content_id', 'name']
    column_default_sort = ('content_id', True)

    # Override list html to make image upload button
    list_template = 'admin/image_list.html'

    # Columns of images
    image_columns = ['background_image', 'index_image', 'main_image', 'thumbnail_image']

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        # Override Index view to inject template variables
        self._template_args['image_columns'] = self.image_columns
        return super(ContentImageView, self).index_view()

    @expose('/upload/<column_name>/<content_id>', methods=['GET', 'POST'])
    def upload(self, column_name, content_id):
        form = FileForm()
        content = Content.query.get(content_id)

        if request.method == 'POST':
            if form.validate_on_submit():
                # Save form data to (temporary) local file
                filename = secure_filename(str(kst_now()) + form.file.data.filename)
                form.file.data.save(filename)

                # Upload local file to S3
                image_path = 'uploads/%s' % filename
                boto3_session = boto3.session.Session(aws_access_key_id=current_app.config['AWS_KEY'],
                                                      aws_secret_access_key=current_app.config['AWS_SECRET_KEY'])
                boto3_session.client('s3')
                s3_client = boto3_session.client('s3')
                s3_client.upload_file(filename, 'ticketplace', image_path)
                flash('이미지 업로드 완료')

                setattr(content, column_name, filename)
                self.session.add(content)
                self.session.commit()

            else:
                flash('이미지 업로드 실패', 'error')
            return redirect(url_for('image.index_view'))

        return self.render('admin/upload.html', form=form, content=content, column_name=column_name)


