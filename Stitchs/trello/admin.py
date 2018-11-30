from django.contrib import admin

# Register your models here.
from .models import (StitchBoard,
                     StitchList,
                     StitchCard,
                     Members,
                     Label)

# Register your models here.
admin.site.register(StitchBoard)
admin.site.register(StitchList)
admin.site.register(StitchCard)
admin.site.register(Members)
admin.site.register(Label)
