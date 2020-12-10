import datetime as dt
from django.shortcuts import render, redirect
from django.http  import HttpResponse,Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, ListView
from .models import *
from .filters import UserFilter
from .forms import *
from .email import send_welcome_email
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from .permissions import IsAdminOrReadOnly


# Create your views here.
def home(req):
    return render(req, "index.html")

class UserDetail(LoginRequiredMixin, DetailView):
    model = Profile
    
class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)

        permission_classes = (IsAdminOrReadOnly,)
    
    def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_merch(self, pk):
        try:
            return MoringaMerch.objects.get(pk=pk)
        except MoringaMerch.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch)
        return Response(serializers.data)
    
def register(req):
    if req.method == "POST":
        Form = UserRegisterForm(req.POST)
        if Form.is_valid():
            Form.save()
            username = Form.cleaned_data.get("username")
            email = form.cleaned_data['email']
            messages.success(req, f"You can now log in the account you have created with us.")
            
            
            recipient = subscriber(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            data = {'success': 'You have been successfully added to mailing list'}
            return JsonResponse(data)

            return redirect("login")
    else:
        Form = UserRegisterForm()
    return render(req, "django-registration/registration_form.html", {'form': Form})


@login_required
def profile(req):
    user = req.user
    profile = Profile.objects.get(user=user)
    likes = profile.num_likes
    unreadMessages = Message.objects.filter(
        receiver=req.user).filter(status=False).count()
    if req.method == "POST":
        form = ProfileUpdateForm(
            req.POST, req.FILES, instance=req.user.profile)

        if form.is_valid():
            form.save()
            messages.success(req, "User Profile account updated.")
            return redirect("profile-page")
    else:
        form = ProfileUpdateForm(instance=req.user.profile)

    context = {
        'form': form,
        'likes': likes,
        'unreadmsgs': unreadMessages
    }

    return render(req, "user_registration/user_profile.html", context)

def unauthenticated_user(view_func):
    def unauthenticated(req, *args, **kwargs):
        if req.user.is_authenticated:
            return redirect("date-page")
        else:
            return view_func(req, *args, **kwargs)
    return unauthenticated

@login_required
def likePost(req, pk):
    user = get_object_or_404(Profile, id=req.POST.get("user_id"))

    if req.user in user.likeability.all():
        user.likeability.remove(req.user)
    else:
        user.likeability.add(req.user)
        if user.user in req.user.profile.likeability.all():
            messages.success(
                req, f"Perfect match! {user.full_name} likes you back.")
    return redirect("home-page")

class WriteMessage(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        pk = self.kwargs.get("username")
        form.instance.receiver = User.objects.get(username=pk)
        return super().form_valid(form)


class DeleteMessage(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = "/"


@login_required
def ViewMessages(req):
    messages = Message.objects.filter(receiver=req.user)
    unreadMessages = Message.objects.filter(
        receiver=req.user).filter(status=False).count()
    userIn = req.user

    context = {
        'msgs': messages,
        'userIn': userIn,
        'unreadmsgs': unreadMessages
    }

    return render(req, "messages/message.html", context)


@login_required
def MarkAsRead(req, pk):
    msg_id = req.POST.get("msg_id")
    message = Message.objects.get(pk=req.POST.get("msg_id"))
    message.status = True
    message.save()

    return redirect("view-messages")

@login_required
def datePage(req):
    users = Profile.objects.all()
    user = req.user
    unreadMessages = Message.objects.filter(
        receiver=user).filter(status=False).count()

    myFilter = UserFilter(req.GET, queryset=users)
    users = myFilter.qs

    context = {
        'users': users,
        'userIn': user,
        'filter': myFilter,
        'unreadmsgs': unreadMessages
    }
    return render(req, "date.html", context)

@login_required
def blockUser(req, pk):
    user = get_object_or_404(Profile, id=req.POST.get("user_id"))

    if req.user not in user.blocked_by.all():
        user.blocked_by.add(req.user)

    return redirect("home-page")

@login_required
def deleteuser(request):
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('blog-home')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'delete account/delete_account.html', context)
