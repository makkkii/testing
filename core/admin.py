from django.contrib import admin

from core.models import Timezone, Company

MAX_SHOW_ALL = 10000
PER_PAGE = 500


@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    list_display = ('utc', 'label', 'alias', 'offset', 'is_dst', 'enabled', 'description')
    search_fields = ['utc', 'label', 'alias', 'description']
    # date_hierarchy = 'created'
    list_filter = ('is_dst', 'enabled')
    list_max_show_all = MAX_SHOW_ALL
    list_per_page = PER_PAGE


admin.site.register(Company)