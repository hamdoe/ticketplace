#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
from ticketplace.models import Company, Content, db

create_user = True


@pytest.mark.usefixtures("testapp")
class TestURLs:
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

        self.example_company = example_company
        self.example_content = example_content

    def teardown(self):
        content = Content.query.filter_by(name='공연명').first()
        db.session.delete(content)
        company = Company.query.filter_by(username='ticketplace').first()
        db.session.delete(company)
        db.session.commit()

    def test_home(self, testapp):
        """ Tests if the home page loads """

        rv = testapp.get('/')
        assert rv.status_code == 200

    def test_detail(self, testapp):
        """ Tests if the detail page loads """
        content = Content.query.first()
        rv = testapp.get('/detail/%d' % content.id)
        assert rv.status_code == 200

    def test_reservation(self, testapp):
        """Test if reservation page loads"""
        content = Content.query.first()
        rv = testapp.get('/reservation/%d' % content.id)
        assert rv.status_code == 200
        assert content.name.encode() in rv.data

    def test_howto(self, testapp):
        """Test if howto page loads"""
        rv = testapp.get('/howto/')
        assert rv.status_code == 200

    def test_recommend(self, testapp):
        """Test if recommend page loads"""
        rv = testapp.get('/recommend/')
        assert rv.status_code == 200

    def test_list(self, testapp):
        """ Tests if the list page loads """
        example_company = Company.query.first()
        content_for_all = Content(company_id=example_company.id,
                            account_bank_code='001',
                            account_name='김예금',
                            account_number='277-054112-01-015',
                            age_max=14,
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
                            name='content_for_all',
                            original_price=10000,
                            price=5000,
                            seating_arrangement='',
                            status=2,
                            teacher_ticket_number='',
                            theater_address1='',
                            theater_address2='',
                            theater_name='',
                            theater_postcode1=1,
                            theater_postcode2=1,
                            transportation_info=''
                            )
        db.session.add(content_for_all)
        db.session.commit()
        rv = testapp.get('/list/')
        assert rv.status_code == 200
        assert b'content_for_all' in rv.data
        assert b'col-xs-6' in rv.data
        # Test blockview
        rv = testapp.get('/list/?blockview=True')
        assert rv.status_code == 200
        assert b'content_for_all' in rv.data
        assert b'col-xs-4' in rv.data
        db.session.delete(content_for_all)
        db.session.commit()

    # Test Admin URLs
    def test_admin_home(self, testapp):
        """ Test admin page index link """
        rv = testapp.get('/admin/')
        assert rv.status_code == 200

    def test_admin_company(self, testapp):
        """ Test admin Company page """
        rv = testapp.get('/admin/company/')
        assert rv.status_code == 200
        rv = testapp.get('/admin/company/details/?id=%d' % self.example_company.id)
        assert rv.status_code == 200
        rv = testapp.get('/admin/company/edit/?id=%d' % self.example_company.id)
        assert rv.status_code == 200
        rv = testapp.get('/admin/company/new/')
        assert rv.status_code == 200

    def test_admin_content(self, testapp):
        """Test admin Content page """
        rv = testapp.get('/admin/content/')
        assert rv.status_code == 200
        rv = testapp.get('/admin/content/details/?id=%d' % self.example_content.id)
        assert rv.status_code == 200
        rv = testapp.get('/admin/content/edit/?id=%d' % self.example_content.id)
        assert rv.status_code == 200
        rv = testapp.get('/admin/content/new/')
        assert rv.status_code == 200

    def test_admin_image(self, testapp):
        """Test admin Image page"""
        rv = testapp.get('/admin/image/')
        assert rv.status_code == 200
