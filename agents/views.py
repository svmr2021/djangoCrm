from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
import random

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/list.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()

        Agent.objects.create(user=user,organization=self.request.user.userprofile)
        send_mail(
            subject = "You are invited to be ab agent",
            message='You are added as an agent on SVMRCRM. Please come login to start working',
            from_email='admin@test.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
    template_name = 'agents/detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.all()


class AgentUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'agents/update.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        return Agent.objects.all()


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse('agents:agent-list')