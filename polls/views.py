from .models import Question, Choice
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic

#汎用ビューのindex
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
    
#古いindex(not 汎用ビュー)
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     #template = loader.get_template("polls/index.html")
#     context = {"latest_question_list":
#             latest_question_list}
#     return render(request, "polls/index.html", context)
#render() 関数は、第1引数として request オブジェクトを、
# 第2引数としてテンプレート名を、
# 第3引数（任意）として辞書を受け取ります

#汎用ビューのdetail
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

#古いdetail(not 汎用ビュー)
# def detail(request, question_id):
#     #get_object_or_404() 関数は、
#     # Django モデルを第一引数に、
#     # 任意の数のキーワード引数を取り、
#     # モデルのマネージャの get() 関数に渡します。
#     # オブジェクトが存在しない場合は 
#     # Http404 を発生させます。
#     question = get_object_or_404(Question,
#                                 pk=question_id)
#     return render(request, "polls/detail.html",
#                 {"question":question})

#def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exits")
    # return render(request, "polls/detail.html",
    #             {"question":question})


#汎用ビューのresult
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

#古いresult(not 汎用ビュー)
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question,
                                pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message" : "You didn't select a choice."
            }
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # POST データが成功した後は
        # 常に HttpResponseRedirect を返す必要がある
        return HttpResponseRedirect(reverse("polls:results",
                                            args=(question.id,)))

#def vote(request, question_id):
#    return HttpResponse("You're voting on question %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question,
                                pk=question_id)
    return render(request,"polls/results.html",
                {"question":question})