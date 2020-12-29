from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from core.models import Assignment, Classroom, Membership, Submission
from django.shortcuts import redirect
from django.urls import reverse_lazy


class MainView(LoginRequiredMixin, generic.ListView):
    template_name = "main.html"

    def get_queryset(self):
        return self.request.user.membership_set.all()


class ClassroomView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Classroom
    template_name = "classroom.html"

    def is_teacher(self):
        pk = self.kwargs["pk"]
        classroom = Classroom.objects.get(pk=pk)
        for membership in list(classroom.membership_set.all()):
            if self.request.user == membership.user and membership.is_teacher:
                return True
        return False

    def get_context_data(self, **kwargs):
        context_data = super(ClassroomView, self).get_context_data(**kwargs)
        context_data["is_teacher"] = self.is_teacher()
        return context_data

    def test_func(self):
        pk = self.kwargs["pk"]
        return self.request.user.membership_set.filter(classroom__pk=pk).count() == 1

    def handle_no_permission(self):
        return redirect("core:main")


class AssignmentView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Assignment
    template_name = "assignment.html"

    def test_func(self):
        """Only allow members of the classroom to see an assignment."""
        pk = self.kwargs["pk"]
        assignment = Assignment.objects.get(pk=pk)
        members = [m.user for m in assignment.classroom.membership_set.all()]
        return self.request.user in members

    def handle_no_permission(self):
        return redirect("core:main")


class AssignmentAdminView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Assignment
    template_name = "assignment_admin.html"

    def test_func(self):
        """Only allow teachers of the classroom to see an assignment."""
        pk = self.kwargs["pk"]
        assignment = Assignment.objects.get(pk=pk)
        teachers = [
            m.user for m in assignment.classroom.membership_set.all() if m.is_teacher
        ]
        return self.request.user in teachers

    def handle_no_permission(self):
        return redirect("core:main")


class SubmissionView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Submission
    template_name = "submission.html"

    def is_teacher(self):
        pk = self.kwargs["pk"]
        submission = Submission.objects.get(pk=pk)
        for membership in list(submission.assignment.classroom.membership_set.all()):
            if self.request.user == membership.user and membership.is_teacher:
                return True
        return False

    def get_context_data(self, **kwargs):
        context_data = super(SubmissionView, self).get_context_data(**kwargs)
        context_data["is_teacher"] = self.is_teacher()
        return context_data

    def test_func(self):
        """Only allow the owner of the submission or teachers of the class to view."""
        pk = self.kwargs["pk"]
        submission = Submission.objects.get(pk=pk)
        return self.request.user == submission.user or self.is_teacher()

    def handle_no_permission(self):
        pk = self.kwargs["pk"]
        assignment = Submission.objects.get(pk=pk).assignment
        return redirect("core:assignment", pk=assignment.pk)


class CreateClassroomView(LoginRequiredMixin, generic.CreateView):
    model = Classroom
    fields = ["name"]
    template_name = "create_classroom.html"

    def get_success_url(self):
        return reverse_lazy("core:classroom", args=[str(self.object.pk)])

    def form_valid(self, form):
        response = super(CreateClassroomView, self).form_valid(form)
        membership = Membership(
            user=self.request.user,
            classroom=self.object,
            status=Membership.ACCEPTED,
            is_teacher=True,
        )
        membership.save()
        return response


class CreateAssignmentView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Assignment
    fields = ["text"]
    template_name = "create_assignment.html"

    def get_success_url(self):
        return reverse_lazy("core:assignment", args=[str(self.object.pk)])

    def form_valid(self, form):
        response = super(CreateAssignmentView, self).form_valid(form)
        assignment = self.object
        assignment.user = self.request.user
        assignment.classroom = Classroom.objects.get(pk=self.kwargs["classroom_pk"])
        assignment.save()
        return response

    def test_func(self):
        """Only allow teachers of the class to create assignments."""
        pk = self.kwargs["classroom_pk"]
        classroom = Classroom.objects.get(pk=pk)
        for membership in list(classroom.membership_set.all()):
            if self.request.user == membership.user and membership.is_teacher:
                return True
        return False

    def handle_no_permission(self):
        return redirect("core:main")
