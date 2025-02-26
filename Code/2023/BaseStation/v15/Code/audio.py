import pygame
import time

def play_sound(channel, sound):
    if not channel.get_busy():
        channel.play(sound)
        return 1
    return 0


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    
    gernerateAudio = 0
    if gernerateAudio == 1:
        from gtts import gTTS
        import os
        
        audios = []
        for i in range(5):
            audios.append("Robot " + str(i+1) + " Connected")
            audios.append("Robot " + str(i+1) + " Disconnected")
            audios.append("Robot " + str(i+1) + " Low Battery")
            audios.append("Robot " + str(i+1) + " PC Low Battery")
            audios.append("Robot " + str(i+1) + " Incorrect Commit")
            audios.append("Robot " + str(i+1) + " High Temperature")
            audios.append("Robot " + str(i+1) + " Slow Loop")
            audios.append("Robot " + str(i+1) + " High CPU Usage")
            audios.append("Robot " + str(i+1) + " High GPU Usage")
        for i in audios:
            myobj = gTTS(text=i, lang='en', slow=False, tld='fr')
            myobj.save(i+".mp3")

    sound1 = pygame.mixer.Sound("audios/Robot 1 Connected.mp3")
    sound2 = pygame.mixer.Sound("audios/Robot 2 Connected.mp3")
    sound3 = pygame.mixer.Sound("audios/Robot 3 Connected.mp3")
    sound4 = pygame.mixer.Sound("audios/Robot 4 Connected.mp3")
    sound5 = pygame.mixer.Sound("audios/Robot 5 Connected.mp3")

    sounds = [sound1, sound2, sound3, sound4, sound5]
    channels = []

    for i in range(1, 5):
        channels.append(pygame.mixer.Channel(i))
        # channels[i-1].play(sounds[i-1])
        # time.sleep(0.5)

    time.sleep(3)

    channels[0].play(sounds[0])
    while channels[0].get_busy():
        pass
    channels[0].play(sounds[0])
    while channels[0].get_busy():
        pass