from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect
from django.urls import *

from .models import *
from .forms import *

from django_filters.views import FilterView
from .filters import MeteoriteClassFilter

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def index(request):
    return HttpResponse("Hello, Welcome to Meteorite Landing Website!.")

class AboutPageView(generic.TemplateView):
    template_name = 'meteorite_landings/about.html'

class HomePageView(generic.TemplateView):
    template_name = 'meteorite_landings/home.html'

@method_decorator(login_required, name='dispatch')
class CountryAreaListView(generic.ListView):
    model = CountryArea
    context_object_name = 'countries'
    template_name = 'meteorite_landings/country_area.html'
    paginate_by = 20

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return CountryArea.objects.order_by('country_area_name')

@method_decorator(login_required, name='dispatch')
class CountryAreaDetailView(generic.DetailView):
    model = CountryArea
    context_object_name = 'country'
    template_name = 'meteorite_landings/country_area_detail.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MeteoriteClassListView(generic.ListView):
    model = MeteoriteClass
    context_object_name = 'meteorite_classes'
    template_name = 'meteorite_landings/meteorite_class.html'
    paginate_by = 20

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return MeteoriteClass.objects.order_by('code')

@method_decorator(login_required, name='dispatch')
class MeteoriteClassDetailView(generic.DetailView):
    model = MeteoriteClass
    context_object_name = 'meteorite_class'
    template_name = 'meteorite_landings/meteorite_class_detail.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MeteoriteClassCreateView(generic.View):
    model = MeteoriteClass
    form_class = MeteoriteClassForm
    success_message = "Meteorite Class created successfully"
    template_name = "meteorite_landings/meteorite_class_new.html'"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = MeteoriteClassForm(request.POST)
        if form.is_valid():
            meteorite_class = form.save(commit=False)
            meteorite_class.save()
            for country in form.cleaned_data['country_area']:
                MeteoriteLanding.objects.create(meteorite_class=meteorite_class, country_area=country)
            return redirect(meteorite_class)
        else:
            return render(request, 'meteorite_landings/meteorite_class_new.html', {'form': form})

    def get(self, request):
        form = MeteoriteClassForm()
        return render(request, 'meteorite_landings/meteorite_class_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class MeteoriteClassUpdateView(generic.UpdateView):
    model = MeteoriteClass
    form_class = MeteoriteClassForm
    context_object_name = 'meteorite_class'
    success_message = "Meteorite Class updated successfully"
    template_name = "meteorite_landings/meteorite_class_update.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        meteorite_class = form.save(commit=False)
        meteorite_class.save()

        old_ids = MeteoriteLanding.objects.values_list('country_area_id', flat=True)\
                                          .filter(meteorite_class_id=meteorite_class.meteorite_class_id)

        new_countries = form.cleaned_data['country_area']
        new_ids = []

        for country in new_countries:
            new_id = country.country_area_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                MeteoriteLanding.objects\
                    .create(meteorite_class=meteorite_class, country_area=country)

        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                MeteoriteLanding.objects\
                    .filter(meteorite_class_id=meteorite_class.meteorite_class_id, country_area_id=old_id)\
                    .delete()

        return HttpResponseRedirect(meteorite_class.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class MeteoriteClassDeleteView(generic.DeleteView):
    model = MeteoriteClass
    success_message = "Meteorite Class deleted successfully"
    success_url = reverse_lazy('meteorite_classes')
    context_object_name = 'meteorite_class'
    template_name = "meteorite_landings/meteorite_class_delete.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        MeteoriteLanding.objects\
            .filter(meteorite_class_id=self.object.meteorite_class_id)\
            .delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class MeteoriteClassFilterView(FilterView):
    filterset_class = MeteoriteClassFilter
    template_name = 'meteorite_landings/meteorite_class_filter.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MeteoriteLandingListView(generic.ListView):
    model = MeteoriteLanding
    context_object_name = 'meteorite_landings'
    template_name = 'meteorite_landings/meteorite_landing.html'
    paginate_by = 100

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return MeteoriteLanding.objects.order_by('country_area', 'meteorite_class')

@method_decorator(login_required, name='dispatch')
class MeteoriteLandingDetailView(generic.DetailView):
    model = MeteoriteLanding
    context_object_name = 'meteorite_landing'
    template_name = 'meteorite_landings/meteorite_landing_detail.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MeteoriteLandingUpdateView(generic.UpdateView):
    model = MeteoriteLanding
    form_class = MeteoriteLandingForm
    context_object_name = 'meteorite_landing'
    success_message = "Meteorite Landing information updated successfully"
    template_name = "meteorite_landings/meteorite_landing_update.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        print('form is valid')
        meteorite_landing = form.save(commit=False)
        meteorite_landing.save()
        print(meteorite_landing.get_absolute_url())
        return HttpResponseRedirect(meteorite_landing.get_absolute_url())
