from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates default user groups with specific permissions'

    def handle(self, *args, **kwargs):
        # Moderators group
        moderators, created = Group.objects.get_or_create(name='Moderators')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Moderators" group'))

            # permissions for moderators
            # they can manage ROMs, BIOS, saves, screenshots, but not users
            perms = Permission.objects.filter(
                codename__in=[
                    'add_rom', 'change_rom', 'delete_rom',
                    'add_bios', 'change_bios', 'delete_bios',
                    'add_save', 'change_save', 'delete_save',
                    'add_screenshot', 'change_screenshot', 'delete_screenshot',
                    'add_comment', 'change_comment', 'delete_comment',
                    'add_review', 'change_review', 'delete_review',
                ]
            )
            moderators.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f'Added {perms.count()} permissions to Moderators'))
        else:
            self.stdout.write(self.style.WARNING('Moderators group already exists'))

        # Regular Users group
        regular_users, created = Group.objects.get_or_create(name='Regular Users')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Regular Users" group'))

            # Add basic permissions for regular users
            # regular users can add their own content and manage their own uploads
            perms = Permission.objects.filter(
                codename__in=[
                    'add_rom', 'change_rom',
                    'add_save', 'change_save',
                    'add_screenshot', 'change_screenshot',
                    'add_comment',
                    'add_review',
                ]
            )
            regular_users.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f'Added {perms.count()} permissions to Regular Users'))
        else:
            self.stdout.write(self.style.WARNING('Regular Users group already exists'))

        # Verified Users group (for users who can upload BIOS files)
        verified_users, created = Group.objects.get_or_create(name='Verified Users')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Verified Users" group'))

            perms = Permission.objects.filter(
                codename__in=[
                    'add_rom', 'change_rom',
                    'add_bios', 'change_bios',
                    'add_save', 'change_save',
                    'add_screenshot', 'change_screenshot',
                    'add_comment',
                    'add_review',
                ]
            )
            verified_users.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f'Added {perms.count()} permissions to Verified Users'))
        else:
            self.stdout.write(self.style.WARNING('Verified Users group already exists'))

        self.stdout.write(self.style.SUCCESS('User groups setup complete!'))

