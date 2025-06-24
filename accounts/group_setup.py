from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import Product, Order
from django.apps import AppConfig

def run():
    customer_group, _ = Group.objects.get_or_create(name='Customer')
    manager_group, _ = Group.objects.get_or_create(name='StoreManager')

    product_ct = ContentType.objects.get_for_model(Product)
    order_ct = ContentType.objects.get_for_model(Order)
    
    for codename in ['add', 'change', 'delete', 'view']:
        Permission.objects.get_or_create(
            codename=f'{codename}_product',
            content_type=product_ct,
            defaults={'name': f'Can {codename} product'}
        )
        Permission.objects.get_or_create(
            codename=f'{codename}_order',
            content_type=order_ct,
            defaults={'name': f'Can {codename} order'}
        )

    manager_group.permissions.set(Permission.objects.filter(
        content_type__in=[product_ct, order_ct]
    ))

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .group_setup import run
        run() 