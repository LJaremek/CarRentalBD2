from django.db import models
from django.forms import ModelChoiceField


class XORForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        self.xor_fields = kwargs.pop("xor_fields", [])
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        for field_name in self.xor_fields:
            setattr(
                cls, "_%s_%s" % (name, field_name), models.BooleanField(default=False)
            )
            models.signals.pre_save.connect(self.check_xor_constraint, sender=cls)

    def check_xor_constraint(self, instance, **kwargs):
        values = [
            bool(getattr(instance, "_%s_%s" % (self.name, field_name)))
            for field_name in self.xor_fields
        ]
        if sum(values) != 1:
            raise ValueError("XOR constraint not satisfied")

    def formfield(self, **kwargs):
        defaults = {"form_class": ModelChoiceField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
      