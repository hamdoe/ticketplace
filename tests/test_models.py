#! ../env/bin/python
# -*- coding: utf-8 -*-

import datetime
import pytest

from ticketplace.models import db, User, Company, Content
from ticketplace.utils import kst_now

create_user = False


@pytest.mark.usefixtures("testapp")
class TestModels:
    def test_user_save(self, testapp):
        """ Test Saving the user model to the database """

        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

        user = User.query.filter_by(username="admin").first()
        assert user is not None

    def test_user_password(self, testapp):
        """ Test password hashing and checking """

        admin = User('admin', 'supersafepassword')

        assert admin.username == 'admin'
        assert admin.check_password('supersafepassword')


@pytest.mark.usefixtures("testapp")
class TestCompany:
    def setup(self):
        example_company = Company(company_name='(주)티켓플레이스',
                              id='ticketplace',
                              manager_email='june@ticketplace.net',
                              manager_name='Minjune Kim',
                              manager_phone='010-1234-5678',
                              password='1234',
                              company_number='012-34-56789',
                              company_type=0)
        db.session.add(example_company)
        db.session.commit()

    def teardown(self):
        company = Company.query.filter_by(id='ticketplace').first()
        db.session.delete(company)
        db.session.commit()

    def test_company_save(self):
        company = Company.query.filter_by(company_name='(주)티켓플레이스').first()
        assert company is not None

    def test_company_created_date(self):
        company = Company.query.filter_by(id='ticketplace').first()
        assert kst_now() - company.created_date < datetime.timedelta(hours=1)


@pytest.mark.usefixtures("testapp")
class TestContent:
    def setup(self):
        example_company = Company(company_name='(주)티켓플레이스',
                                  id='ticketplace',
                                  manager_email='june@ticketplace.net',
                                  manager_name='Minjune Kim',
                                  manager_phone='010-1234-5678',
                                  password='1234',
                                  company_number='012-34-56789',
                                  company_type=0)
        db.session.add(example_company)
        db.session.commit()
        example_content = Content(company_id=example_company.company_id,
                                  account_bank_code='001',
                                  account_name='김예금',
                                  account_number='277-054112-01-015',
                                  age_max=18,
                                  age_min=7,
                                  bus_parking_info='bus_parking_info',
                                  capacity=100,
                                  description='',
                                  duration=50,
                                  genre=0,
                                  inquire_number='010-1234-5768',
                                  invitation_ticket_number='',
                                  landing_ad=0,
                                  location=0,
                                  manager_email='frigen@naver.com',
                                  manager_name='김담당',
                                  manager_phone='010-1234-5768',
                                  name='공연명',
                                  original_price=10000,
                                  price=5000,
                                  seating_arrangement='',
                                  status=0,
                                  teacher_ticket_number='',
                                  theater_address1='',
                                  theater_address2='',
                                  theater_name='',
                                  theater_postcode1=1,
                                  theater_postcode2=1,
                                  transportation_info=''
                                  )
        db.session.add(example_content)
        db.session.commit()

    def teardown(self):
        content = Content.query.filter_by(name='공연명').first()
        db.session.delete(content)
        company = Company.query.filter_by(id='ticketplace').first()
        db.session.delete(company)
        db.session.commit()

    def test_content_save(self):
        content = Content.query.filter_by(name='공연명').first()
        company = content.company
        assert content is not None
        assert company is not None

    def test_propertied(self):
        content = Content.query.filter_by(name='공연명').first()
        assert content.discount_rate == 0.5