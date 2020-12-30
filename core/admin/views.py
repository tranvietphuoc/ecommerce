from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import session, redirect, url_for, request, abort, render_template
from flask_login import current_user


class AdminView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        else:
            if current_user.has_role("superuser"):
                return True
            return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when
        a view is not accessible
        """
        if current_user.has_role("superuser"):
            can_export = True
            edit_modal = True
            create_modal = True
            page_size = 20
            details_modal = (True,)
            column_display_pk = True
        else:
            if not self.is_accessible():
                if current_user.is_authenticated:
                    # permission denied
                    abort(403)
                else:
                    # login
                    return redirect(url_for("users.login", next=request.url))


class AdminUserView(AdminView):
    def _handle_view(self, name, **kwargs):
        if current_user.has_role("superuser"):
            can_export = True
        else:
            if not self.is_accessible():
                if current_user.is_authenticated:
                    abort(403)
                else:
                    return redirect(url_for("users.login", next=request.url))
