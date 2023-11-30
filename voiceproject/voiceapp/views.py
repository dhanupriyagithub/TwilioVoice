import os
from django.shortcuts import render
from django.http import HttpResponse
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.rest import Client
import time
import requests
from datetime import datetime, timedelta
from .models import CallRecord

account_sid = "AC4cc5b473630fa06d6b8f864f9c743582"
auth_token = "74998b5f06388dc6f7e8af97ff4d0935"

client = Client(account_sid, auth_token)

from_phone_number = "+19802245395"

recording_folder = "recording"

def upload_audio(request):
    if request.method == 'POST':
        to_phone_number = request.POST.get('phone_number')
        question1 = request.POST.get('question1')
        question2 = request.POST.get('question2')
        question3 = request.POST.get('question3')

        call_time_str = request.POST.get('call_time')
        call_time = datetime.strptime(call_time_str, '%H:%M').time()

        now = datetime.now().time()
        scheduled_time = datetime.combine(datetime.now().date(), call_time)
        if scheduled_time < datetime.now():
            scheduled_time += timedelta(days=1)

        delay_seconds = (datetime.combine(datetime.now().date(), call_time) - datetime.combine(datetime.now().date(), now)).total_seconds()

        time.sleep(delay_seconds)

        questions = [
            "Welcome to DCI. we are calling from HR team.",
            f"Question 1: {question1}",
            f"Okay Question 2: {question2}",
            f"Question 3: {question3}",
            "Thanks for your answers. We will get back to you shortly"
        ]

        def ask_question(question, gather, voice_response):
            gather.say(question)
            voice_response.append(gather)

        voice_response = VoiceResponse()
        for question in questions:
            gather = Gather(numDigits=1, action='/process_survey', method='POST')
            ask_question(question, gather, voice_response)
            time.sleep(5)

        call = client.calls.create(
            to=to_phone_number,
            from_=from_phone_number,
            twiml=str(voice_response),
            record=True
        )
        print(f"Calling {to_phone_number}...")
        time.sleep(70)

        call_sid = call.sid
        print(call_sid)
        recordings = client.recordings.list(call_sid=call_sid)
        print(recordings)

        recordings.sort(key=lambda x: x.date_created, reverse=True)
        recording_url = None
        if recordings:
            recording_media_url = recordings[0].media_url + ".wav"
            print(recording_media_url)
            auth = (account_sid, auth_token)
            print(auth)
            response = requests.get(recording_media_url, auth=auth)
            print(response)
            if response.status_code == 200:
                local_file_path = os.path.join(recording_folder, f"{to_phone_number}-recording.wav")

                with open(local_file_path, 'wb') as f:
                    f.write(response.content)

                print(f"Recording saved as {local_file_path}")
                
                recording_url = request.build_absolute_uri(f'E:/JAYA/daily_project/voice_AI/voiceproject/recording/{to_phone_number}-recording.wav')

        call_record = CallRecord(
            phone_number=to_phone_number,
            question1=question1,
            question2=question2,
            question3=question3,
            call_time=call_time,
            recording_url=recording_url
        )
        call_record.save()

        return HttpResponse("Call and recording completed.")

    return render(request, 'home.html')
