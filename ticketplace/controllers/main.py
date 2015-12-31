from flask import Blueprint, current_app, redirect, render_template, request, url_for
from ticketplace.extensions import cache
from ticketplace.models import Content, Tag
from ticketplace.send_email import send_email

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
def index():
    """ Index page of eduticket.kr
    Displays contents from `FRONTPAGE_CONTENT_IDS`
    """
    frontpage_content_ids = current_app.config['FRONTPAGE_CONTENT_IDS']
    frontpage_contents = [Content.query.get(id) for id in frontpage_content_ids]

    return render_template('main/index.html', **locals())


@main.route('/detail/<int:content_id>')
def detail(content_id):
    """ 콘텐츠 디테일 페이지 """
    try:
        content = Content.query.get(content_id)
    except:
        return redirect(url_for('main.index'))

    return render_template('main/detail.html', **locals())


@main.route('/reservation/<int:content_id>', methods=('GET', 'POST'))
def reservation(content_id):
    try:
        content = Content.query.get(content_id)
    except:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email_content = str(request.form)
        helpdesk_email = current_app.config.get('HELPDESK_EMAIL')
        send_email(helpdesk_email, '예약문의가 왔습니다.', email_content)
        return redirect(url_for('main.detail', content_id=content.id))
    return render_template('main/reservation.html', **locals())


@main.route('/howto/')
def howto():
    return render_template('main/howto.html', **locals())


@main.route('/list/')
def list_():
    """ 콘텐츠 리스트 페이지
    태그 시스템을 지원한다.
    ex) eduticket.kr/list/?tag=유아&tag=초등&tag=코믹
    """
    tags = request.args.getlist('tag')
    blockview = request.args.get('blockview', False, type=bool)

    query = Content.query
    if tags:
        # Filter for contents with given tags
        # Note this is not the most efficient way of doing this.
        # However, for the sake of readability I would like to avoid using SQL wizardaries.
        query = query.join(Content.tags)
        for tag in tags:
            query = query.filter(Content.tags.any(Tag.name==tag))

    contents = query.all()

    if blockview:
        return render_template('main/listblock.html', **locals())
    else:
        return render_template('main/list.html', **locals())
