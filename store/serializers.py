from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


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

    products_count = serializers.IntegerField()
    
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
