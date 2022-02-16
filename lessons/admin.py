from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Lesson, Attendance, History


class LessonAdmin(admin.ModelAdmin):
    model = Lesson

    # Admin 화면에서 User 리스트에 출력되는 컬럼
    list_display = (
        'id', 'teacher_id', 'get_teacher_name', 'lesson_date', 'lesson_time', 'lesson_type', )

    # 화면 우측에 필터링 옵션에 출력되는 항목
    list_filter = ('lesson_type', 'teacher_id',)

    fieldsets = (
        ('담당강사', {'fields': ('teacher_id',)}),
        ('스케쥴', {'fields': ('lesson_date', 'lesson_time', 'lesson_type')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('teacher_id', 'lesson_date', 'lesson_time', 'lesson_type')}
         ),
    )

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

    def get_teacher_name(self, obj):
        return obj.teacher_id.name

    get_teacher_name.admin_order_field = "teacher_id"  # 정렬 가능 설정
    get_teacher_name.short_description = "담당강사"  # 컬럼 헤더명 변경

    search_fields = ('teacher_id',)
    ordering = ('teacher_id',)


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance

    # Admin 화면에서 User 리스트에 출력되는 컬럼
    list_display = (
        'id', 'lesson_id', 'member_id', 'get_member_name', 'status', 'input_dtime',)

    # 화면 우측에 필터링 옵션에 출력되는 항목
    list_filter = ('status',)

    fieldsets = (
        ('등록정보', {'fields': ('lesson_id', 'member_id', 'status')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('lesson_id', 'member_id', 'status',)}
         ),
    )

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

    def get_member_name(self, obj):
        return obj.member_id.name

    get_member_name.admin_order_field = "member_id"  # 정렬 가능 설정
    get_member_name.short_description = "수강생"  # 컬럼 헤더명 변경


class HistoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'created_by', 'lesson_date', 'lesson_time')
    pass


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(History, HistoryAdmin)