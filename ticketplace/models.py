from flask.ext.login import AnonymousUserMixin
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Text
from ticketplace.utils import kst_now
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import Email

db = SQLAlchemy()

# Define many-to-many association table
tag_association_table = Table('tag_association',
                              db.Model.metadata,
                              Column('content_id', Integer, ForeignKey('content.content_id')),
                              Column('tag_id', Integer, ForeignKey('tag.id')),
                              PrimaryKeyConstraint('content_id', 'tag_id')
                              )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Company(db.Model, UserMixin):
    __tablename__ = 'company'
    company_id = Column(Integer, primary_key=True, doc='company pk', nullable=False)
    account_bank_code = Column(String(255), doc='계좌 은행 코드', nullable=True, info={
        'label': '계좌 은행 코드',
        'description': '계좌가 개설된 은행의 고유 코드'
    })
    account_name = Column(String(255), doc='예금주', nullable=True, info={
        'label': '예금주',
        'description': '제작사 은행계좌의 예금주'
    })
    account_number = Column(String(255), doc='계좌 번호', nullable=True, info={
        'label': '계좌 번호',
        'description': '제작사의 계좌 번호'
    })
    address1 = Column(String(255), doc='기본 주소', nullable=True, info={
        'label': '기본 주소',
        'description': '제작사의 기본 주소'
    })
    address2 = Column(String(255), doc='상세 주소', nullable=True, info={
        'label': '상세 주소',
        'description': '제작사의 상세 주소'
    })
    business_license = Column(String(255), doc='사업자등록증 파일 경로', nullable=True, info={
        'label': '사업자등록증 파일 경로',
        'description': '사업자등록증 파일 경로. amazon s3로 업로드 받는다.'
    })
    company_name = Column(String(255), doc='회사 이름, 상호명', nullable=False, info={
        'label': '회사 이름, 상호명'
    })
    company_number = Column(String(255), doc='사업자 등록번호', nullable=False, info={
        'label': '사업자 등록번호'
    })
    company_type = Column(Integer, doc='사업자 유형', nullable=False, info={
        'label': '사업자 유형',
        'description': '0: 개인 사업자, 1: 법인 사업자'
    })
    created_date = Column(DateTime(timezone=True), doc='가입 일자', default=kst_now, info={
        'label': '가입 일자',
        'description': '가입 일자(자동생성)'
    })
    id = Column(String(255), unique=True, doc='아이디', nullable=False, info={
        'label': '아이디',
        'description': '아이디는 4글자에서 12글자 영문, 숫자로 한다.'
    })
    mail_order_number = Column(String(255), doc='통신판매업 신고번호', nullable=True, info={
        'label': '통신판매업 신고번호'
    })
    manager_email = Column(String(255), doc='담당자 이메일', nullable=False, info={
        'label': '담당자 이메일',
        'validators': Email()
    })
    manager_name = Column(String(255), doc='담당자 이름', nullable=False, info={
        'label': '담당자 이름'
    })
    manager_phone = Column(String(255), doc='담당자 연락처', nullable=False, info={
        'label': '담당자 연락처'
    })
    modified_date = Column(DateTime(timezone=True), doc='정보수정 일자', default=kst_now, info={
        'label': '정보수정 일자',
        'description': '제작사 정보수정 일자'
    })
    note = Column(Text, nullable=True, info={
        'label': '비고'
    })
    password = Column(String(255), doc='패스워드', nullable=False, info={
        'label': '패스워드',
        'description': 'hash 값을 저장한다.'
    })
    postcode1 = Column(Integer, doc='우편번호 1', nullable=True, info={
        'label': '우편번호 1'
    })
    postcode2 = Column(Integer, doc='우편번호 2', nullable=True, info={
        'label': '우편번호 2'
    })
    represent_email = Column(String(255), doc='대표자 이메일', nullable=True, info={
        'label': '대표자 이메일'
    })
    represent_name = Column(String(255), doc='대표자 이름', nullable=True, info={
        'label': '대표자 이름'
    })
    represent_phone = Column(String(255), doc='대표자 연락처', nullable=True, info={
        'label': '대표자 연락처'
    })
    status = Column(Integer, doc='상태', default=0, info={
        'label': 'status',
        'description': '제작사 계정의 상태. 0: 정상, 1: 계약서 작성됨, 2: 약관동의 필요'
    })
    tax_type = Column(Integer, doc='과세 유형', default=0, info={
        'label': '과세 유형',
        'description': '0: 일반, 1: 면세, 2: 간이'
    })
    content_list = relationship('Content', backref='company', lazy='dynamic')

    # for login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Company(%d): %s>' % (self.company_id or 0, self.company_name)


