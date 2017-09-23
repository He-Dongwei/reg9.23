from django.contrib import admin

# Register your models here.
from .models import paper,journal,recommend,author,reviewer,web,review,theme
admin.site.register(paper)
admin.site.register(journal)
admin.site.register(recommend)
admin.site.register(author)
admin.site.register(reviewer)
admin.site.register(web)
admin.site.register(review)
admin.site.register(theme)

