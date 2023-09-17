from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from .models import Photo, Categories


class LogIn(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('gallery')


class Register(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('gallery')
        return super(Register, self).get(*args, **kwargs)


def get_user_photo(request):
    print(request.user)
    category = request.GET.get('category')
    print(category)
    categories = Categories.objects.filter(user=request.user)
    print(categories)
    if category is None:
        photos = Photo.objects.filter(user=request.user)
    else:
        photos = Photo.objects.filter(user=request.user, category__name=str(category))
    print(photos)
    context = {
        'photos': photos,
        'categories': categories,
        }
    return render(request, 'main/gallery.html', context)


class PhotoList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'main/gallery.html'
    context_object_name = 'photos'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        category = self.request.GET.get('category')

        if category == None:
            context['photos'] = Photo.objects.all()
        else:
            context['photos'] = Photo.objects.filter(category__name=str(category))

        context['categories'] = Categories.objects.filter(user=self.request.user)

        return context


class PhotoDetail(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'main/photo.html'
    context_object_name = 'photo'



def AddPhoto(request):

    categories = Categories.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Categories.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Categories.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description = data['description'],
            image = image,
        )

        return redirect('gallery')

    context = {'categories':categories}
    return render(request,'main/add.html',context)


class DeletePhoto(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('gallery')
    template_name = 'main/delete.html'
    context_object_name = 'photo'


class UpdatePhoto(LoginRequiredMixin, UpdateView):
    model = Photo
    success_url = reverse_lazy('gallery')
    template_name = 'main/update.html'
    fields = ['category', 'description', 'image']


    def get_context_data(self, *args, **kwargs):
        context = super(UpdatePhoto , self).get_context_data(*args, **kwargs)
        image = self.request.GET.get('image')
        context['categories'] = Categories.objects.all()
        context['image'] = image
        return context
