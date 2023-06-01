from django.shortcuts import render
from .models import Chat
# Create your views here.
def chat(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        Chat(text=text).save()
    return render(request,'chat/index.html',{
        'messages':Chat.objects.all()
    })
    
def chatdelete(request,id):
    try:
        Chat.objects.get(id=id).delete()
    except:
        pass
    return render(request,'chat/index.html',{
        'messages':Chat.objects.all()
    })