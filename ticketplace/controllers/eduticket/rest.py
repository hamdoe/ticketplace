from flask import render_template, request, redirect, flash
from flask.ext.wtf import Form
from sqlalchemy.exc import ProgrammingError
from wtforms_alchemy import model_form_factory
from wtforms.fields.simple import SubmitField
import ticketplace.models as models
from ticketplace.models import db
from ticketplace.controllers.eduticket import eduticket

url_prefix = '/admin/'


# wtforms-alchemy와 flask-wtf을 같이 쓰기 위한 스크립트
BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


def camel_case(word):
    """snake_case -> CamelCase"""
    return ''.join(x.capitalize() for x in word.split('_'))


def get_table(table_name):
    """
    Returns table object
    Accepts both snake_case and CamelCase
    """
    return getattr(models, camel_case(table_name))


def generate_form(table_name):
    """
    Generates GeneralForm class
    Usage Example:

    CompanyForm = generate_form('Company')
    form = CompanyForm(obj=company)
    """
    try:
        table = get_table(table_name)
    except (TypeError, AttributeError):
        table = None

    class GeneralForm(ModelForm):
        class Meta:
            model = table

            # Make foreign key editable
            include_foreign_keys = True

        submit = SubmitField()

        def __iter__(self):
            # Sets the order of the fields
            fields = list(super(GeneralForm, self).__iter__())
            fields = fields[1:] + fields[:1]
            return (field for field in fields)

    return GeneralForm


CompanyForm = generate_form('Company')
ContentForm = generate_form('Content')
ContentTimeForm = generate_form('ContentTime')
ReservationForm = generate_form('Reservation')
HumanForm = generate_form('Human')
EventForm = generate_form('Event')


def update_object(table_name, object_id):
    Table = get_table(table_name)
    object = Table.query.filter_by(**{table_name + '_id': object_id}).first()
    Form = generate_form(table_name)
    if request.method == 'GET':
        form = Form(request.form, obj=object)
        return render_template('form.html', form=form)
    elif request.method == 'POST':
        for key in request.form:
            data = request.form[key]
            if data == '':
                continue
            setattr(object, key, data)
        try:
            db.session.commit()
        except (TypeError, ProgrammingError):
            flash('오류가 발생하여 입력이 되지 않았습니다.', 'error')
            db.session.rollback()
        return redirect(url_prefix + table_name)


def delete_object(table_name, object_id):
    Table = get_table(table_name)
    try:
        object = Table.query.filter_by(**{table_name + '_id': object_id}).first()
        db.session.delete(object)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return redirect(url_prefix + table_name)


@eduticket.route('/form/<table_name>', methods=['GET', 'POST'])
def form(table_name):
    if request.method == 'GET':
        Form = generate_form(table_name)
        form = Form()
        if form is not None:
            return render_template('form.html', form=form, table=table_name)
        else:
            return 'table %s does not exist.' % table_name
    elif request.method == 'POST':
        temp_object = get_table(table_name)()
        for key in request.form:
            data = request.form[key]
            if data == '':
                data = None
            setattr(temp_object, key, data)
        try:
            db.session.add(temp_object)
            db.session.commit()
        except (TypeError, ProgrammingError):
            flash('오류가 발생하여 입력이 되지 않았습니다.', 'error')
            db.session.rollback()
        return redirect(url_prefix + table_name)


@eduticket.route('/<table_name>/update/<object_id>', methods=['GET', 'POST'])
def update(table_name, object_id):
    return update_object(table_name, object_id)


@eduticket.route('/<table_name>/delete/<int:object_id>')
def delete(table_name, object_id):
    return delete_object(table_name, object_id)
