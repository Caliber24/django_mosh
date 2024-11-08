from django.contrib import admin, messages
# from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# from tags.models import TaggedItem
from django.db.models.aggregates import Count
# Register your models here.

# class TagInline(GenericTabularInline):
#     autocomplete_fields=['tag']
#     model = TaggedItem



class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html("<a href='{}'>{} Products</a>", url, collection.products_count)
        # return collection.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f"<img src='{instance.image.url}' class='thumbnail' />")
        return ''
    
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields =['title', 'slug']
    # readonly_fields=['title']
    # exclude=['promotions']
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug': ['title']
    }
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    # inlines = [TagInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    search_fields = ['title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    # queryset.select_related
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request,
                          f'{updated_count} products were successfully updated',
                          messages.ERROR
                          )

    def collection_title(self, product):
        return product.collection.title

    class Media:
        css = {
            'all': ['store/style.css']
        }

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'membership', 'orders']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    @admin.display(ordering='orders_count')
    def orders(self, customer):

        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               }))

        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)

        # return customer.orders_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'placed_at', 'payment_status']
    list_editable = ['payment_status']
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    def customer_name(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'
