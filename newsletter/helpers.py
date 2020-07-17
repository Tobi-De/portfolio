from .models import Submission


def add_newsletter_subscriber(email, newsletter):
    submission, created = Submission.objects.get_or_create(email=email)
    if created:
        submission.newsletter.add(newsletter)
        if submission.is_email_valid():
            newsletter.send_confirmation_email(submission)
            return True
    return False
