from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Tag,Post


class ObjectCreateMixin:
    model_form = None
    template = None
    def get(self, request):
        form = self.model_form()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model_form(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save(commit=False)
            user = User.objects.get(username=request.user)
            new_post.author_id = user.id
            new_post.save()
            return redirect(new_post)
        return render(request, self.template, context={'form': bound_form})