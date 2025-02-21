from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Booking


@shared_task
def send_booking_email(booking_id):
    """
    Task to send an e-mail notification.
    """
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        subject = f'Hello from Alx Travels: Your booking id- {booking.booking_id}'
        message = 'Your Booking has been placed successfully!'
        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [
                              booking.email], fail_silently=False)

        return mail_sent
    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found."


@shared_task
def booking_confirmation_email(booking_id):
    """
    Task to send an e-mail notification when a booking is
    successfully created.
    """
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        subject = f'Booking Confirmation - {booking.booking_id}'
        message = (
            f'Dear Customer,\n\n'
            f'Your booking has been successfully Confirmed!\n'
            f'Booking ID: {booking.booking_id}\n'
            f'Listing: {booking.listing.start_location} to {booking.listing.destination}\n'
            f'Start Date: {booking.start_date}\n'
            f'End Date: {booking.end_date}\n\n'
            f'Thank you for choosing us!\n'
        )

        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [
                              booking.email], fail_silently=False)
        print(f'finished sending email: {mail_sent} messages')
        return mail_sent

    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found."
