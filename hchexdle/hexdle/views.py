from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from os import getenv
import json

COLS = int(getenv('DJANGO_COLS'))
ROWS = int(getenv('DJANGO_ATTEMPTS'))
DICTIONARY = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f"]

class ContestantCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'hexdle/contestant_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        #save the new user first
        form.save()
        #get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        #authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

def home(request):
    if request.method == 'GET':
        context = {'cols': range(COLS), 'last_col': COLS-1, 'rows': range(ROWS), 'last_row': ROWS-1}
        return render(request, 'hexdle/home.html', context)
    else:
        return HttpResponseNotAllowed(['GET'])

def check_answer(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        if user.contestant.rattempts == 0:
            result = []
            for i in range(COLS):
                result.append('n')
            return JsonResponse({'remainingAttempts': user.contestant.rattempts, 'result': result, 'message': 'No remaining attempts.', 'gameOver': True})
        body_unicode = request.body.decode('utf-8')
        try:
            body_data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'The object is not a valid JSON.'})
        if 'answer' in body_data.keys():
            answer = body_data['answer']
            if len(answer) != COLS:
                return JsonResponse({'error': 'Answer must include exactly ' + str(COLS) + ' elements.'})
            userhash = list(user.contestant.hash)
            result = []
            for i in range(COLS):
                result.append('n')
            solved = 0
            for i in range(COLS):
                answer[i] = answer[i].lower()
                if answer[i] not in DICTIONARY:
                    return JsonResponse({'error': 'Character "' + answer[i]+ '" is invalid. Valid characters are ' + str(DICTIONARY)})
                if answer[i] == userhash[i]:
                    result[i] = 'y'
                    solved = solved + 1
                elif answer[i] in userhash:
                    result[i] = 'm'
            user.contestant.rattempts = user.contestant.rattempts - 1
            user.save()
            if solved == COLS:
                return JsonResponse({'remainingAttempts': user.contestant.rattempts,'result': result,
                'message': 'You found the HEX string. The flag is: ' + getenv('DJANGO_FLAG') + '.'})
            else:
                return JsonResponse({'remainingAttempts': user.contestant.rattempts,'result': result})
        else:
                return JsonResponse({'error': 'No answer provided.'})
    else:
        return HttpResponseNotAllowed(['POST'])