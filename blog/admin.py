from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import Post, Category, Tag, Comment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)

