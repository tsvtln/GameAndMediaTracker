from django.core.management.base import BaseCommand
from CheckPoint.common.models import Board


class Command(BaseCommand):
    help = 'Populates the forum boards'

    def handle(self, *args, **options):
        boards_data = [
            {
                'name': 'Emulator Help',
                'slug': 'emulator-help',
                'description': 'Get help with emulator issues and configurations'
            },

            {
                'name': 'BIOS Help',
                'slug': 'bios-help',
                'description': 'BIOS installation and troubleshooting support'
            },

            {
                'name': 'Other',
                'slug': 'other',
                'description': 'Other support topics'
            },

            {
                'name': 'Retro Gaming',
                'slug': 'retro-gaming',
                'description': 'Discuss classic games and retro gaming culture'
            },

            {
                'name': 'PC Gaming',
                'slug': 'pc-gaming',
                'description': 'PC gaming discussions'},
            {
                'name': 'Off Topic',
                'slug': 'off-topic',
                'description': 'General discussions and off-topic conversations'
            },

            {
                'name': 'Game Guides',
                'slug': 'game-guides',
                'description': 'Walkthroughs and game guides'
            },

            {
                'name': 'Emulator Setup',
                'slug': 'emulator-setup',
                'description': 'Step-by-step emulator setup guides'
            },

            {
                'name': 'BIOS Setup',
                'slug': 'bios-setup',
                'description': 'BIOS installation and setup guides'
            },
        ]

        created_count = 0
        updated_count = 0

        for board_data in boards_data:
            board, created = Board.objects.get_or_create(
                slug=board_data['slug'],
                defaults={
                    'name': board_data['name'],
                    'description': board_data['description']
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created board: {board.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Board already exists: {board.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nForum has been populated! Created: {created_count}, Already existed: {updated_count}'
        ))
