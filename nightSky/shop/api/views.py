from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import status
from knox.auth import TokenAuthentication
from shop.models import Order, Payment
from shop.api.serializers import OrderSerializer
from rest_framework.response import Response
import requests
import json

from nightSky.settings import (
    MERCHANT_ID,
    CALLBACK_URL,
    ZP_API_REQUEST,
    ZP_API_STARTPAY,
    ZP_API_VERIFY,
)


class OrderAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        # return Order.objects.all()


class RequestPaymentAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_order(self, pk):
        try:
            return Order.objects.get(
                user=self.request.user,
                pk=pk,
                status=Order.StatusChoice.PAYMENT,
            )
        except Order.DoesNotExist:
            raise ValidationError({"order": "order does not exist"})

    def get_payment_url(self, order):
        payment = order.payment
        phone = self.request.user.phone_number
        email = self.request.user.email

        req_data = {
            "merchant_id": MERCHANT_ID,
            "amount": payment.price,
            "callback_url": CALLBACK_URL,
            "description": "توضیحات",
            "metadata": {"mobile": phone, "email": email},
        }

        req_header = {"accept": "application/json", "content-type": "application/json'"}

        req = requests.post(
            url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header
        )

        if len(req.json()["errors"]) == 0:

            authority = req.json()["data"]["authority"]

            payment.authority = authority
            payment.save()

            return Response(
                data={"url": ZP_API_STARTPAY.format(authority=authority)},
                status=status.HTTP_200_OK,
            )
        else:
            e_code = req.json()["errors"]["code"]
            e_message = req.json()["errors"]["message"]
            return Response(
                data={"detail": f"Error code: {e_code}, Error Message: {e_message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, pk):
        order = self.get_order(pk)
        return self.get_payment_url(order)


class VerifyPaymentAPIView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get_payment(self, authority):
        return Payment.objects.get(authority=authority, is_verified=False)

    def get(self, request):
        t_status = request.GET.get("Status")
        t_authority = request.GET["Authority"]

        if request.GET.get("Status") == "OK":
            payment = self.get_payment(t_authority)

            req_header = {
                "accept": "application/json",
                "content-type": "application/json'",
            }
            req_data = {
                "merchant_id": MERCHANT_ID,
                "amount": payment.price,
                "authority": t_authority,
            }
            req = requests.post(
                url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header
            )
            if len(req.json()["errors"]) == 0:
                t_status = req.json()["data"]["code"]
                if t_status == 100:
                    payment.ref_id = str(req.json()["data"]["ref_id"])
                    payment.is_verified = True
                    payment.save()
                    order = payment.order
                    order.status = Order.StatusChoice.POSTING
                    order.save()
                    return Response(
                        data=self.get_serializer(payment.order).data,
                        status=status.HTTP_200_OK,
                    )
                    # TODO: redirect to panel
                    return redirect()
                elif t_status == 101:
                    return Response(
                        "Transaction submitted : " + str(req.json()["data"]["message"])
                    )
                else:
                    return Response(
                        "Transaction failed.\nStatus: "
                        + str(req.json()["data"]["message"])
                    )
            else:
                e_code = req.json()["errors"]["code"]
                e_message = req.json()["errors"]["message"]
                return Response(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return Response("Transaction failed or canceled by user")