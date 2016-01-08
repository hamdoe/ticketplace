#! ../env/bin/python
# -*- coding: utf-8 -*-

import datetime
import pytest

from ticketplace.models import db, Company, Content
from ticketplace.utils import kst_now

create_user = False


@pytest.mark.usefixtures("testapp")
class TestCompany:
    def setup(self):
        example_company = Company(name='(주)티켓플레이스',
                              username='ticketplace',
                              manager_email='june@ticketplace.net',
                              manager_name='Minjune Kim',
                              manager_phone='010-1234-5678',
                              password='1234',
                              company_number='012-34-56789',
                              type=0)
        db.session.add(example_company)
        db.session.commit()

    def teardown(self):
        company = Company.query.filter_by(username='ticketplace').first()
        db.session.delete(company)
        db.session.commit()

    def test_company_save(self):
        company = Company.query.filter_by(name='(주)티켓플레이스').first()
        assert company is not None

    def test_company_created_date(self):
        company = Company.query.filter_by(username='ticketplace').first()
        assert kst_now() - company.created_date < datetime.timedelta(hours=1)


@pytest.mark.usefixtures("testapp")
class TestContent:
    def setup(self):
        example_company = Company(name='(주)티켓플레이스',
                                  username='ticketplace',
                                  manager_email='june@ticketplace.net',
                                  manager_name='Minjune Kim',
                                  manager_phone='010-1234-5678',
                                  password='1234',
                                  company_number='012-34-56789',
                                  type=0)
        db.session.add(example_company)
        db.session.commit()
        example_content = Content(company_id=example_company.id,
                                  mininum_age=7,
                                  info_bus_parking='info_bus_parking',
                                  capacity=100,
                                  description='',
                                  duration=50,
                                  genre=0,
                                  inquire_number='010-1234-5768',
                                  invitation_ticket_number='',

                                  location=0,
                                  manager_email='frigen@naver.com',
                                  manager_name='김담당',
                                  manager_phone='010-1234-5768',
                                  name='공연명',
                                  original_price=10000,
                                  price=5000,
                                  info_seat='',
                                  status=0,
                                  teacher_ticket_number='',
                                  theater_address1='',
                                  theater_address2='',
                                  theater_name='',
                                  theater_postcode='12345',
                                  info_transportation=''
                                  )
        db.session.add(example_content)
        db.session.commit()

    def teardown(self):
        content = Content.query.filter_by(name='공연명').first()
        db.session.delete(content)
        company = Company.query.filter_by(username='ticketplace').first()
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