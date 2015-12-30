"""filters.py

Register filters that can be used in any template files.

"""

from ticketplace.utils import kst_now


def register_filters(app):
    """Register template filters for app"""
    @app.template_filter('number')
    def number_filter(n):
        """ 템플릿 용 숫자 필터. 버림하고 콤마 넣어줌 """
        return '{:,}'.format(int(n))

    @app.template_filter('percent')
    def percent(n):
        """ float비율을 퍼센트로 변경
        """
        return '{:}'.format(int(float(n) * 100))

    @app.template_filter('age')
    def age_filter(age):
        if not age:
            return '전체관람가'
        return '%d세 이상' % age

    @app.template_filter('actor_change')
    def actor_change_filter(actor_change):
        if type(actor_change) == str:
            return actor_change
        else:
            return ['변경 없음', '변경 있음'][actor_change]

    @app.template_filter('datetime')
    def datetime_filter(date, format='%Y/%m/%d(%a) %p %I:%M'):
        """
            템플릿 용 날짜 필터.
        """
        if not date:
            return '없음'

        # windows상의 strftime함수가 유니코드를 못읽어서 날짜를 파싱하고 다시 입력하는 뻘짓을 해야함
        result = format
        tokens = ('%a', '%A', '%b', '%B', '%c', '%d', '%H', '%I', '%j', '%m', '%M',
                  '%p', '%S', '%U', '%w', '%W', '%x', '%X', '%y', '%Y', '%Z', '%%')
        replacements = {token: date.strftime(token) for token in tokens}
        for token, variable in replacements.items():
            result = result.replace(token, variable)

        return result

    @app.template_filter('before')
    def timeago_filter(from_date, to_date=kst_now()):
        interval = to_date - from_date
        interval_second = int(interval.total_seconds())
        if interval_second < 60:
            return str(interval_second) + '초 전'
        elif interval_second < 60 * 60:
            return str(interval_second // 60) + '분 전'
        elif interval_second < 60 * 60 * 24:
            return str(interval_second // (60 * 60)) + '시간 전'
        elif interval_second < 60 * 60 * 24 * 30:
            return str(interval_second // (60 * 60 * 24)) + '일 전'
        elif interval_second < 60 * 60 * 24 * 365:
            return str(interval_second // (60 * 60 * 24 * 30)) + '개월 전'
        else:
            return str(interval_second // (60 * 60 * 24 * 365)) + '년 전'

    @app.template_filter('truncate')
    def truncate_filter(s, length, end='...'):
        """Return a truncated copy of the string."""
        if len(s) <= length:
            return s
        else:
            return s[:length] + end