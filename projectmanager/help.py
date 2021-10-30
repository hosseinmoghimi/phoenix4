from .apps import APP_NAME
sidebar_links = [

    {
        'app_name': APP_NAME,
        'title': 'مدیریت پروژه',
        'template': 'index',
        'childs': [
            {
                'app_name': APP_NAME,
                'title': 'لیست 1',
                'template': 'add_location'
            },
            {
                'app_name': APP_NAME,
                'title': 'لیست 2',
                'template': 'add_location'
            },
        ]
    },
    {
        'app_name': APP_NAME,
        'title': 'افزودن لوکیشن برای پروژه',
        'template': 'add_location'
    },
    {
        'app_name': APP_NAME,
        'title': 'افزودن کارفرما',
        'template': 'add_employer'
    },
    {
        'app_name': APP_NAME,
        'title': 'افزودن پرسنل',
        'template': 'add_employee'
    },
    {
        'app_name': APP_NAME,
        'title': 'افزودن برگه انبارداری',
        'template': 'add-material-sheet'
    },

]
