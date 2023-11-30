from django.contrib import admin

from feedback.models import Feedback, FileUpload, PersonalData, StatusLog


__all__ = []


class PersonalDataInline(admin.StackedInline):
    model = PersonalData
    can_delete = False


@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = [
        PersonalData.name.field.name,
        PersonalData.mail.field.name,
    ]
    list_display_links = [
        PersonalData.name.field.name,
        PersonalData.mail.field.name,
    ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        Feedback.text.field.name,
        Feedback.created_on.field.name,
        Feedback.status.field.name,
    ]
    list_display_links = [
        Feedback.text.field.name,
    ]
    readonly_fields = [Feedback.created_on.field.name]
    inlines = [PersonalDataInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if "status" in form.changed_data:
            StatusLog.objects.create(
                user=request.user,
                feedback=obj,
                from_status=form.initial["status"],
                to=obj.status,
            )


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = [
        StatusLog.user.field.name,
        StatusLog.timestamp.field.name,
        StatusLog.feedback.field.name,
        StatusLog.from_status.field.name,
        StatusLog.to.field.name,
    ]
    readonly_fields = [
        StatusLog.user.field.name,
        StatusLog.timestamp.field.name,
        StatusLog.feedback.field.name,
        StatusLog.from_status.field.name,
        StatusLog.to.field.name,
    ]


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = [
        FileUpload.file.field.name,
        FileUpload.feedback.field.name,
    ]

    list_display_links = [
        FileUpload.feedback.field.name,
    ]
