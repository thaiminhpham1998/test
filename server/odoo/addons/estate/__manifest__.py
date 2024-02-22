{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base','bedrooms', 'living area', 'garage', 'garden'], #bedrooms, living area, garage, garden
    'website': 'https://www.odoo.com/app/estate',
    'author': "Thai Name",
    'category': 'Marketing/Estate',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/mymodule_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
}