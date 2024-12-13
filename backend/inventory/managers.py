from rest_framework import serializers
from core.validations import (
    remove_spaces, validate_length, validate_no_start_num_or_special,
    validate_min_value, validate_max_value, validate_stock,
    validate_choice
)
from .models import (
    WarehouseModel, LocationModel, CategoryModel, 
    ProductModel, InventoryModel, InventoryTransactionModel
)
from .choices import MovementChoices, TypeChoices

class WarehouseManager(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = WarehouseModel

    def validate_name(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 64)
        value = validate_no_start_num_or_special(value)
        return value

    def validate_description(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 128)
        value = validate_no_start_num_or_special(value)
        return value

class LocationManager(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = LocationModel

    def validate_name(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 64)
        value = validate_no_start_num_or_special(value)
        return value

    def validate_description(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 128)
        value = validate_no_start_num_or_special(value)
        return value
    
class CategoryManager(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = CategoryModel

    def validate_code(self, value):
        value = validate_min_value(value, 21000)
        value = validate_max_value(value, 32000)
        return value

    def validate_name(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 64)
        value = validate_no_start_num_or_special(value)
        return value

    def validate_description(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 128)
        value = validate_no_start_num_or_special(value)
        return value
    
class ProductManager(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = ProductModel

    def validate_name(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 64)
        value = validate_no_start_num_or_special(value)
        return value
    
    def validate_description(self, value):
        value = remove_spaces(value)
        value = validate_length(value, 128)
        value = validate_no_start_num_or_special(value)
        return value
    
class InventoryManager(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = InventoryModel

    def validate_quantity(self, value):
        value = validate_min_value(value, 0)
        return value

class InventoryTransactionManager(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = InventoryTransactionModel

    def validate_quantity(self, value):
        is_out_transaction = self.initial_data['movement'] == MovementChoices.OUT
        inventory_quantity = InventoryModel.objects.get(pk=self.initial_data['inventory']).quantity
        value = validate_min_value(value, 1)
        if is_out_transaction:
            value = validate_stock(value, inventory_quantity)
        return value

    def validate_type(self, value):
        is_out_transaction = self.initial_data['movement'] == MovementChoices.OUT
        if is_out_transaction:
            allowed_types = [
                (TypeChoices.SALE, 'Venta'),
                (TypeChoices.LOST, 'Perdido'),
                (TypeChoices.DAMAGED, 'Dañado'),
                (TypeChoices.LOAN, 'Préstamo')
            ]
        else:
            allowed_types = [
                (TypeChoices.PURCHASE, 'Compra'),
                (TypeChoices.RETURN, 'Devolución')
            ]
        value = validate_choice(value, allowed_types)
        return value