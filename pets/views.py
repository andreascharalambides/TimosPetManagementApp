from datetime import datetime
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pet, Task, Category
from .forms import PetForm, TaskForm
from django.urls import reverse_lazy


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the selected day from query parameters, default to today
        day_param = self.request.GET.get("day")
        if day_param:
            try:
                selected_day = datetime.strptime(day_param, "%Y-%m-%d").date()
            except ValueError:
                selected_day = now().date()
        else:
            selected_day = now().date()

        # Fetch pets and tasks for the user
        context['pets'] = Pet.objects.filter(user=self.request.user)
        context['tasks'] = Task.get_tasks_for_day(user=self.request.user, day=selected_day)
        context['selected_day'] = selected_day  # Pass the selected day to the template

        return context


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/add_pet.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# pets/views.py

class TaskFormView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'pets/task_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        task = form.save(commit=False)
        new_category_name = form.cleaned_data.get('new_category')
        category = form.cleaned_data.get('category')

        # TODO Handle "--new-type--" case --> only then consider new category
        if new_category_name:
            # Create or get the new category
            new_category, created = Category.objects.get_or_create(
                user=self.request.user, name=new_category_name
            )
            if not category:
                # Assign the new category to the task
                task.category = new_category
            else:
                # Both provided; assign selected category and save new category
                pass  # task.category is already assigned from the form
        else:
            # No new category; ensure category is assigned
            task.category = category

        task.save()
        form.save_m2m()
        return super().form_valid(form)

class TaskCreateView(TaskFormView, CreateView):
    """View for creating a task."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False  # Flag for distinguishing between add and update
        return context

class TaskUpdateView(TaskFormView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True  # Flag for distinguishing between add and update
        return context

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('home')  # Redirect to the home page

    def get(self, *args, **kwargs):
        # Skip confirmation and delete immediately
        self.object = self.get_object()
        if self.object.pet.user == self.request.user:
            self.object.delete()
        return redirect(self.success_url)

from django.http import JsonResponse
from datetime import datetime
from .models import Task

def fetch_tasks_for_day(request):
    """
    API endpoint to fetch tasks for a specific day.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    day_param = request.GET.get("day")
    if not day_param:
        return JsonResponse({"error": "Day parameter is required"}, status=400)

    try:
        selected_day = datetime.strptime(day_param, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    tasks = Task.get_tasks_for_day(user=request.user, day=selected_day)

    # Serialize task data
    task_data = [
        {
            "id": task.id,
            "category": task.category.name if task.category else "No Category",
            "pet": task.pet.name,
            "start_time": task.start_date.strftime("%H:%M"),
            "frequently": task.frequently,
            "important": task.important,
        }
        for task in tasks
    ]

    return JsonResponse({"tasks": task_data}, status=200)