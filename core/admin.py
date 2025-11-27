from django.contrib import admin
from .models import PageView
from django.db.models import Count

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'url', 'method', 'user', 'ip_address')
    list_filter = ('method', 'timestamp')
    search_fields = ('url', 'ip_address')
    
    change_list_template = 'admin/core/pageview/change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_views': qs.count(),
            'unique_visitors': qs.values('ip_address').distinct().count(),
            'top_pages': qs.values('url').annotate(total=Count('url')).order_by('-total')[:5],
        }
        
        response.context_data['summary'] = metrics
        
        return response
