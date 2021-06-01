from django.contrib import admin

from .models import *

admin.site.register(Account)
admin.site.register(BusinessNature)
admin.site.register(TrueLayerAccount)
admin.site.register(TrueLayerCard)
admin.site.register(TrueLayerAccountTransaction)
admin.site.register(TrueLayerCardTransaction)
admin.site.register(TrueLayerMerchant)
admin.site.register(TrueLayerClassification)
