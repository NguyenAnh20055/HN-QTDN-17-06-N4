# -*- coding: utf-8 -*-
{
    'name': "quan_ly_van_ban",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','nhan_su','quan_ly_khach_hang'],

    'data': [
    'security/ir.model.access.csv',
    
    'data/sequence.xml', 
    
    'views/danh_sach_van_ban_views.xml',
    'views/loai_van_ban_views.xml',
    'views/van_ban_den_views.xml',
    'views/van_ban_di_views.xml',
    'views/van_ban_noi_bo_views.xml',
    'views/ai_tim_kiem_views.xml',
    'data/dashboard_data.xml',
    'views/dashboard_van_ban.xml',
    'views/khach_hang_inherit_views.xml',
    'views/menu.xml',
    
    ],  
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
