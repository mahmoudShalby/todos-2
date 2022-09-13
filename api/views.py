from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Todo


def all(request):
  return JsonResponse(serialize('json', Todo.objects.all()), safe=False)

def new(request):
  if request.method == 'GET' and 'content' in request.GET:
    todo = Todo.objects.create(content=request.GET['content'])
    todo.save()
    return JsonResponse(serialize('json', [todo]), safe=False)
  else:
    return JsonResponse('false', safe=False)

def delete(request):
  if request.method == 'GET' and 'id' in request.GET:
    try:
      todo = Todo.objects.get(id=request.GET['id'])
      todo.delete()
      return JsonResponse('true', safe=False)
    except Todo.DoesNotExist:
      return JsonResponse('false', safe=False)
  else:
    return JsonResponse('false', safe=False)

def edit(request):
  if request.method == 'GET' and 'id' in request.GET and 'new-content' in request.GET:
    try:
      todo = Todo.objects.get(id=request.GET['id'])
      todo.content = request.GET['new-content']
      todo.save()
      return JsonResponse('true', safe=False)
    except Todo.DoesNotExist:
      return JsonResponse('false', safe=False)
  else:
    return JsonResponse('false', safe=False)
