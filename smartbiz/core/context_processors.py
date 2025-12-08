from .utils import get_notifications


def notifications_processor(request):
    """Add notifications to template context"""
    return {
        "notifications": get_notifications(request)
    }
