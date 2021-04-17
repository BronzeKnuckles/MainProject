from django.urls import path
from . import views

urlpatterns = [
    path('api', views.api, name="api"),
    path('mine', views.mine, name="mine"),
    path('lbh', views.last_block_hash, name="last-block-hash"),
    path('new_tx', views.new_transaction, name="new-transaction"),

    path('full_chain', views.full_chain, name="full-chain"),
    path('block/<int:block_num>',views.block, name="block-num"),
    path('register_nodes', views.register_nodes, name="register-nodes"),
    path('consensus', views.consensus, name="consensus"),
]