from flask.ext.admin.contrib.sqla.view import ModelView


class CompanyView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_exclude_list = ['account_bank_code', 'account_name', 'account_number', 'address1', 'address2', 'business_license', 'company_number', 'company_type', 'created_date', 'mail_order_number', 'modified_date', 'password', 'postcode1', 'postcode2', 'status', 'tax_type']


class ContentView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_exclude_list = ['account_bank_code', 'account_name', 'account_number', 'actor_change', 'age_max', 'age_min', 'background_image', 'bus_parking_info', 'capacity', 'created_date', 'description', 'created_date', 'description', 'duration', 'fee', 'genre', 'index_image', 'information1', 'information2', 'information3', 'information4', 'information5', 'information_file', 'invitation_ticket_number', 'landing_ad', 'latitude', 'location', 'longitude', 'main_image', 'modified_date', 'seating_arrangement', 'teacher_ticket_number', 'theater_address1', 'theater_address2', 'theater_postcode1', 'theater_postcode2', 'thumbnail_image', 'transportation_info']
