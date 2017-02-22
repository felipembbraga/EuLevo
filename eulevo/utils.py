from core.tasks import send_multiply_messages


def delete_deals(queryset=None, user_list=[], title='', body=''):
    send_multiply_messages.delay(
        user_list,
        message_body=body,
        message_title=title
    )

    for item in queryset:
        item.delete()