from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .PersonalData import PersonalData
from .forms import UploadFileForm, DocumentForm
# Imports
import os
import pandas as pd
from os import listdir
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pylev

import re

import seaborn as sns
sns.set_style('darkgrid')
sns.color_palette('Spectral')
import matplotlib.pyplot as plt


import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



User = get_user_model()

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            user_frame = []

            user_frame.append(pd.read_csv(request.FILES['document'].file.name, sep='\t', 
                            dtype={'rsid':'str', 'chromosome':'object', 'position':'int', 'genotype':'str'}, 
                            comment='#'))


            data_frame = pd.concat(user_frame, axis=0, ignore_index=True)

            df = pd.DataFrame(data_frame)
            print(df.info)
           # print(pd.head())
        
          #  handle_uploaded_file(request.FILES)
            form.save()
               # return HttpResponseRedirect('/success/url/')
           # return User.objects.get(file=self.request.FILES['file'])
      #  return redirect('home')
            messages.add_message(
                    request, messages.INFO, _("File successfully uploaded")
                )

    else:
        form = DocumentForm()
    return render(request, '/home/mark/vscode/user-data/personal/phenotype/srv/phenotype/phenotype/templates/users/upload.html', {
        'form': form
    })

# Imaginary function to handle an uploaded file.
class UserUploadView(LoginRequiredMixin, UpdateView):
    model = User
    def upload_file(self, request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
               # return HttpResponseRedirect('/success/url/')
                return User.objects.get(file=self.request.FILES['file'])
        else:
            form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
'''
    def model_form_upload(self, request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DocumentForm()
        return render(request, 'upload.html', {
            'form': form
        })
'''

user_upload_view = UserUploadView.as_view()

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)

user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

user_redirect_view = UserRedirectView.as_view()
