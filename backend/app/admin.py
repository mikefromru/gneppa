from django.contrib import admin
from . models import (
    Level,
    Question,
    UserLevel,
    AppFile,
    VocabLevel,
    ClickCounter
)

@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    pass

@admin.register(VocabLevel)
class VocabLevelAdmin(admin.ModelAdmin):
    pass

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):

    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    search_fields = ('id', 'name')

@admin.register(AppFile)
class AppFileAdmin(admin.ModelAdmin):
        pass

@admin.register(ClickCounter)
class ClickCounterAdmin(admin.ModelAdmin):
    pass
