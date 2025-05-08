from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import Category, Service, Tag
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create categories from category choices and sample services  for each category"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run the command in dry-run mode without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        try:
            self.stdout.write("Starting category and service creation")
            logger.info(f"Executing command with dry_run={dry_run}")

            if dry_run:
                self.stdout.write("Running in dry-run mode - no changes will be made")
                self._preview_categories_and_services()
            else:
                with transaction.atomic():
                    categories = self._create_categories()
                    self._create_services(categories)

            self.stdout.write(self.style.SUCCESS('Command completed successfully'))

        except Exception as e:
            logger.error(f"Error in command: {str(e)}")
            raise CommandError(f"Error executing command: {str(e)}")

    def _create_categories(self):
        """Create categories based on CATEGORY choices"""
        categories = []
        existing_categories = set(Category.objects.values_list('name', flat=True))
        
        for category_name, _ in Category.CATEGORY:
            if category_name not in existing_categories:
                category = Category(name=category_name)
                category.save()
                categories.append(category)
                self.stdout.write(f"Created category: {category_name}")
            else:
                category = Category.objects.get(name=category_name)
                categories.append(category)
                self.stdout.write(f"Category already exists: {category_name}")
        
        return categories

    def _create_services(self, categories):
        """Create 5 sample services for each category"""
        sample_service_names = [
            "Basic Service",
            "Premium Service",
            "Express Service",
            "Professional Service",
            "Standard Service"
        ]

        for category in categories:
            existing_services = set(Service.objects.filter(category=category).values_list('name', flat=True))
            
            for service_name in sample_service_names:
                full_service_name = f"{category.name} {service_name}"
                if full_service_name not in existing_services:
                    service = Service(
                        name=full_service_name,
                        category=category
                    )
                    service.save()
                    self.stdout.write(f"Created service: {full_service_name} in {category.name}")
                else:
                    self.stdout.write(f"Service already exists: {full_service_name} in {category.name}")

    def _preview_categories_and_services(self):
        """Preview what would be created in dry-run mode"""
        self.stdout.write("Categories that would be created or used:")
        for category_name, _ in Category.CATEGORY:
            self.stdout.write(f"- {category_name}")
        
        self.stdout.write("\nServices that would be created for each category:")
        for category_name, _ in Category.CATEGORY:
            self.stdout.write(f"\nCategory: {category_name}")
            for service_name in ["Basic Service", "Premium Service", "Express Service", 
                               "Professional Service", "Standard Service"]:
                self.stdout.write(f"- {category_name} {service_name}")