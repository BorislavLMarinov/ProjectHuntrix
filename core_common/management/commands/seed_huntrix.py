from django.core.management.base import BaseCommand
from core_common.models import Teacher, Parent
from huntrix_game_app.models import DifficultyLevel, MazeTask, ArithmeticTask
from player_app.models import Avatar, KidProfile


class Command(BaseCommand):
    help = 'Seeds the database with KPOP Huntrix starter content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Huntrix data...')
        trainee, _ = DifficultyLevel.objects.get_or_create(
            name="Trainee", multiplier=1.0, color_code="#00FF00"
        )
        idol, _ = DifficultyLevel.objects.get_or_create(
            name="Idol", multiplier=1.5, color_code="#FF007A"
        )
        Teacher.objects.get_or_create(
            username="teacher_rose",
            defaults={
                'password': 'password123',
                'email': 'rose@huntrix.com',
                'age': 25,
                'school_name': 'YG Academy'
            }
        )
        parent_user, _ = Parent.objects.get_or_create(
            username="parent_jimin",
            defaults={
                'password': 'password123',
                'email': 'jimin@huntrix.com',
                'age': 30,
                'relationship_to_kid': 'parent'
            }
        )
        kid_profile, _ = KidProfile.objects.get_or_create(
            name="Young-Su",
            defaults={
                'parent': parent_user,
                'age': 10,
                'total_points': 150,
                'level': 2
            }
        )
        Avatar.objects.get_or_create(
            display_name="Neo-Vocalist",
            kid=kid_profile,
            defaults={
                'style': 'vocal',
                'bio': 'Ready to hit the high notes!'
            }
        )
        MazeTask.objects.get_or_create(
            title="Dance Studio Navigation",
            defaults={
                'difficulty': trainee,
                'description': "Navigate the trainee to the center of the dance floor.",
                'base_points': 20,
                'grid': [
                    [0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0],
                    [1, 1, 0, 1, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0]
                ],
                'end_row': 4,
                'end_col': 4
            }
        )
        ArithmeticTask.objects.get_or_create(
            title="Ticket Sales Subtraction",
            defaults={
                'difficulty': idol,
                'description': "Calculate how many tickets are left for the world tour.",
                'number_a': 50,
                'number_b': 20,
                'operation': '-',
                'base_points': 15
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Huntrix!'))