from django.shortcuts import render, redirect, reverse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreation, AssignAgentForm, CategoryUpdateForm
from django.views.generic import *
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents import mixins
from .models import Category


# Create your views here.

# CLASS BASED VIEWS


class LandingPage(TemplateView):
    template_name = 'landing.html'


class LeadList(LoginRequiredMixin, ListView):
    template_name = 'leads/list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadList, self).get_context_data(**kwargs)
        if self.request.user.is_organizer:
            queryset = Lead.objects.filter(organization=self.request.user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


class LeadDetail(LoginRequiredMixin, DetailView):
    template_name = 'leads/detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreate(mixins.OrganisorAndLoginRequiredMixin, CreateView):
    template_name = 'leads/create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:list-view')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject='A lead has been created',
            message="Go to the site to see the new lead",
            from_email='test@test.com',
            recipient_list=['test2@test.com'],
        )
        return super(LeadCreate, self).form_valid(form)


class LeadUpdate(mixins.OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:list-view')


class LeadDelete(mixins.OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/delete.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:list-view')


class LeadSignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreation

    def get_success_url(self):
        return reverse('login-page')


class AssignAgent(mixins.OrganisorAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgent, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {
                'request': self.request
            }
        )
        return kwargs

    def get_success_url(self):
        return reverse('leads:list-view')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgent, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
            )
        context.update(
            {
                'unassigned_lead_count': queryset.filter(category__isnull=True).count()
            }
        )
        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/category_update.html'
    context_object_name = 'lead'
    form_class = CategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset

    def get_success_url(self):
        return reverse('leads:detail-view', kwargs={'pk':self.get_object().id})


# FUNCTION BASED VIEWS
def landing_page(request):
    return render(request, 'landing.html')


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/list.html', context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/detail.html', context)


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form': form,
    }
    return render(request, 'leads/create.html', context)


'''def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = form.cleaned_data['agent']
            Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent,
            )
            return redirect('/leads')
    context = {
        'form': form,
    }
    return render(request, 'leads/create.html', context)
'''


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads/')

    context = {
        'form': form,
        'lead': lead,
    }

    return render(request, 'leads/update.html', context)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()

    return redirect('/leads')
