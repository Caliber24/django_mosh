from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='products-reviews')



carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='carts-items')

# router = SimpleRouter()
# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

urlpatterns = router.urls + products_router.urls + carts_router.urls

# urlpatterns = [
#     path('',include(router.urls))
# ]


# urlpatterns = [
# path('products/',views.ProductList.as_view()),
# path('products/<int:id>', views.ProductDetail.as_view()),
# path('collections/', views.CollectionList.as_view(), name='collection-list'),
# path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail')
# ]
