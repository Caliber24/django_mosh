from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order, ProductImage
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id','unit_price']
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['unit_price', 'last_update']
    lookup_field = 'id'

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=self.request.query_params['collection_id'])

    #     return  queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['id']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(APIView):
        # def get(self, request):
        #     queryset = Product.objects.select_related('collection').all()
        #     serializer = ProductSerializer(
        #         queryset, many=True, context={'request': request})
        #     return Response(serializer.data)

        # def post(self, request):
        #     serializer = ProductSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()

#     # def get_serializer_class(self):
#     #     return ProductSerializer()

#     def get_serializer_context(self):
#         return {'request': self.request}


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductDetail(APIView):

#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # if serializer.is_valid():
#         #   serializer.validated_data
#         #   return Response('ok')
#         # else:

#         #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with an Product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted because it is associated with an Product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response()

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()

#     serializer_class = CollectionSerializer

# @api_view(["GET", "POST"])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(
#             products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it is associated with an Product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response()

# @api_view(["GET", "PUT", "DELETE"])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(
#         products_count=Count('products')), pk=pk)
#     if request.method == "GET":
#         serializer = CollectionSerializer(instance=collection)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(
#             instance=collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it is associated with an Product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}


class CartViewSet(RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(
            user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={
                                           'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}