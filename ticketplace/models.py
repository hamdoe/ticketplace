from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Text
from ticketplace.utils import kst_now

db = SQLAlchemy()

# Define many-to-many association table
tag_association_table = Table('tag_association',
                              db.Model.metadata,
                              Column('content_id', Integer, ForeignKey('content.id')),
                              Column('tag_id', Integer, ForeignKey('tag.id')),
                              PrimaryKeyConstraint('content_id', 'tag_id')
                              )


class Company(db.Model, UserMixin):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, doc='company pk', nullable=False)

    account_bank_code = Column(Text, doc='계좌 은행 코드')
    account_name = Column(Text, doc='예금주')
    account_number = Column(Text, doc='계좌 번호')
    address1 = Column(Text, doc='기본 주소')
    address2 = Column(Text, doc='상세 주소')
    business_license = Column(Text, doc='사업자등록증 파일 경로')
    company_number = Column(Text, doc='사업자 등록번호', nullable=False)
    created_date = Column(DateTime(timezone=True), doc='가입 일자', default=kst_now)
    mail_order_number = Column(Text, doc='통신판매업 신고번호')
    manager_email = Column(Text, doc='담당자 이메일', nullable=False)
    manager_name = Column(Text, doc='담당자 이름', nullable=False)
    manager_phone = Column(Text, doc='담당자 연락처', nullable=False)
    modified_date = Column(DateTime(timezone=True), doc='정보수정 일자', default=kst_now)
    name = Column(Text, doc='회사 이름, 상호명', nullable=False)
    note = Column(Text, doc='비고')
    password = Column(Text, doc='패스워드', nullable=False)
    postcode = Column(Text, doc='신규 우편번호')
    represent_email = Column(Text, doc='대표자 이메일')
    represent_name = Column(Text, doc='대표자 이름')
    represent_phone = Column(Text, doc='대표자 연락처')
    status = Column(Integer, doc='상태', default=0)
    tax_type = Column(Integer, doc='과세 유형', default=0)
    type = Column(Integer, doc='사업자 유형', nullable=False)
    username = Column(Text, unique=True, doc='아이디', nullable=False)
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
        return '<Company(%d): %s>' % (self.id or 0, self.name)


class Content(db.Model):
    id = Column(Integer, primary_key=True, doc='content pk', nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'), doc='제작사 키', nullable=False)

    actor_change = Column(Integer, default=0, doc='배우 변경 여부', nullable=False)
    mininum_age = Column(Integer, doc='최소 적합 연령')
    capacity = Column(Integer, doc='좌석 수', nullable=False)
    created_date = Column(DateTime(timezone=True), doc='생성 일자', default=kst_now)
    description = Column(Text, doc='공연 줄거리', nullable=False)
    duration = Column(Integer, doc='러닝 타임 (분 단위)', nullable=False)
    fee = Column(Integer, doc='수수료 (단위: 원)')
    genre = Column(Integer, doc='공연종류. 0: 공연 1: 전시', nullable=False)
    image_index = Column(Text, doc='메인 페이지용 이미지')
    image_background = Column(Text, doc='상품 설명 배경 이미지')
    image_main = Column(Text, doc='상품 설명 메인 이미지')
    image_thumbnail = Column(Text, doc='썸네일 이미지')
    info_bus_parking = Column(Text, doc='단체 버스 주차안내')
    info_eduticket = Column(Text, doc='에듀티켓안내')
    info_details = Column(Text, doc='관람안내')
    info_time = Column(Text, doc='공연시간안내')
    info_refund = Column(Text, doc='환불규정안내')
    info_transportation = Column(Text, doc='대중교통 안내')
    info_seat = Column(Text, doc='좌석 배치 방법')
    inquire_number = Column(Text, doc='문의전화', nullable=False)
    invitation_ticket_number = Column(Text, doc='초대권 제공 수량', nullable=False)
    location = Column(Integer, doc='0: 서울 1: 경기 2: 부산', nullable=False)
    manager_email = Column(Text, doc='담당자 연락처', nullable=False)
    manager_name = Column(Text, doc='담당자 이름', nullable=False)
    manager_phone = Column(Text, doc='담당자 핸드폰 번호', nullable=False)
    name = Column(Text, doc='제목', nullable=False)
    note = Column(Text, doc='비고')
    original_price = Column(Integer, doc='정가(할인전)', nullable=False)
    price = Column(Integer, doc='가격 (1인 기준)', nullable=False)
    status = Column(Integer, doc='status 명세', nullable=False)
    subname = Column(Text, doc='부제목')
    tags = relationship('Tag', secondary=tag_association_table)
    teacher_ticket_number = Column(Text, doc='인솔자표 제공량 ex) 20명당 1매', nullable=False)
    theater_address1 = Column(Text, doc='극장 주소', nullable=False)
    theater_address2 = Column(Text, nullable=False)
    theater_name = Column(Text, doc='극장 이름', nullable=False)
    theater_postcode = Column(Text, doc='극장 우편번호')
    start_date = Column(DateTime(timezone=True), doc='콘텐츠 시작 일자')

    end_date = Column(DateTime(timezone=True), doc='콘텐츠 종료 일자')

    @property
    def theater_address(self):
        return self.theater_address1 + ' ' + self.theater_address2

    @property
    def discount_rate(self):
        return (self.original_price - self.price) / self.original_price

    def __repr__(self):
        # 직접 객체 생성시 primary key가 아직 부여되지 않았을 수도 있다.
        return '<Content(%d): %s>' % (self.id or 0, self.name)


class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return '<Tag(%d): %s>' % (self.id or 0, self.name)

