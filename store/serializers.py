from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem, Customer, OrderItem, Order
from .signals import order_created

# class CollectionsSerializer(serializers.Serializer):
#   id = serializers.IntegerField()
#   title = serializers.CharField(max_length=255)

# class ProductSerializer(serializers.Serializer):
#   id = serializers.IntegerField()
#   title = serializers.CharField(max_length=255)
#   price = serializers.DecimalField(max_digits=6,decimal_places=2, source='unit_price')
#   price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#   # ba estefade az nested object
#   # collection = CollectionsSerializer()

#   # in rahe aval serialize kardan relationshp hast
#   # collection = serializers.PrimaryKeyRelatedField(
#   #   queryset = Collection.objects.all()
#   # )
#   # collection = serializers.StringRelatedField()

#   # estefade az hyper link
#   collection = serializers.HyperlinkedRelatedField(
#     queryset=Collection.objects.all(),
#     view_name='collection-detail'
#   )

#   def calculate_tax(self, product: Product):
#     return product.unit_price * Decimal(1.1)


class CollectionSerializer(serializers.ModelSerializer):
    # products_count = serializers.SerializerMethodField(
    #     method_name='product_count')

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

    # def product_count(self, collection: Collection):
    #     product_count = Product.objects.filter(
    #         collection_id=collection.id).count()
    #     return product_count


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'price', 'price_with_tax',  'collection']

    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField('calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    # def create(self, validated_data):
    #   product = Product(**validated_data)
    #   product.other=1
    #   product.save()
    #   return product

    # def update(self, instance, validated_data):
    #   instance.unit_price = validated_data.get('price')
    #   instance.save()
    #   return instance

    # def validate(self, data):
    #   if data['password']!=data['confirm_password']:
    #     return serializers.ValidationError('Password do not match')
    #   return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)
    id = serializers.UUIDField(read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            #
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # Create a new Item
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with given ID was found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is Empty')
        return cart_id

    def save(self, **kwargs):
        # print(self.validated_data['cart_id'])
        # print(self.context['user_id'])
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects\
                .select_related('product')\
                .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__, order=order)
            return order
