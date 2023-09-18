import json

from django.contrib import admin
from django.template.defaultfilters import capfirst
from django.utils import translation


class NewInlineAdminFormSet(admin.helpers.InlineAdminFormSet):
    def inline_formset_data(self) -> str:
        """Change JSON for the Add another {{ ObjectPhoto }} button"""

        verbose_name = self.opts.verbose_name
        return json.dumps(
            {
                "name": "#%s" % self.formset.prefix,
                "options": {
                    "prefix": self.formset.prefix,
                    # "addText": "Добавить %(verbose_name)s"
                    "addText": "Добавить"
                    % {
                        "verbose_name": capfirst(verbose_name),
                    },
                    "deleteText": translation.gettext("Remove"),
                },
            }
        )


def improve_inline_formset(inline_admin_formsets):
    new_inline_admin_formsets = []
    for current_inline_admin_formset in inline_admin_formsets:
        new_inline_admin_formset = NewInlineAdminFormSet(
            current_inline_admin_formset.opts,
            current_inline_admin_formset.formset,
            current_inline_admin_formset.fieldsets,
            current_inline_admin_formset.prepopulated_fields,
            current_inline_admin_formset.readonly_fields,
            current_inline_admin_formset.model_admin,
            current_inline_admin_formset.has_add_permission,
            current_inline_admin_formset.has_change_permission,
            current_inline_admin_formset.has_delete_permission,
            current_inline_admin_formset.has_view_permission,
        )
        new_inline_admin_formsets.append(new_inline_admin_formset)
    return new_inline_admin_formsets
