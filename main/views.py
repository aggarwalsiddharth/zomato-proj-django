from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,UpdateView,DetailView,DeleteView,FormView,CreateView,ListView
from django.views.generic.edit import FormMixin
from django.urls import reverse,reverse_lazy
from django import forms
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import forms,models
from django.db.models import Avg
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.

class SuccessView(TemplateView):
    template_name = 'main/success.html'

def login_view(request):

    if request.method == "GET":
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)

                try:
                    return HttpResponseRedirect(request.GET['next'])
                except KeyError:
                    return HttpResponseRedirect( reverse('index') )
    context = {
        "form": form
    }
    return render(request, 'main/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect( reverse('login') )

class Signup(CreateView):
    form_class = UserCreationForm
    success_url =reverse_lazy('login')
    template_name = 'main/signup.html'

class Addrestaurant(CreateView):
    model = models.Restaurant
    fields = '__all__'
    success_url = '/success/'
    template_name = 'main/addrestaurant.html'

@method_decorator(login_required, name = 'dispatch')
class RestaurantDetail(FormMixin,DetailView):
    template_name = 'main/restaurant_detail.html'
    model = models.Restaurant
    context_object_name = 'restaurant'
    success_url = 'success/'
    form_class = forms.ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=self.get_form()
        return context

    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
        else:
            self.form_invalid(form)

        return HttpResponseRedirect(redirect_to='/success/')

    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.restaurant = self.get_object()
        obj.save()
        return super().form_valid(form)





# @method_decorator(login_required,name = 'dispatch')
# class Index(TemplateView):
#     template_name = 'main/index.html'
#     if request.user.is_authenticated:
#         username = request.user.username
@login_required
def index(request):
    username = request.user.username
    context ={
        'username':username,
    }
    return render(request,'main/index.html',context)

class RestaurantList(ListView):
    paginate_by = 10
    model = models.Restaurant
    template_name = 'main/restaurant_list.html'
    context_object_name = 'restaurants'
    qs = f = r = None

    def get(self, request, *args, **kwargs):
        self.qs = models.Restaurant.objects.all()
        self.f = request.GET['filter']
        self.r = request.GET['reverse']


        if self.f == 'a2z' and self.r == 'False':
            self.qs = self.qs.order_by('name')
        elif self.f == 'a2z' and self.r == 'True':
            self.qs = self.qs.order_by('-name')
        elif self.f == 'rating' and self.r == 'False':
            self.qs = self.qs.annotate(average_rating=Avg('review__rating')).order_by('average_rating')
        elif self.f == 'rating' and self.r == 'True':
            self.qs = self.qs.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')

        return super().get(request)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurants'] = self.qs
        context['f'] = self.f
        context['r'] = self.r
        return context