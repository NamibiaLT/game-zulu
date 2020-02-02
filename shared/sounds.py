import pygame

pygame.init()
pygame.mixer.init()

#### Sounds ####
soundWarningMissile = pygame.mixer.Sound("warning_incoming_missile.wav")
soundMissile = pygame.mixer.Sound("sounds/missile.wav")
soundSuccess = pygame.mixer.Sound("sounds/success.wav")
soundTrumpet = pygame.mixer.Sound("sounds/trumpet.wav")
soundGateSuccess = pygame.mixer.Sound("sounds/sound_gate_success.wav") 
soundButtonPushDead = pygame.mixer.Sound("sounds/button_push_dead.wav")
soundButtonDead = pygame.mixer.Sound("sounds/button-10.wav")
soundButtonPush1 = pygame.mixer.Sound("sounds/button_push_1.wav")
soundbuttonPush2 = pygame.mixer.Sound("sounds/button_push_2.wav")

#### Background Music ####
introMusicSpace = "sounds/intro_music_space.wav"
gamePlayMusic = 'sounds/spooky_gameplay.wav'
lava = "sounds/lava.wav"
