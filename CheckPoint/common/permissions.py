from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerOrModeratorMixin(UserPassesTestMixin):
    # allow access to staff, moderators or if the object is made by the user
    owner_field = 'uploaded_by'  # default field name for owner

    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        if user.is_staff or user.groups.filter(name='Moderators').exists():
            return True

        # allow if user is the owner
        owner = getattr(obj, self.owner_field, None)
        if owner == user:
            return True
        return False


class ModeratorOnlyMixin(UserPassesTestMixin):
    # allow access to staff and moderators only
    def test_func(self):
        user = self.request.user

        # allow if user is_staff
        if user.is_staff:
            return True

        # allow if user is in Moderators group
        if user.groups.filter(name='Moderators').exists():
            return True
        return False


class ModeratorOrVerifiedMixin(UserPassesTestMixin):
    # allow access to staff, moderators, or verified users
    def test_func(self):
        user = self.request.user
        # allow if user is_staff
        if user.is_staff:
            return True

        # allow if user is in 'Moderators' or 'Verified Users' groups
        if user.groups.filter(name__in=['Moderators', 'Verified Users']).exists():
            return True
        return False
