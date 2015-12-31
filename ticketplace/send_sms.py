# -*- coding: utf-8 -*-

import sys
import threading
import ticketplace.coolsms as coolsms

coolsms_user = 'frigen'
coolsms_password = "c00lsmsticketp1ace"

SMS_MAX_LENGTH = 90


def send_sms(phone_number, text, sent_by='02-18006403', *, debug=False):
    """

    :param phone_number: 발신번호
    :param text: 내용
    :param sent_by: 수신번호
    :param debug: True일경우 실제로 문자를 보내지 않고 콘솔에 출력만 함
    return:
    """
    if debug:
        print('sending text to %s by %s: %s' % (phone_number, text, sent_by))
        return

    def send_sms_thread(phone_number, text, sent_by, *, debug):
        is_lms = len(bytes(text, 'euc-kr')) > SMS_MAX_LENGTH
        cs = coolsms.sms()
        cs.setuser(coolsms_user, coolsms_password)
        if is_lms:
            print('sending lms', text)
            cs.addlms(phone_number, sent_by, '[에듀티켓]', text)
        else:
            print('sending sms : ', text)
            cs.addsms(phone_number, sent_by, text)
        if cs.connect():
            cs.send()  # 리턴값 받아서 디버그 가능
        else:
            print("서버에 접속할 수 없습니다. 네트워크 상태를 확인하세요.")

        # 연결 해제
        cs.disconnect()
        cs.printr()

    # Spawn nonblocking thread
    thread = threading.Thread(target=send_sms_thread, args=(phone_number, text, sent_by), kwargs={'debug': debug})
    thread.start()

if __name__ == '__main__':
    try:
        send_sms(phone_number=sys.argv[1], text=' '.join(sys.argv[2:]))
    except TypeError:
        print('Usage: send_sms.py phone_number text [sent_by]')
