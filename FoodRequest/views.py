from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Request
from .serializers import RequestSerializer
from django.core.exceptions import ObjectDoesNotExist
from .wrappers import check_valid_address, post_create_address, post_update_address, \
    get_address_id_wise_address_details, get_address_string
from .constants import RequestStatus
from django.contrib.auth import get_user_model
from collections import defaultdict
from django.db.models import Q
from .tasks import send_multi_format_email
from authentication.constants import UserType
from datetime import datetime


class RequestCreateList(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @staticmethod
    def get_users_in_given_city(city):
        User = get_user_model()
        emails = User.objects.filter(city=city, user_type=UserType.NGO.value)\
            .values_list("email", flat=True)
        return emails

    def post(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        address_details = request.data['address']
        is_valid, errors = check_valid_address(address_details)
        if not is_valid:
            return Response({"message": "Invalid address", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        request.data['address'] = post_create_address(address_details)["address_id"]
        response = super().post(request, args, kwargs)

        request_city = address_details["city"]
        to_emails = self.get_users_in_given_city(request_city)
        # sending email
        ctxt_for_email = request.data
        ctxt_for_email["address"] = get_address_string(request.data['address'])
        send_multi_format_email("request", "request_email", ctxt_for_email, target_emails=to_emails)

        response.data = {
            "id": response.data["id"]
        }
        return response


class RequestRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Request.objects.select_related('created_by', 'accepted_by').all()
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        request_id = kwargs["pk"]
        try:
            request_obj = Request.objects.get(id=request_id)
        except ObjectDoesNotExist:
            return Response({"message": "Invalid Request Id"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = self.serializer_class(request_obj).data
        address_id = response_data["address"]
        response_data["address"] = get_address_id_wise_address_details([address_id])[address_id]
        response_data["created_by"] = {
            "name": request_obj.created_by.get_full_name()
        }
        if request_obj.accepted_by:
            response_data["accepted_by"] = {
                "name": request_obj.accepted_by.get_full_name()
            }
        else:
            response_data["accepted_by"] = {
                "name": ""
            }
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        request_id = kwargs["pk"]
        try:
            request_obj = Request.objects.get(id=request_id)
        except ObjectDoesNotExist:
            return Response({"message": "Invalid Request Id"}, status=status.HTTP_400_BAD_REQUEST)

        # validating address id
        address_data = request.data.get("address", {})
        if "id" in address_data:
            if request.data["address"]["id"] != request_obj.address_id:
                return Response({"message": "Invalid Address Id"}, status=status.HTTP_400_BAD_REQUEST)
            address_data.pop("id")

        is_valid, errors = check_valid_address(address_data)
        if not is_valid:
            return Response({"message": "Invalid address", "errors": errors})

        request.data['address'] = post_update_address(
            request_obj.address_id, address_data)["address_id"]

        response = super().put(request, args, kwargs)
        response.data = {
            "id": response.data["id"]
        }
        return response


class GetActiveRequests(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Request.objects.filter(request_status=RequestStatus.open.value).all()
    serializer_class = RequestSerializer

    @staticmethod
    def get_user_id_wise_user_details(user_ids):
        User = get_user_model()
        users = User.objects.filter(id__in=user_ids)

        default_value = {
            "name": "",
            "email": "",
            "phone_number": ""
        }

        user_id_wise_user_details = {None: default_value}
        for user in users:
            user_id_wise_user_details[user.id] = {
                "name": user.get_full_name(),
                "email": user.email,
                "phone_number": user.phone_number
            }

        for user_id in user_ids:
            if user_id not in user_id_wise_user_details:
                user_id_wise_user_details[user_id] = default_value

        return user_id_wise_user_details

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(~Q(created_by=request.user.id) &
                                             Q(pickup_date_time__gte=datetime.now()))
        response = super().get(request, args, kwargs)

        address_ids = []
        user_ids = []
        for request_data in response.data["results"]:
            address_ids.append(request_data["address"])
            if request_data["created_by"]:
                user_ids.append(request_data["created_by"])
            if request_data["accepted_by"]:
                user_ids.append(request_data["accepted_by"])
        address_id_wise_address_data = get_address_id_wise_address_details(address_ids)
        user_id_wise_user_details = self.get_user_id_wise_user_details(user_ids)

        for request_data in response.data["results"]:
            request_data["created_by"] = user_id_wise_user_details[request_data["created_by"]]
            request_data["accepted_by"] = user_id_wise_user_details[request_data["accepted_by"]]
            request_data["address"] = address_id_wise_address_data[request_data["address"]]
        return response


class GetMyRequests(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @staticmethod
    def get_user_id_wise_user_details(user_ids):
        User = get_user_model()
        users = User.objects.filter(id__in=user_ids)

        default_value = {
            "name": "",
            "email": "",
            "phone_number": ""
        }

        user_id_wise_user_details = {None: default_value}
        for user in users:
            user_id_wise_user_details[user.id] = {
                "name": user.get_full_name(),
                "email": user.email,
                "phone_number": user.phone_number
            }

        for user_id in user_ids:
            if user_id not in user_id_wise_user_details:
                user_id_wise_user_details[user_id] = default_value

        return user_id_wise_user_details

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(created_by=request.user.id))
        response = super().get(request, args, kwargs)

        address_ids = []
        user_ids = []
        for request_data in response.data["results"]:
            address_ids.append(request_data["address"])
            if request_data["created_by"]:
                user_ids.append(request_data["created_by"])
            if request_data["accepted_by"]:
                user_ids.append(request_data["accepted_by"])
        address_id_wise_address_data = get_address_id_wise_address_details(address_ids)
        user_id_wise_user_details = self.get_user_id_wise_user_details(user_ids)

        for request_data in response.data["results"]:
            request_data["created_by"] = user_id_wise_user_details[request_data["created_by"]]
            request_data["accepted_by"] = user_id_wise_user_details[request_data["accepted_by"]]
            request_data["address"] = address_id_wise_address_data[request_data["address"]]
        return response


class GetMyAcceptedRequests(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @staticmethod
    def get_user_id_wise_user_details(user_ids):
        User = get_user_model()
        users = User.objects.filter(id__in=user_ids)

        default_value = {
            "name": "",
            "email": "",
            "phone_number": ""
        }

        user_id_wise_user_details = {None: default_value}
        for user in users:
            user_id_wise_user_details[user.id] = {
                "name": user.get_full_name(),
                "email": user.email,
                "phone_number": user.phone_number
            }

        for user_id in user_ids:
            if user_id not in user_id_wise_user_details:
                user_id_wise_user_details[user_id] = default_value

        return user_id_wise_user_details

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(accepted_by=request.user.id))
        response = super().get(request, args, kwargs)

        address_ids = []
        user_ids = []
        for request_data in response.data["results"]:
            address_ids.append(request_data["address"])
            if request_data["created_by"]:
                user_ids.append(request_data["created_by"])
            if request_data["accepted_by"]:
                user_ids.append(request_data["accepted_by"])
        address_id_wise_address_data = get_address_id_wise_address_details(address_ids)
        user_id_wise_user_details = self.get_user_id_wise_user_details(user_ids)

        for request_data in response.data["results"]:
            request_data["created_by"] = user_id_wise_user_details[request_data["created_by"]]
            request_data["accepted_by"] = user_id_wise_user_details[request_data["accepted_by"]]
            request_data["address"] = address_id_wise_address_data[request_data["address"]]
        return response


class AcceptRequests(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request_id = kwargs["id"]
        try:
            request_obj = Request.objects.get(id=request_id)
        except ObjectDoesNotExist:
            return Response({"message": "Invalid Request Id"}, status=status.HTTP_400_BAD_REQUEST)

        if request_obj.request_status != RequestStatus.open.value:
            return Response({"message": "Request Already Fullfilled"}, status=status.HTTP_400_BAD_REQUEST)

        if request_obj.created_by == request.user.id:
            return Response({"message": "You created the request, you can't accept it"},
                            status=status.HTTP_400_BAD_REQUEST)

        request_obj.request_status = RequestStatus.completed.value
        request_obj.accepted_by = request.user
        request_obj.save()
        # sending email
        ctxt_for_email = RequestSerializer(request_obj).data
        ctxt_for_email["address"] = get_address_string(ctxt_for_email["address"])
        ctxt_for_email["No. of People served"] = get_address_string(ctxt_for_email["quantity"])
        ctxt_for_email["accepted_by"] = {
            "name": request.user.get_full_name(),
            "email": request.user.email,
            "phone_number": request.user.phone_number
        }
        send_multi_format_email("request_accepted", "request_accepted_email",
                                ctxt_for_email, target_emails=[request_obj.created_by.email])

        return Response({"message": "Request Approved!!"}, status=status.HTTP_200_OK)


class CancelRequests(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request_id = kwargs["id"]
        try:
            request_obj = Request.objects.get(id=request_id)
        except ObjectDoesNotExist:
            return Response({"message": "Invalid Request Id"}, status=status.HTTP_400_BAD_REQUEST)

        if request_obj.request_status != RequestStatus.open.value:
            return Response({"message": "Request not in open state"}, status=status.HTTP_400_BAD_REQUEST)

        request_obj.request_status = RequestStatus.cancelled.value
        request_obj.save()
        return Response({"message": "Request Cancelled!!"}, status=status.HTTP_200_OK)
