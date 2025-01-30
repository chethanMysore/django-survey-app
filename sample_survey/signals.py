import asyncio
from django.core.signals import request_finished
from django.dispatch import receiver, Signal

# Incoming message signal dispatcher
incoming_feedback_dispatcher = Signal()


# @receiver(request_finished)
# async def my_callback(sender, **kwargs):
#     await asyncio.sleep(5)
#     print("Request finished!")


@receiver(incoming_feedback_dispatcher)
def incoming_feedback_receiver(sender, msg, **kwargs):
    feedback = msg
    print(f'Feedback received by the receiver - {feedback}')
