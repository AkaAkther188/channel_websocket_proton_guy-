from django.shortcuts import render,redirect
from .models import Room,Message

def CreateRoom(request):
    if request.method == 'POST':
        
        username = request.POST.get('user_name')
        room = request.POST.get('room')
        
        try:
            get_room = Room.objects.get(room_name=room)

        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
        return redirect('room', room_name=room, username=username)
        
    return render(request, 'index.html')

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    
    Message.objects.filter(room=get_room).exclude(sender=username).update(seen=True)
    get_message = Message.objects.filter(room=get_room)

    context = {
        "message": get_message,
        "user": username,
        "room_name": room_name,
    }

    return render(request, '_message.html', context)


