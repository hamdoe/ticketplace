import boto3
from flask.ext.admin.base import BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.sqla.view import ModelView
from flask.ext.wtf.file import FileField
from flask.ext.wtf.form import Form
from flask.globals import request, current_app, session
from flask.helpers import url_for, flash
from jinja2 import Markup
from ticketplace.models import Content
from ticketplace.utils import kst_now
from werkzeug.utils import redirect, secure_filename
from wtforms.fields.simple import SubmitField, StringField


class FileForm(Form):
    file = FileField('Your File')
    submit = SubmitField('Submit')


class LoginForm(Form):
    password = StringField('패스워드')
    submit = SubmitField('Submit')


class IndexView(AdminIndexView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        login_form = LoginForm()
        if request.method=='POST':
            if not current_app.config.get('MASTER_PASSWORD', None):
                flash('패스워드가 설정되어 있지 않습니다. 관리자를 탓하세요.', 'error')
                return redirect(url_for('admin.index'))
            if login_form.data['password'] == current_app.config.get('MASTER_PASSWORD'):
                flash('성공적으로 로그인되었습니다.')
                session['admin_authenticated'] = True
                return redirect(url_for('admin.index'))
            else:
                flash('로그인 실패', 'error')
                return redirect(url_for('admin.index'))
        self._template_args['login_form'] = login_form
        return super(IndexView, self).index()


class CompanyView(ModelView):
    """ Admin view for `Company` """
    can_view_details = True
    column_list = ['id', 'name', 'username', 'represent_name', 'represent_phone', 'represent_email',
                   'manager_name', 'manager_phone', 'manager_email', 'note']
    column_searchable_list = [column for column in column_list if column not in ['id']]

    def is_accessible(self):
        return session.get('admin_authenticated', False)


class ContentView(ModelView):
    """ Admin view for `Content` """
    can_view_details = True
    column_list = ['id', 'name', 'company.name', 'original_price', 'price', 'start_date', 'end_date', 'manager_name', 'manager_phone', 'manager_email', 'inquire_number', 'status', 'note']
    column_searchable_list = ['name', 'company.name', 'manager_name', 'manager_phone', 'manager_email', 'inquire_number', 'note']

    def is_accessible(self):
        return session.get('admin_authenticated', False)


class TagView(ModelView):
    """ Admin view for content tags"""
    can_view_details = True

    def is_accessible(self):
        return session.get('admin_authenticated', False)


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
    can_edit = False

    column_list = ['id', 'name', 'background_image', 'index_image', 'main_image', 'thumbnail_image']

    column_searchable_list = ['name']
    column_sortable_list = ['id', 'name']
    column_default_sort = ('id', True)

    # Override list html to make image upload button
    list_template = 'admin/image_list.html'

    # Columns of images
    image_columns = ['background_image', 'index_image', 'main_image', 'thumbnail_image']

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        # Override Index view to inject template variables
        form = FileForm()
        self._template_args['image_columns'] = self.image_columns
        self._template_args['form'] = form
        return super(ContentImageView, self).index_view()

    @expose('/upload/<column_name>/<content_id>', methods=['GET', 'POST'])
    def upload(self, column_name, content_id):
        form = FileForm()
        content = Content.query.get(content_id)

        if request.method == 'POST':
            try:
                # Save form data to (temporary) local file
                filename = secure_filename(str(kst_now()) + form.file.data.filename)
                form.file.data.save(filename)

                # Upload local file to S3 (Note this is a blocking call)
                image_path = 'uploads/%s' % filename
                aws_key = current_app.config.get('AWS_KEY', None)
                aws_secret_key = current_app.config.get('AWS_SECRET_KEY', None)
                if not aws_key or not aws_secret_key:
                    flash('AWS키가 설정되지 않았습니다.', 'error')
                    raise Exception
                boto3_session = boto3.session.Session(aws_access_key_id=aws_key,
                                                      aws_secret_access_key=aws_secret_key)
                boto3_session.client('s3')
                s3_client = boto3_session.client('s3')
                s3_client.upload_file(filename, 'ticketplace', image_path)

                # Set Image path to column
                setattr(content, column_name, filename)
                self.session.add(content)
                self.session.commit()

                flash('이미지 업로드 완료')
            except:
                flash('이미지 업로드 실패', 'error')
            return redirect(url_for('image.index_view'))

        return self.render('admin/upload.html', form=form, content=content, column_name=column_name)

    def is_accessible(self):
        return session.get('admin_authenticated', False)


