from django.contrib import admin
from import_export import resources

# Register your models here.
from .models import Post, Comment, Airport

class CommentInline(admin.TabularInline):
    model = Comment
    
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


class AirportResource(resources.ModelResource):

    class Meta:
        model = Airport
        
        
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Airport)

