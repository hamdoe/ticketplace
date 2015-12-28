from flask import Blueprint, current_app, render_template, request, url_for
from sqlalchemy.sql.expression import desc
from ticketplace.extensions import cache
from ticketplace.models import Content, Tag

main = Blueprint('main', __name__)


@main.context_processor
def inject_template_functions():
    def download(path):
        """ path를 받아 S3버킷에서의 url을 리턴 """
        if not path:
            """ Return default image if path is not supplied. """
            return url_for('static', filename='imgs/poster1.jpg')
        return 'https://ticketplace.s3.amazonaws.com/uploads/' + path
    return locals()


@main.route('/')
@main.route('/index')
@cache.cached(timeout=1000)
def home():
    """ Index page of eduticket.kr
    Displays contents from `FRONTPAGE_CONTENT_IDS` and `RECOMMENDED_CONTENT_IDS`
    """
    frontpage_content_ids = current_app.config['FRONTPAGE_CONTENT_IDS']
    frontpage_contents = [Content.query.get(id) for id in frontpage_content_ids]

    #: structure frontpage_contents into nested list to display them in carousel
    frontpage_carousel = [frontpage_contents[i:i+3] for i in range(0, len(frontpage_contents), 3)]

    recommended_content_ids = current_app.config['RECOMMENDED_CONTENT_IDS']
    recommended_contents = [Content.query.get(id) for id in recommended_content_ids]

    return render_template('main/index.html', **locals())


@main.route('/content/detail')
def detail():
    """ 콘텐츠 디테일 페이지 """

    related_content_ids = current_app.config['RELATED_CONTENT_IDS']
    related_contents = [Content.query.filter_by(content_id=content_id).first() for content_id in related_content_ids]

    content_id = request.args.get('content_id')
    content = Content.query.filter_by(content_id=content_id).first()

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

    try:
        list_page_title = ['유아 공연 목록', '초등 공연 목록', '청소년 공연 목록'][int(content_type)]
    except (TypeError, IndexError):
        list_page_title = '전체 공연 목록'

    return render_template('list.html', **locals())


@main.route('/list/')
def list_():
    """ 콘텐츠 리스트 페이지
    태그 시스템을 지원한다.
    ex) eduticket.kr/list/?tag=유아&tag=초등&tag=코믹
    """
    tags = request.args.getlist('tag')

    query = Content.query
    if tags:
        # Filter for contents with given tags
        # Note this is not the most efficient way of doing this.
        # However, for the sake of readability I would like to avoid using SQL wizardaries.
        query = query.join(Content.tags)
        for tag in tags:
            query = query.filter(Content.tags.any(Tag.name==tag))

    contents = query.all()

    return render_template('list.html', **locals())
