from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from rest_framework import viewsets
from .tasks import booking_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        """
        Save the booking instance and trigger the email task.
        """
        instance = serializer.save()

        if instance.status == 'confirmed':
            booking_confirmation_email.delay(instance.booking_id) # Send email asynchronously
    
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
