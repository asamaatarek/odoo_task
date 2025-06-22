{
    'name': 'HMS',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Hospitals Mangement System',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'report/report_templates.xml',
        'report/reports.xml',
        'views/base_menu.xml',
        'views/hms_patient_menu.xml',
        'views/hms_doctors_menu.xml',
        'views/hms_department_menu.xml',
        'views/res_partner_inherit_view.xml',
    ]
}

