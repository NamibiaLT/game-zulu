import pygame

pygame.init()
pygame.mixer.init()

#### Sounds ####
soundWarningMissile = pygame.mixer.Sound("sound/warning_incoming_missile.wav")
soundMissile = pygame.mixer.Sound("sound/missile.wav")
soundSuccess = pygame.mixer.Sound("sound/success.wav")
soundTrumpet = pygame.mixer.Sound("sound/trumpet.wav")
soundGateSuccess = pygame.mixer.Sound("sound/sound_gate_success.wav") 
soundButtonPushDead = pygame.mixer.Sound("sound/button_push_dead.wav")
soundButtonDead = pygame.mixer.Sound("Sound/button-10.wav")
soundButtonPush1 = pygame.mixer.Sound("sound/button_push_1.wav")
soundbuttonPush2 = pygame.mixer.Sound("sound/button_push_2.wav")

#### Background Music ####
introMusicSpace = "sound/intro_music_space.wav"
gamePlayMusic = 'sound/spooky_gameplay.wav'
lava = "sound/lava.wav"
