import subprocess

play_wait_sound = subprocess.Popen(["/home/pi/python_games/beep1.ogg"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#stop_wait_sound = play_wait_sound.stdin.write("q")

def soundgame():
    play_wait_sound
    if input == 1:
        #stop_wait_sound
        play_a_sound
    if input == 2:
        #stop_wait_sound
        return play_gameplay_sound
    if input == 3:
        #stop_wait_sound
        return play_another_sound