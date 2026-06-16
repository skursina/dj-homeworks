from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return
        
        main_scopes_count = 0
        scopes_count = 0

        for form in self.forms:
            cleaned_data = getattr(form, 'cleaned_data', None)
            
            if not cleaned_data:
                continue
            
            if cleaned_data.get('DELETE'):
                continue

            tag = cleaned_data.get('tag')

            if not tag:
                continue

            scopes_count += 1

            if cleaned_data.get('is_main'):
                main_scopes_count += 1
        
        if scopes_count == 0:
            raise ValidationError(
                'У статьи должен быть хотя бы один тэг')

        if main_scopes_count != 1:
            raise ValidationError(
                'У статьи должен быть только один основной тэг')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet
    extra = 1
    fields = ['tag', 'is_main']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']
    list_filter = ['published_at', 'scopes__tag']
    search_fields = ['title', 'text']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']