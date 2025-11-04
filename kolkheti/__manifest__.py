# -*- coding: utf-8 -*-
{
    'name': "kolkheti",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/table.xml',
        'views/clubs.xml',
        'views/employees.xml',
        'views/news.xml',
        'views/lastMatch.xml',
        'views/stadiums.xml',
        'views/nextMatch.xml',
        'views/country.xml',
        'views/stats.xml',
        'views/video.xml',
        'views/photos.xml',
        'views/matches.xml',
        'views/gallery.xml'
    ]
}

