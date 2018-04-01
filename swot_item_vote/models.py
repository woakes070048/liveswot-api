from django.db import models

from authenticationjwt.models import User

from swot_item.models import SwotItem


class Vote(models.Model):
    VOTE_TYPES = (('up', 'UP'), ('down', 'DOWN'))

    created = models.DateTimeField(auto_now_add=True)
    voteType = models.CharField(choices=VOTE_TYPES,
                                max_length=4,
                                blank=False,
                                null=False)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   blank=False,
                                   null=True,
                                   related_name='+',
                                   related_query_name='+')
    item = models.ForeignKey(SwotItem,
                             on_delete=models.SET_NULL,
                             blank=False,
                             null=True,
                             related_name='+',
                             related_query_name='+')
