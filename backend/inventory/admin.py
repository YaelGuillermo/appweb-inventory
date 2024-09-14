from django.contrib import admin
from .models import (
    WarehouseModel, LocationModel, CategoryModel,
    ProductModel, InventoryModel, InventoryTransactionModel
)

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(WarehouseModel, WarehouseAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'warehouse', 'description', 'created_at')
    search_fields = ('name', 'warehouse__name')
    list_filter = ('warehouse', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(LocationModel, LocationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(CategoryModel, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'description', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(ProductModel, ProductAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'location', 'quantity', 'created_at')
    search_fields = ('product__name', 'location__name')
    list_filter = ('location', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(InventoryModel, InventoryAdmin)

class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'location', 'quantity', 'movement', 'created_at')
    search_fields = ('product__name', 'location__name')
    list_filter = ('movement', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(InventoryTransactionModel, InventoryTransactionAdmin)