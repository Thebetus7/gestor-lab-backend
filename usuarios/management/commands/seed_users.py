from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from usuarios.models import CustomUser

class Command(BaseCommand):
    help = 'Crea usuarios semilla y sus roles básicos'

    def handle(self, *args, **options):
        # Crear grupos base (roles)
        admin_group, _ = Group.objects.get_or_create(name='admin')
        operador_group, _ = Group.objects.get_or_create(name='operador')

        # Crear o actualizar usuario admin
        admin_user, created_admin = CustomUser.objects.get_or_create(username='admin_test')
        if created_admin:
            admin_user.set_password('Admin1234!')
            admin_user.save()
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Usuario admin_test creado con éxito'))
        else:
            self.stdout.write('El usuario admin_test ya existe')

        # Crear o actualizar usuario operador
        op_user, created_op = CustomUser.objects.get_or_create(username='operador_test')
        if created_op:
            op_user.set_password('Operador1234!')
            op_user.save()
            op_user.groups.add(operador_group)
            self.stdout.write(self.style.SUCCESS('Usuario operador_test creado con éxito'))
        else:
            self.stdout.write('El usuario operador_test ya existe')
