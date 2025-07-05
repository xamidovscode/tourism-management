JAZZMIN_SETTINGS = {

    "site_title": "Magical Deserts Tours",
    "site_header": "Magical Deserts Tours",
    "site_brand": "MD Tours",
    "site_logo": "images/logo.png",
    "login_logo": "images/login.png",
    "login_logo_dark": "images/login.png",

    "welcome_sign": "Welcome to MD Tours Management System👋",
    "copyright": "© 2025 IMB Technologies",

    "show_sidebar": True,
    "navigation_expanded": True,

    "changeform_format": "horizontal_tabs",

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "tours"},
    ],

    "order_with_respect_to": ["sales", "tours", "common"],

    "icons": {
        "admin.LogEntry": "fas fa-book",
        "auth.Permission": "fas fa-key",
        "auth.Group": "fas fa-users",
        "contenttypes.ContentType": "fas fa-layer-group",
        "sessions.Session": "fas fa-clock",

        "common.TourType": "fas fa-map-signs",
        "common.TransferType": "fas fa-exchange-alt",
        "common.Currency": "fas fa-dollar-sign",
        "common.Hotel": "fas fa-hotel",
        "common.Adult": "fas fa-child",
        "common.Child": "fas fa-child",
        "common.Market": "fas fa-globe",

        "tours.Tour": "fas fa-route",
        "tours.TourAgePrice": "fas fa-child",
        "tours.TourExtraPrice": "fas fa-plus-circle",

        "users.CustomUser": "fas fa-user",

        "sales.Customer": "fas fa-user-friends",
        "sales.Sale": "fas fa-money-bill-wave",
        "sales.TourProxy": "fas fa-route",
        "sales.SaleProxy": "fas fa-receipt",
    },


    "show_collapsed": True,


    "use_google_fonts_cdn": True,

    "custom_js": None,
    "custom_css": "css/main.css",

    "changeform_format": "horizontal_tabs",  # optional
    "show_ui_builder": False,

    "hide_apps": [
        "auth", 'apps.common'
    ],
    "hide_models": ["auth.Group"],
}


JAZZMIN_UI_TWEAKS = {
    "theme": "lux",

}