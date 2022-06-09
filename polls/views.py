from bs4 import BeautifulSoup
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def wordcloud(request):
    context = {}
    return render(request, 'polls/wordcloud.html', context)


def showwordcloud(request):
    query = request.POST['query']

    from . import news_wordcloud
    from wordcloud import WordCloud
    from konlpy.tag import Hannanum
    import pandas as pd
    from collections import Counter

    news_wordcloud.collect_and_store(query)
   
    hannanum = Hannanum()

    txt = open('./polls/news.txt', 'r')
    soup = BeautifulSoup(txt, 'html.parser')

    contents = soup.select('#dic_area')[0].get_text()

    lines = contents.splitlines()

    temp = []
    for i in range(len(lines)):
        temp.append(hannanum.nouns(lines[i]))

    def flatten(l):
        flatList = []
        for elem in l:
            if type(elem) == list:
                for e in elem:
                    flatList.append(e)
            else:
                flatList.append(elem)
        return flatList

    word_list = flatten(temp)
    word_list = pd.Series([x for x in word_list if len(x) > 1])

    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

    wordcloud = WordCloud(
        font_path = font_path,
        width = 800,
        height = 800,
        background_color="white"
    )

    count = Counter(word_list)
    wordcloud = wordcloud.generate_from_frequencies(count)
    array = wordcloud.to_array()

    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(5,5))
    plt.imshow(array, interpolation="bilinear")
    plt.show()
    fig.savefig('./polls/static/polls/images/newswordcloud.png')

    context = {"query": query}
    return render(request, 'polls/showwordcloud.html', context)