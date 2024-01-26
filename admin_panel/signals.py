# from django.db.models.signals import post_save, post_delete, pre_save
# from django.dispatch import receiver
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Room
# from .graph_utils import rebuild_graph  # Updated import here
#
#
# @receiver(pre_save, sender=Room)
# def pre_update_graph_on_room_save(sender, instance, **kwargs):
#     try:
#         # Check if the room already exists
#         original = Room.objects.get(pk=instance.pk)
#     except ObjectDoesNotExist:
#         # If not, this is a new room, and we'll handle it in post_save
#         return
#
#     # If the room exists and certain fields that affect the graph have changed, then flag for update
#     fields_that_affect_graph = ['x', 'y', 'is_elevator']
#     if any(getattr(original, field) != getattr(instance, field) for field in fields_that_affect_graph):
#         instance._update_graph = True
#
#
# @receiver(post_save, sender=Room)
# def post_update_graph_on_room_save(sender, instance, created, **kwargs):
#     # This flag is to prevent recursion since saving within rebuild_graph will trigger post_save again
#     if 'skip_signal' in kwargs:
#         return
#     if created or getattr(instance, '_update_graph', False):
#         rebuild_graph()  # Call the function to rebuild the graph
#
#
# @receiver(post_delete, sender=Room)
# def update_graph_on_room_delete(sender, instance, **kwargs):
#     # This flag is to prevent recursion since saving within rebuild_graph will trigger post_save again
#     if 'skip_signal' in kwargs:
#         return
#     rebuild_graph()  # Call the function to rebuild the graph
