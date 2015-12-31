from flask import flash, render_template, request
from ticketplace.controllers.eduticket.resources.send_sms import send_sms
from ticketplace.controllers.eduticket import eduticket


@eduticket.route('/sms', methods=['GET', 'POST'])
def sms():
    """ 문자 보내기 관련 스크립트
    sender: 발신번호
    phone: 전화번호
    content: 문자 내용
    preserve_x: 각 x 변수에 대해서 그 값을 유지할 것인지 여부
    """
    sender = request.form.get('sender', '02-18006403', type=str)
    preserve_sender = request.form.get('preserve_sender', True, type=bool)
    phone = request.form.get('phone', '', type=str)
    preserve_phone = request.form.get('preserve_phone', False, type=bool)
    content = request.form.get('content', '', type=str)
    preserve_content = request.form.get('preserve_content', False, type=bool)

    if request.method == 'POST':
        if not phone:
            flash('전화번호를 입력해 주세요', 'error')
            return render_template('sms.html', **locals())
        if not content:
            flash('문자 내용을 입력해 주세요', 'error')
            return render_template('sms.html', **locals())
        if not sender:
            flash('발신번호를 입력해 주세요.', 'error')
            return render_template('sms.html', **locals())

        send_sms(phone, content, sent_by=sender)
        flash('%s에 발신번호 %s로 메세지가 전송되었습니다: %s' % (phone, sender, content))
        return render_template('sms.html', **locals())

    return render_template('sms.html', **locals())
