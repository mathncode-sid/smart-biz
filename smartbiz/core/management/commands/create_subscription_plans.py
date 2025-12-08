from django.core.management.base import BaseCommand
from core.models import SubscriptionPlan


class Command(BaseCommand):
    help = 'Create default subscription plans'

    def handle(self, *args, **options):
        plans = [
            {
                'name': 'Free',
                'description': 'Perfect for getting started with basic inventory and sales tracking.',
                'price': 0,
                'duration_days': 30,
                'features': [
                    'Up to 50 products',
                    'Basic sales tracking',
                    'Limited analytics',
                    'Email support',
                ]
            },
            {
                'name': 'Basic',
                'description': 'Ideal for small businesses managing daily sales and inventory.',
                'price': 499,
                'duration_days': 30,
                'features': [
                    'Up to 500 products',
                    'Advanced sales tracking',
                    'Real-time analytics',
                    'Low stock alerts',
                    'Priority email support',
                ]
            },
            {
                'name': 'Premium',
                'description': 'For growing businesses with advanced needs and priority support.',
                'price': 1499,
                'duration_days': 30,
                'features': [
                    'Unlimited products',
                    'Advanced analytics & reports',
                    'Custom alerts & notifications',
                    'API access',
                    '24/7 priority support',
                    'Multi-user support (coming soon)',
                ]
            },
        ]

        for plan_data in plans:
            features = plan_data.pop('features')
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created subscription plan: {plan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Plan {plan.name} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created/verified subscription plans')
        )
