from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pet, Task, Category
from .forms import PetForm, TaskForm
from django.urls import reverse_lazy


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.filter(user=self.request.user)
        context['tasks'] = Task.objects.filter(pet__user=self.request.user)
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

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'pets/add_task.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        task = form.save(commit=False)
        new_category_name = form.cleaned_data.get('new_category')
        category = form.cleaned_data.get('category')

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

