from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from usuarios.autenticacion.models import CustomUser

class Command(BaseCommand):
    help = 'Crea usuarios semilla y sus roles básicos'

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='admin')
        operador_group, _ = Group.objects.get_or_create(name='operador')

        admin_user, created_admin = CustomUser.objects.get_or_create(username='admin')
        if created_admin:
            admin_user.set_password('admin12345')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Usuario admin creado con éxito'))
        else:
            admin_user.set_password('admin12345')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write('El usuario admin ya existe (credenciales actualizadas)')

        op_user, created_op = CustomUser.objects.get_or_create(username='operador_test')
        if created_op:
            op_user.set_password('Operador1234!')
            op_user.save()
            op_user.groups.add(operador_group)
            self.stdout.write(self.style.SUCCESS('Usuario operador_test creado con éxito'))
        else:
            self.stdout.write('El usuario operador_test ya existe')

        # Auxiliares de acceso rápido
        auxiliar_group, _ = Group.objects.get_or_create(name='auxiliar')
        for username in ['auxBeto', 'auxJuan']:
            aux_user, created_aux = CustomUser.objects.get_or_create(username=username)
            aux_user.set_password('auxiliar123')
            aux_user.is_active = True
            aux_user.is_deleted = False
            aux_user.save()
            aux_user.groups.add(auxiliar_group)
            if created_aux:
                self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado con éxito'))
            else:
                self.stdout.write(f'El usuario {username} ya existe (credenciales actualizadas y activado)')
