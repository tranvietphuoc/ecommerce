from ecommerce.extensions import db


class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f"<Role('{self.id}', '{self.role_name}')>"


class RoleMixin:
    def __init__(self, *args):
        pass

    def has_role(self, *args):
        """Utility for checking Roles."""

        set_args = {arg for arg in args}  # set comprehension
        role_query = {role.role_name for role in self.roles}
        return role_query.issubset(set_args)
