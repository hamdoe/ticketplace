from flask.ext.admin.contrib.sqla.view import ModelView


class CompanyView(ModelView):
    """ Admin view for `Company` """
    can_view_details = True
    column_list = ['company_id', 'company_name', 'id', 'represent_name', 'represent_phone', 'represent_email', 'manager_name', 'manager_phone', 'manager_email', 'note']
    column_searchable_list = [column for column in column_list if column not in ['company_id']]


class ContentView(ModelView):
    """ Admin view for `Content` """
    can_view_details = True
    column_list = ['content_id', 'name', 'company.company_name', 'original_price', 'price', 'content_start_date', 'content_end_date', 'manager_name', 'manager_phone', 'manager_email', 'inquire_number', 'status', 'note']
    column_searchable_list = [column for column in column_list if column not in ['content_id', 'company']]
