from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cost-centers', views.CostCenterViewSet)
router.register(r'sociedades', views.SociedadViewSet)
router.register(r'traders', views.TraderViewSet)
router.register(r'commodity-groups', views.CommodityGroupViewSet)
router.register(r'commodity-types', views.CommodityTypeViewSet)
router.register(r'commodities', views.CommodityViewSet)
router.register(r'counterparties', views.CounterpartyViewSet)
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'exchange-rates', views.ExchangeRateViewSet)
router.register(r'contracts', views.ContractViewSet, basename='contract')
router.register(r'contract-amendments', views.ContractAmendmentViewSet, basename='contractamendment')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.search_global, name='global_search'),
]