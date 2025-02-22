from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from rest_framework import viewsets
from .tasks import booking_confirmation_email, send_booking_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    @swagger_auto_schema(
        responses={
        200: openapi.Response(
            description="Listing retrieved successfully."
        ),
        201: openapi.Response(
            description="Listing created successfully."
        ),
        204: openapi.Response(
            description="No content. The listing has been successfully deleted."
        ),
        400: openapi.Response(
            description="Bad Request. The request was invalid or missing required fields."
        ),
        401: openapi.Response(
            description="Unauthorized. Authentication credentials were missing or invalid."
        ),
        403: openapi.Response(
            description="Forbidden. You do not have permission to perform this action."
        ),
        404: openapi.Response(
            description="Not Found. The requested listing does not exist."
        ),
    },
    )

    def perform_create(self, serializer):
        """
        Save the listing instance.
        """
        serializer.save()



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Booking retrieved successfully",
            ),
            204: openapi.Response(
                description="No content. The requested resource has been successfully processed, but there is no content to return."
            ),
            400: openapi.Response(
                description="Bad Request. The request was invalid or missing required fields.",
            ),
            401: openapi.Response(
                description="Unauthorized. Authentication credentials were missing or invalid.",
            ),
        },
    )
    def perform_create(self, serializer):
        """
        Save the booking instance and trigger the email task.
        """
        instance = serializer.save()

        # Send email asynchronously
        send_booking_email.delay(instance.booking_id)

    def perform_update(self, serializer):
        """
        Update the booking instance and trigger the email task.
        """
        instance = serializer.save()
        if instance.status == 'confirmed':
            booking_confirmation_email.delay(instance.booking_id)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
            description="Review retrieved successfully."
        ),
        201: openapi.Response(
            description="Review created successfully."
        ),
        204: openapi.Response(
            description="No content. The review has been successfully deleted."
        ),
        400: openapi.Response(
            description="Bad Request. The request was invalid or missing required fields."
        ),
        401: openapi.Response(
            description="Unauthorized. Authentication credentials were missing or invalid."
        ),
        403: openapi.Response(
            description="Forbidden. You do not have permission to perform this action."
        ),
        404: openapi.Response(
            description="Not Found. The requested review does not exist."
        ),
        }
    )
    def perform_create(self, serializer):
        """
        Save the review instance.
        """
        serializer.save()
    