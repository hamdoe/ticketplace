from flask import Blueprint, current_app, render_template, request, url_for
from sqlalchemy.sql.expression import desc
from ticketplace.extensions import cache
from ticketplace.models import Content

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
@cache.cached(timeout=1000)
def home():
    # TODO: find out the best way to access configuration
    # TODO: make config['FRONTPAGE_CONTENT_IDS'] flat

    frontpage_contents = [[Content.query.filter_by(content_id=content_id).first() for content_id in ids] for ids in
                          current_app.config['FRONTPAGE_CONTENT_IDS']]
    recommended_contents = [Content.query.filter_by(content_id=content_id).first() for content_id in
                            current_app.config['RECOMMENDED_CONTENT_IDS']]

    def download(path):
        """ path를 받아 S3버킷에서의 url을 리턴 """
        if not path:
            #
            return url_for('static', filename='imgs/poster1.jpg')
        return 'https://ticketplace.s3.amazonaws.com/uploads/' + path

    return render_template('index.html', **locals())


@main.route('/content/detail')
def detail():
    """ 콘텐츠 디테일 페이지 """

    related_content_ids = [1, 2, 3, 4]
    related_contents = [Content.query.filter_by(content_id=content_id).first() for content_id in related_content_ids]

    content_id = request.args.get('content_id')
    content = Content.query.filter_by(content_id=content_id).first()

    def download(path):
        """ path를 받아 S3버킷에서의 url을 리턴 """
        if not path:
            return url_for('static', filename='imgs/poster1.jpg')
        return 'https://ticketplace.s3.amazonaws.com/uploads/' + path

    return render_template('detail.html', **locals())


@main.route('/content/list')
def content_list():
    """ 콘텐츠 리스트 페이지 """
    content_type = request.args.get('content_type')

    query = Content.query
    query = query.filter_by(status=2)
    if content_type == '0':
        query = query.filter(Content.age_min < 8)
    elif content_type == '1':
        query = query.filter(Content.age_min < 14).filter(Content.age_max > 7)
    elif content_type == '2':
        query = query.filter(Content.age_max > 13)
    query = query.order_by(desc(Content.content_id))
    contents = query.all()

    del query

    def download(path):
        """ path를 받아 S3버킷에서의 url을 리턴 """
        if not path:
            #
            return url_for('static', filename='imgs/poster1.jpg')
        return 'https://ticketplace.s3.amazonaws.com/uploads/' + path

    return render_template('list.html', int=int, **locals())
