from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from showrunner.models import Conference, School, Team, Player

admin.site.site_header = "DragonsTV Hydra"

admin.site.register(Conference)


def fetch_stats_for_teams(modeladmin, request, queryset):
    for team in queryset:
        team.fetch_stats()
        team.save()


def fetch_roster_for_teams(modeladmin, request, queryset):
    for team in queryset:
        team.fetch_roster()


class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        "image_tag",
        "full_name",
        "conference",
        "website",
        "view_teams_link",
    ]
    list_display_links = [
        "full_name",
    ]
    list_filter = ["conference"]
    search_fields = ["school_name", "team_name"]

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" height="30" width="auto" />'.format(obj.logo.url)
        )

    def view_teams_link(self, obj):
        url = (
            reverse("admin:showrunner_team_changelist")
            + "?"
            + urlencode({"school__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">Teams</a>', url)

    view_teams_link.short_description = ""


admin.site.register(School, SchoolAdmin)


class TeamAdmin(admin.ModelAdmin):
    actions = [fetch_stats_for_teams, fetch_roster_for_teams]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    list_display = ["school", "sport", "view_players_link"]
    list_filter = ["school", "sport"]

    def view_players_link(self, obj):
        url = (
            reverse("admin:showrunner_player_changelist")
            + "?"
            + urlencode({"team__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">Players</a>', url)

    view_players_link.short_description = ""


admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="80" height="auto" />'.format(obj.image.url)
        )

    def headshot(self, obj):
        return format_html(
            '<img src="{url}" width="100" height="auto" />'.format(
                url=obj.image.url,
            )
        )

    image_tag.short_description = ""
    list_display = [
        "image_tag",
        "uniform",
        "full_name",
        "team",
        "position",
        "height",
        "hometown",
        "high_school",
    ]
    list_display_links = ["full_name"]
    list_filter = [
        "team",
    ]
    search_fields = ["first_name", "last_name"]
    ordering = ["uniform"]
    readonly_fields = ["headshot"]


admin.site.register(Player, PlayerAdmin)
