from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
from django.conf import settings

def notify_slack(text, attach_url=None):
    if settings.TESTING or settings.SLACK_HOOK_URL is None:
        return
    if attach_url:
        attach_url = settings.BASE_URL + attach_url
        text = '%s %s' % (text, attach_url)
    post_fields = {'payload': json.dumps({'text': text, 'username': 'Many Ideas Bot', 'icon_emoji': ':robot_face:'})}
    request = Request(settings.SLACK_HOOK_URL, urlencode(post_fields).encode())
    urlopen(request, timeout=5).read().decode()