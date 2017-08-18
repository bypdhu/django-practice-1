from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ", ".join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # use Django's template system to separate the design from Python
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list':latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))

    # use django.shortcuts.render and we no longer need to import loader and HttpResponse.
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # latest_question_list = get_list_or_404(Question)[:5]
    context = {
        'latest_question_list': latest_question_list,
        'app': "/polls",
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    #
    # try:
    #     question = Question.objects.get(pk=question_id)
    #     context = {'question': question}
    # except Question.DoesNotExist:
    #     raise Http404("Question doesn't not exist")
    # return render(request, 'polls/detail.html', context)

    # use shortcut http404.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # return HttpResponse("You're looking at the results of question %s." % question_id)

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s" % question_id)

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    #  the ListView generic view uses a default template called <app name>/<model name>_list.html;
    # we use template_name to tell ListView to use our existing "polls/index.html" template.
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # the DetailView generic view uses a template called <app name>/<model name>_detail.html.
    # In our case, it would use the template "polls/question_detail.html".
    # Use template_name to override it.
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
