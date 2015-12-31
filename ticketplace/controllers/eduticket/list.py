from ticketplace.controllers.eduticket import eduticket
from flask import render_template, request
from ticketplace.models import Content, Company


@eduticket.route('/company')
def company():
    # Parsing arguments
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    current_endpoint = request.endpoint

    # Data manipulation
    pagination = Company.query.order_by(Company.id.desc()).paginate(current_page, per_page, error_out=False)
    company_list = pagination.items
    return render_template('company_list.html', **locals())


@eduticket.route('/content')
def content():
    # Parsing arguments
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    current_endpoint = request.endpoint

    # Data manipulation
    pagination = Content.query.order_by(Content.id.desc()).paginate(current_page, per_page, error_out=False)
    content_list = pagination.items

    return render_template('content_list.html', **locals())
