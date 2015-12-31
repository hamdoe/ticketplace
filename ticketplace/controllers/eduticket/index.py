from flask.templating import render_template
from ticketplace.controllers.eduticket import eduticket
from ticketplace.models import Content


@eduticket.route('/')
@eduticket.route('/index')
def index():
    # eduticket_reservation_list = ReservationDao.get_all(vendor="에듀티켓")
    # on_sale_content = ContentDao.get_all(status=2)

    # total_paid = 0
    # total_chargeless = 0
    # total_sales = 0
    #
    # for reservation in eduticket_reservation_list:
    #     if(reservation.status in (1,3)):
    #         total_paid += reservation.charged
    #         total_sales += reservation.charged * reservation.price
    #         total_chargeless += reservation.chargeless

    # reservation_count = len(eduticket_reservation_list)
    # on_sale_content_count = len(on_sale_content)


    eduticket_reservation_list = []
    on_sale_content = Content.query.filter_by(status=2).all()
    total_paid = 0
    total_chargeless = 0
    total_sales = 0
    reservation_count = 0
    on_sale_content_count = Content.query.filter_by(status=2).count()
    return render_template('eduticket.html', **locals())
