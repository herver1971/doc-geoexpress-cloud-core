from typing import List

from dal_select2_taggit.widgets import TaggitSelect2
from django.http.request import QueryDict


class TaggitSelect2Custom(TaggitSelect2):
    """
    Overriding Select2 tag widget for taggit's TagField.
    Fixes error in tests where 'value' is None.
    """

    def value_from_datadict(self, data, files, name):
        """
        Handle multi-word tag.

        Insure there's a comma when there's only a single multi-word tag,
        or tag "Multi word" would end up as "Multi" and "word".
        """

        try:
            value = super().value_from_datadict(data, files, name)
            if value and "," not in value:
                value = f"{value},"
            return value
        except TypeError:
            return ""


class TaggitProfileSelect2Custom(TaggitSelect2):
    """
    Overriding Select2 tag widget for ContactRoleField.
    """

    def value_from_datadict(self, data, files, name) -> List[str]:
        """
        Handle multi-profiles.

        Returns list of selected elements
        """

        if type(data) is dict and name in data:
            return data[name]
        elif type(data) is QueryDict:
            return data.getlist(name)
        return []
