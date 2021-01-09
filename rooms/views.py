from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 5
    paginate_orphans = 2
    context_object_name = "rooms"
    ordering = ("-created",)


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class SerchView(View):
    def get(self, request):
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            creater = form.cleaned_data.get("creater")
            tags = form.cleaned_data.get("tags")

            filter_args = {}

            if title is not None:
                filter_args["title__icontains"] = title

            if creater is not None:
                filter_args["creater__icontains"] = creater

            for tag in tags:
                filter_args["tag"] = tag

            rooms = models.Room.objects.filter(**filter_args)
            rooms = reversed(rooms)

            # To do
            # paginiate 제한, page nav 만들기

        return render(
            request,
            "rooms/search.html",
            {"form": form, "rooms": rooms},
        )
