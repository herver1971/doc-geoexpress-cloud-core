#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from geonode.base.models import ResourceBase
from geonode.documents.models import Document
from geonode.layers.models import Dataset
from geonode.maps.models import Map
from geonode.utils import get_geonode_app_types


class FavoriteManager(models.Manager):
    def favorites_for_user(self, user):
        return self.filter(user=user)

    def _favorite_ct_for_user(self, user, model):
        content_type = ContentType.objects.get_for_model(model)
        result = self.favorites_for_user(user).filter(content_type=content_type).prefetch_related("content_object")
        return result

    def favorite_documents_for_user(self, user):
        return self._favorite_ct_for_user(user, Document)

    def favorite_maps_for_user(self, user):
        return self._favorite_ct_for_user(user, Map)

    def favorite_datasets_for_user(self, user):
        return self._favorite_ct_for_user(user, Dataset)

    def favorite_users_for_user(self, user):
        return self._favorite_ct_for_user(user, get_user_model())

    def favorite_for_user_and_content_object(self, user, content_object):
        """
        Returns the Favorite object if it exists for the given user, type, and the primary key
        of the input content_object. If no Favorite exists, returns None.

        .. note::
            Due to the class's `unique_together` constraint, there can be only 0 or 1 Favorite
            object for the given combination of user, type, and content_object.

        """

        content_type = ContentType.objects.get_for_model(type(content_object))
        result = self.filter(user=user, content_type=content_type, object_id=content_object.pk)

        if result and len(result) > 0:
            return result[0]
        else:
            return None

    def bulk_favorite_objects(self, user):
        """
        Get the actual favorite objects for a user as a dict by content_type
        """

        favs = {}
        for m in (Document, Map, Dataset, get_user_model()):
            ct = ContentType.objects.get_for_model(m)
            f = self.favorites_for_user(user).filter(content_type=ct)
            favs[ct.name] = m.objects.filter(id__in=f.values("object_id"))
        return favs

    def create_favorite(self, content_object, user):
        if isinstance(content_object, ResourceBase):
            geoapp_types = get_geonode_app_types()
            if content_object.resource_type in geoapp_types:
                content_type = ContentType.objects.get(model="geoapp")
            else:
                content_type = ContentType.objects.filter(model=content_object.resource_type).last()
        else:
            content_type = ContentType.objects.get_for_model(type(content_object))

        favorite, _ = self.get_or_create(
            user=user,
            content_type=content_type,
            object_id=content_object.pk,
        )
        return favorite


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_on = models.DateTimeField(auto_now_add=True)

    objects = FavoriteManager()

    class Meta:
        verbose_name = "favorite"
        verbose_name_plural = "favorites"
        unique_together = (("user", "content_type", "object_id"),)

    def __str__(self):
        if self.content_object:
            return f"Favorite: {self.content_object.title}, {self.content_type}, {self.user}"
        else:
            return "Unknown"
