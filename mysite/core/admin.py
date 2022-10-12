from django.contrib import admin

from solo.admin import SingletonModelAdmin

from mysite.core.models import (
    AboutPage,
    Belief,
    HomePage,
    Location,
    Mission,
    OnlinePlatforms,
    Vision,
    WeeklyActivity,
)


class WeeklyActivtyAdmin(admin.ModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


class BeliefAdmin(admin.ModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


class VisionAdmin(SingletonModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


class MissionAdmin(SingletonModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


class LocationAdmin(admin.ModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


class HomePageAdmin(SingletonModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


class AboutPageAdmin(SingletonModelAdmin):
    exclude = (
        "slug",
        "status_changed",
    )


admin.site.register(WeeklyActivity, WeeklyActivtyAdmin)
admin.site.register(Belief, BeliefAdmin)
admin.site.register(OnlinePlatforms, SingletonModelAdmin)
admin.site.register(Vision, VisionAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
