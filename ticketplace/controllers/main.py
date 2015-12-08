from flask import Blueprint, current_app, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from ticketplace.extensions import cache
from ticketplace.forms import LoginForm
from ticketplace.models import User, Content

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
@cache.cached(timeout=1000)
def home():
    # TODO: find out the best way to access configuration
    # TODO: make config['FRONTPAGE_CONTENT_IDS' flat

    frontpage_contents = [[Content.query.filter_by(content_id=content_id).first() for content_id in ids] for ids in
                          current_app.config['FRONTPAGE_CONTENT_IDS']]
    recommended_contents = [Content.query.filter_by(content_id=content_id).first() for content_id in current_app.config['RECOMMENDED_CONTENT_IDS']]

    def download(path):
        """ path를 받아 S3버킷에서의 url을 리턴 """
        if not path:
            #
            return url_for('static', filename='imgs/poster1.jpg')
        return 'https://ticketplace.s3.amazonaws.com/uploads/' + path

    return render_template('index.html', **locals())


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200


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
            #
            return url_for('static', filename='imgs/poster1.jpg')
        return 'https://ticketplace.s3.amazonaws.com/uploads/' + path

    return render_template('detail.html', **locals())

