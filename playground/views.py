from django.shortcuts import render
from django.db.models import Q, F, Value, Func, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Avg, Sum, Max, Min, Count
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection
# Create your views here.

# @transaction.atomic()
def say_hello(request):
    # query_set = Product.objects.filter(sku__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # query_set =Product.objects.values('sku','title', 'collection__title')
    # query_set =Product.objects.values_list('sku','title', 'collection__title')
    # query_set = Product.objects.all()[5:10]
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')
    # query_set = Product.objects.filter(collection__id=1).order_by('unit_price')
    # query_set = Product.objects.order_by('unit_price', '-title').reverse()
    # query_set = Product.objects.filter(inventory=F('collection__id'))
    # query_set = Product.objects.filter(Q(inventor_lt=10) | Q(unit_price__lt=20))
    # query_set = Product.objects.filter(unit_price__range=(20,30))

    # None
    # product = Product.objects.filter(pk=0).first()

    # exists = Product.objects.filter(pk=0).exists()

    # try:
    #   product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #   pass
    # for product in query_set:
    #   print(product)

    # list(query_set)

    # product[0:5]

    # query_set = Product.objects.defer('description')
    # query_set = Product.objects.only('description')

    # select_related(1)
    # prefetch_related(n)
    # query_set = Product.objects.select_related('collection').all()
    # query_set = Product.objects.prefetch_related(
    #     'promotions').select_related('collection').all()

    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # result = Product.objects.aggregate(
    #     count=Count('sku'), min_price=Min('unit_price'))

    # queryset = Customer.objects.annotate(is_new=Value(True))
    # queryset = Customer.objects.annotate(new_id=F('id')+1)
    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Func(F('first_name'), Value(" "), F("last_name"), function='CONCAT')
    #     )
    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Concat('first_name', Value(" "),'last_name')
    #     )

    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # discounted_price = ExpressionWrapper(F('unit_price')*0.8,output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )


    # queryset = TaggedItem.objects.get_tags_for(Product, 1) 


    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type=content_type,
    #         object_id=1
    #     )


    # queryset = Product.objects.all()
    # list(queryset)
    # queryset[0]
    
    
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(sku=1)
    # collection.featured_product_id = 1
    # collection.save()
    # collection = Collection.objects.create(title='a', featured_product_id=1)
    
    
    # collection = Collection.objects.get(pk=101)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()
    
    # Collection.objects.filter(pk=101).update(featured_product=None,title='Video Games')
    # collection = Collection(pk=11)
    # collection.delete()
    # Collection.objects.filter(id__gt=5).delete()
    
    
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id=1
    #     order.save()
        
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 1000
    #     item.save()
    
    # queryset = Product.objects.raw('SELECT * FROM store_product')
    # queryset = Product.objects.raw('SELECT id,title FROM store_product')
    
    # cursor = connection.cursor() 
    # cursor.execute("SELECT")
    # cursor.close()
    
    # with connection.cursor() as cursor:
    #     cursor.callproc('get_customers',[1,2,3])
    
    return render(request, 'hello.html', {'name': "Amir"})
