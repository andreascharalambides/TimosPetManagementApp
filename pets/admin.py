from django.contrib import admin
from .models import Pet, Category, Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1  # Number of extra blank forms to display
    fields = ['data', 'category', 'start_date', 'end_date', 'important']
    readonly_fields = ['frequently']

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'user')
    list_filter = ('breed',)
    search_fields = ('name', 'breed')
    inlines = [TaskInline]

    def age(self, obj):
        return obj.age()

    age.short_description = 'Age'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('data', 'pet', 'category', 'start_date', 'end_date', 'important')
    list_filter = ('category', 'important', 'start_date', 'end_date')
    search_fields = ('data', 'comments')
    date_hierarchy = 'start_date'