class Content(db.Model):
    content_id = Column(Integer, primary_key=True, doc='content pk', nullable=False)
    company_id = Column(Integer, ForeignKey('company.company_id'), doc='제작사 키', nullable=False, info={
        'label': '제작사',
        'description': '제작사의 pk'
    })
    account_bank_code = Column(String(255), doc='대표 은행 코드', nullable=False, info={
        'label': '대표 은행 코드'
    })
    account_name = Column(String(255), doc='예금주', nullable=False, info={
        'label': '예금주'
    })
    account_number = Column(String(255), doc='계좌 번호', nullable=False, info={
        'label': '계좌 번호'
    })
    actor_change = Column(Integer, default=0, doc='배우 변경 여부', nullable=False, info={
        'label': '배우 변경 여부',
        'description': '0 : 바뀌지 않음, 1 : 바뀜'
    })
    age_max = Column(Integer, doc='최대 적합 연령', nullable=False, info={
        'label': '최대 적합 연령'
    })
    age_min = Column(Integer, doc='최소 적합 연령', nullable=False, info={
        'label': '최소 적합 연령'
    })
    background_image = Column(String(255), doc='상품 설명 배경 이미지', nullable=True, info={
        'label': '상품 설명 배경 이미지',
        'description': '상품 설명 배경 이미지 링크'
    })
    #TODO: block_image = Column(String(255), nullable=True)
    bus_parking_info = Column(Text, doc='단체 버스 주차안내', nullable=False, info={
        'label': '단체 버스 주차안내'
    })
    capacity = Column(Integer, doc='좌석 수', nullable=False, info={
        'label': '좌석 수'
    })
    created_date = Column(DateTime(timezone=True), doc='생성 일자', default=kst_now, info={
        'label': '생성 일자',
        'description': '생성 일자(자동생성)'
    })
    description = Column(Text, doc='공연 줄거리', nullable=False, info={
        'label': '공연 줄거리'
    })
    duration = Column(Integer, doc='러닝 타임 (분 단위)', nullable=False, info={
        'label': '러닝 타임 (분 단위)'
    })
    fee = Column(Integer, doc='수수료 (단위: 원)', nullable=True, info={
        'label': '수수료 (단위: 원)'
    })
    genre = Column(Integer, doc='공연종류. 0: 공연 1: 전시', nullable=False, info={
        'label': '공연종류',
        'description': '0: 공연, 1: 전시'
    })
    index_image = Column(String(255), doc='메인 페이지용 이미지', nullable=True, info={
        'label': '메인 페이지용 이미지'
    })
    information1 = Column(Text, doc='에듀티켓안내', nullable=True, info={
        'label': '에듀티켓안내'
    })
    information2 = Column(Text, doc='이용안내', nullable=True, info={
        'label': '이용안내'
    })
    information3 = Column(Text, doc='관람안내', nullable=True, info={
        'label': '관람안내'
    })
    information4 = Column(Text, doc='공연시간안내', nullable=True, info={
        'label': '공연시간안내'
    })
    information5 = Column(Text, doc='환불규정안내', nullable=True, info={
        'label': '환불규정안내'
    })
    information_file = Column(String(255), doc='zip파일', nullable=True, info={
        'label': 'zip파일'
    })
    inquire_number = Column(String(255), doc='문의전화', nullable=False, info={
        'label': '문의전화'
    })
    invitation_ticket_number = Column(String(255), doc='초대권 제공 수량', nullable=False, info={
        'label': '초대권 제공 수량'
    })
    landing_ad = Column(Integer, doc='랜딩 페이지 광고 여부0: 신청하지 않음1: 신청함', nullable=False, info={
        'label': '랜딩 페이지 광고 여부',
        'description': '0: 신청하지 않음, 1: 신청함'
    })
    latitude = Column(Float, doc='위도', nullable=True, info={
        'label': '위도'
    })
    location = Column(Integer, doc='0: 서울 1: 경기 2: 부산', nullable=False, info={
        'label': '도시',
        'description': '0: 서울 1: 경기 2: 부산'
    })
    longitude = Column(Float, doc='경도', nullable=True, info={
        'label': '경도'
    })
    main_image = Column(String(255), doc='상품 설명 메인 이미지', nullable=True, info={
        'label': '상품 설명 메인 이미지'
    })
    manager_email = Column(String(255), doc='담당자 연락처', nullable=False, info={
        'label': '담당자 연락처'
    })
    manager_name = Column(String(255), doc='담당자 이름', nullable=False, info={
        'label': '담당자 이름'
    })
    manager_phone = Column(String(255), doc='담당자 핸드폰 번호', nullable=False, info={
        'label': '담당자 핸드폰 번호'
    })
    modified_date = Column(DateTime(timezone=True), doc='수정 일자', default=kst_now, info={
        'label': '수정 일자',
        'description': '수정 일자(자동 생성)'
    })
    name = Column(String(255), doc='제목', nullable=False, info={
        'label': '제목'
    })
    note = Column(Text, nullable=True)
    original_price = Column(Integer, doc='정가(할인전)', nullable=False, info={
        'label': '정가(할인전)'
    })
    price = Column(Integer, doc='가격 (1인 기준)', nullable=False, info={
        'label': '가격 (1인 기준)'
    })
    resolved_money = Column(Integer, doc='정산 금액', default=0, info={
        'label': '정산 금액'
    })
    resolved_note = Column(String(255), doc='정산 내역', nullable=True, info={
        'label': '정산 내역'
    })
    seating_arrangement = Column(Text, doc='좌석 배치 방법', nullable=False, info={
        'label': '좌석 배치 방법'
    })
    status = Column(Integer, doc='status 명세', nullable=False, info={
        'label': 'status',
        'description': '0: 작성 중, 1: 등록 신청 중, 2: 등록 완료 및 판매 중, 3: 마감 및 기간 만료'
    })
    subname = Column(String(255), doc='부제목', nullable=True, info={
        'label': '부제목'
    })
    tags = relationship('Tag', secondary=tag_association_table)
    teacher_ticket_number = Column(String(255), doc='인솔자표 제공량 ex) 20명당 1매', nullable=False, info={
        'label': '인솔자표 제공량',
        'description': '인솔자표 제공량 ex) 20명당 1매'
    })
    theater_address1 = Column(String(255), doc='극장 주소', nullable=False, info={
        'label': '극장 주소'
    })
    theater_address2 = Column(String(255), nullable=False, info={
        'label': '극장 세부주소'
    })
    theater_name = Column(String(255), doc='극장 이름', nullable=False, info={
        'label': '극장 이름'
    })
    theater_postcode1 = Column(Integer, doc='극장 우편번호', nullable=False, info={
        'label': '극장 우편번호1'
    })
    theater_postcode2 = Column(Integer, nullable=False, info={
        'label': '극장 우편번호2'
    })
    thumbnail_image = Column(String(255), doc='썸네일 이미지', nullable=True, info={
        'label': '썸네일 이미지'
    })
    transportation_info = Column(Text, doc='대중교통 안내', nullable=False, info={
        'label': '대중교통 안내'
    })
    start_date = Column(DateTime(timezone=True), doc='콘텐츠 시작 일자')

    end_date = Column(DateTime(timezone=True), doc='콘텐츠 종료 일자')

    def __repr__(self):
        # 직접 객체 생성시 primary key가 아직 부여되지 않았을 수도 있다.
        return '<Content(%d): %s>' % (self.content_id or 0, self.name)

    @property
    def discount_rate(self):
        return (self.original_price - self.price) / self.original_price


class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return '<Tag(%d): %s>' % (self.id or 0, self.name)

