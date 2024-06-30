

from django.urls import path

from pay_star import views

urlpatterns=[
    path('payment',view=views.PaymentView.as_view()),
    path('callback',view=views.CallbackView.as_view())
]