from markupsafe import Markup
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from src.basic.data.models import Banner, News
from src.config import settings
from src.session import engine


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if (
            username == settings.admin_username
            and password == settings.admin_password
        ):
            request.session.update({"token": "authorized"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        if request.session.get("token") == "authorized":
            return True

        return False


class BannerAdmin(ModelView, model=Banner):
    name = "Banner"
    name_plural = "Banners"
    icon = "fa-solid fa-image"

    column_list = [
        Banner.id,
        Banner.image,
        Banner.position,
        Banner.name,
        Banner.active,
        Banner.created_at,
        Banner.updated_at,
    ]
    column_sortable_list = [
        Banner.id,
        Banner.position,
        Banner.name,
        Banner.active,
        Banner.created_at,
        Banner.updated_at,
    ]
    column_searchable_list = [
        Banner.name,
        Banner.description,
        Banner.image,
    ]
    column_details_list = [
        Banner.id,
        Banner.image,
        Banner.position,
        Banner.name,
        Banner.description,
        Banner.active,
        Banner.created_at,
        Banner.updated_at,
    ]
    column_default_sort = [(Banner.position, True), (Banner.id, True)]
    form_columns = [
        Banner.image,
        Banner.position,
        Banner.name,
        Banner.description,
        Banner.active,
    ]
    edit_template = "sqladmin/banner_edit.html"
    details_template = "sqladmin/banner_details.html"
    column_formatters = {
        Banner.image: lambda model, attribute: Markup(
            f'<img src="{model.image}" alt="Banner" '
            'style="max-height: 64px; max-width: 160px; '
            'border-radius: 8px; object-fit: cover;" />'
        )
        if model.image
        else ""
    }
    column_formatters_detail = {
        Banner.image: lambda model, attribute: Markup(
            f'<div style="display:flex; flex-direction:column; gap:12px;">'
            f'<img src="{model.image}" alt="Banner" '
            'style="max-height: 240px; max-width: 480px; '
            'border-radius: 12px; object-fit: contain; border: 1px solid #d9e2ec; '
            'padding: 8px; background: #fff;" />'
            f'<a href="{model.image}" target="_blank">{model.image}</a>'
            "</div>"
        )
        if model.image
        else ""
    }


class NewsAdmin(ModelView, model=News):
    name = "News"
    name_plural = "News"
    icon = "fa-solid fa-newspaper"

    column_list = [
        News.id,
        News.image,
        News.position,
        News.name,
        News.active,
        News.created_at,
        News.updated_at,
    ]
    column_sortable_list = [
        News.id,
        News.position,
        News.name,
        News.active,
        News.created_at,
        News.updated_at,
    ]
    column_searchable_list = [
        News.name,
        News.description,
        News.image,
    ]
    column_details_list = [
        News.id,
        News.image,
        News.position,
        News.name,
        News.description,
        News.active,
        News.created_at,
        News.updated_at,
    ]
    column_default_sort = [(News.position, True), (News.id, True)]
    form_columns = [
        News.image,
        News.position,
        News.name,
        News.description,
        News.active,
    ]
    edit_template = "sqladmin/banner_edit.html"
    details_template = "sqladmin/banner_details.html"
    column_formatters = {
        News.image: lambda model, attribute: Markup(
            f'<img src="{model.image}" alt="News" '
            'style="max-height: 64px; max-width: 160px; '
            'border-radius: 8px; object-fit: cover;" />'
        )
        if model.image
        else ""
    }
    column_formatters_detail = {
        News.image: lambda model, attribute: Markup(
            f'<div style="display:flex; flex-direction:column; gap:12px;">'
            f'<img src="{model.image}" alt="News" '
            'style="max-height: 240px; max-width: 480px; '
            'border-radius: 12px; object-fit: contain; border: 1px solid #d9e2ec; '
            'padding: 8px; background: #fff;" />'
            f'<a href="{model.image}" target="_blank">{model.image}</a>'
            "</div>"
        )
        if model.image
        else ""
    }


def setup_admin(app) -> Admin:
    authentication_backend = AdminAuth(secret_key=settings.admin_secret_key)
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
    )
    admin.add_view(BannerAdmin)
    admin.add_view(NewsAdmin)
    return admin
