#!/usr/bin/env python2

'''
name:
sperling.py

type:
script

description:
This script allows to conduct a cognitive experiment which is a replication
of an experiment originaly designed by George Sperling.
'''

from psychopy import visual, event, core, sound
from random import randint
import datetime


################################################################
#
#               VARIABLES SETTINGS
#
################################################################

################################
# ### MONITOR AND WINDOW

# for debugging process it is recomendened not to use fulscreen
fullscr = False

# width and height of the window in pixels (it matters only if fullscr == False
# win_width, win_height = 2560, 1440
win_width, win_height = 1000, 700

# create main window
mywin = visual.Window(
    [win_width, win_height],
    monitor='testMonitor',
    winType='pyglet',
    units='pix',
    fullscr=fullscr
    )
mywin.setMouseVisible(False)

# flag in case experimenter decides to stop the experiment
quit_experiment = False

# ### END OF MONITOR AND WINDOW
################################

################################
# ### STIMULI SETTINGS

# size of the font for stimuli
fontsize = 70

instruction_text = 'You will be shown boards with letters. '
instruction_text += 'After that you will hear one of three tones: '
instruction_text += 'high, medium or low. \n'
instruction_text += 'Your task is ... \n\n'
instruction_text += 'Press space if you are ready'

# with mask or without after the stimulus
mask_appear = True

# how many trials in one experiment
n_trials = 10

# matrix size
x, y = 3, 4

########################
# Available signs

# # numbers
# signs = '1234567890'

# # Polish upper cases (without diacritics)
# signs = 'ABCDEFGHIJKLMNOPRSTUWZ'

# English upper cases
signs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
########################

# time before first stimulus appears, after instruction (in seconds)
init_gap_time = 1.0

# stimulus exposure time, matrix of signs (in seconds)
exposure_time_matrix = 0.5

# Stimulus-onset asynchrony - time between the stimulus and the mask
soa = 0.0

# stimulus exposure time, matrix of signs (in seconds)
exposure_time_mask = 0.5

# gap between mask (or matrix) and the sound
time_before_sound = 0.5

# for how long play the sound
sound_duration = 0.5

# gap between sound played and the recalling stage
time_after_sound = 0.5

# Inter Trial Interval, time between an answer and next stimulus (in seconds)
iti = 1.0

# ### END OF STIMULI SETTINGS
################################

################################################################
#
#               END OF VARIABLES SETTINGS
#
################################################################


################################################################
#
#               PRELIMINARIES
#
################################################################

################################
# ### GENERATE STIMULI
'''
    Tutaj trzeba wrzucic generator generujacy bodzce.
    Dostepne znaki nalezy zczytac ze zmiennej 'signs', a wymiary matrycy
    ze zmiennych 'x' oraz 'y'.
    Format bodzcow musi byc taki jak w 'stimuli_raw' przedstawionych ponizej.

    Na koniec musi sie tez wygenerowac maska o takich samych rozmiarach
    jak matryca.
'''
stimuli_raw = [
    [
        'A B C D',
        'E F G H',
        'J K L M'
    ],
    [
        'J K L M',
        'A B C D',
        'E F G H',
    ],
    ]

mask_raw = [
    '# # # #',
    '# # # #',
    '# # # #'
    ]

'''
    Od tego miejsca program sam przemieli zmienna 'stimuli_raw' tak, zeby dalo
    sie ja wyswietlic za pomoca psychopy.
'''

stimuli = []
mask = ''.join([i + '\n' for i in mask_raw])

for stimulus_raw in stimuli_raw:
    stimuli.append(''.join([i + '\n' for i in stimulus_raw]))

trials = []
# ### END OF GENERATE STIMULI
################################

################################
# ### CONSTANT BOARDS

# instruction text wrap is 90% of the window width
instruction = visual.TextStim(
    win=mywin,
    text=instruction_text,
    font='Monospace',
    pos=(0, 0), height=fontsize, wrapWidth=win_width*0.9
    )

mask = visual.TextStim(
    win=mywin,
    text=mask, font='Monospace',
    pos=(0, 0), height=fontsize
    )

empty = visual.TextStim(
    win=mywin,
    text='', font='Monospace',
    pos=(0, 0), height=fontsize
    )
# ### END OF CONSTANT BOARDS
################################

################################
# ### SOUNDS
low = sound.Sound(
    value='C', sampleRate=44100, secs=sound_duration, bits=8, octave=3
    )
low.setVolume(0.45)

mid = sound.Sound(
    value='C', sampleRate=44100, secs=sound_duration, bits=8, octave=4
    )
mid.setVolume(0.35)

high = sound.Sound(
    value='C', sampleRate=44100, secs=sound_duration, bits=8, octave=5
    )
high.setVolume(0.1)

sounds = [high, mid, low]
# ### END OF SOUNDS
################################

################################################################
#
#               END OF PRELIMINARIES
#
################################################################


################################################################
#
#               EXPERIMENT
#
################################################################

# code the time to name file or variable
time_code = datetime.datetime.now().strftime("%Y%m%d%H%M")

################################
# ### INSTRUCTION

instruction.draw()
mywin.flip()

# wait until space pressed
while 'space' not in event.getKeys():
    pass

# iterate across all stimuli
for i in range(len(stimuli)):

    # set current stimulus
    stimulus = stimuli[i]

    # randomly choose which row will be recalled
    row = randint(0, 2)

    # the correct answer is...
    correct = stimuli_raw[i][row].replace(' ', '')

    print(correct)

    # prepare matrix of signs which will be displayed
    matrix = visual.TextStim(
        win=mywin,
        text=stimulus, font='Monospace',
        pos=(0, 0), height=fontsize
        )

    # diplay the matrix of signs
    matrix.draw()
    mywin.flip()
    core.wait(exposure_time_matrix)

    # diplay the mask (if set)
    if mask_appear:
        # time gap between the matrix and the mask
        if soa > 0.0:
            core.wait(soa)
        mask.draw()
        mywin.flip()
        core.wait(exposure_time_mask)

    # play the sound indicating the row to be recalled
    empty.draw()
    mywin.flip()
    core.wait(time_before_sound)

    sounds[row].play()

    core.wait(time_after_sound)

    # (re)set the empty space to fill
    # it has to be list because python doesn't allow: 'ab_'[2]='c'
    text_typed = ['_', ' ', '_', ' ', '_',  ' ', '_']

    # set counter to navigate which letter is the participant filling
    counter = 0

    # prepare the board with empty spaces to fill
    visual.TextStim(
        win=mywin,
        text=''.join(text_typed), font='Monospace',
        pos=(0, -100), height=fontsize
        ).draw()
    mywin.flip()

    # filling begins
    while True:
        # get the key pressed
        keys_list = event.getKeys()
        # if empty check another time if the participant has pressed something
        if not keys_list:
            pass
        # escape quits the experiment
        elif 'escape' in keys_list:
            quit_experiment = True
            break
        # remove previous character
        elif 'backspace' in keys_list:
            if counter >= 2:
                counter -= 2
            text_typed[counter] = '_'
            visual.TextStim(
                win=mywin,
                text=''.join(text_typed), font='Monospace',
                pos=(0, -100), height=fontsize
                ).draw()
            mywin.flip()
        # if all signs are inputed, go to another trial
        elif 'return' in keys_list:
            if counter == 8:
                break
        # read sign pressed
        else:
            if counter < 8:
                text_typed[counter] = keys_list[0].upper()
                if len(keys_list[0]) == 1:
                    visual.TextStim(
                        win=mywin,
                        text=''.join(text_typed), font='Monospace',
                        pos=(0, -100), height=fontsize
                        ).draw()
                    mywin.flip()
                    counter += 2

    # break the experiement if appropriate key was pressed (by default: escape)
    if quit_experiment:
        break

    answer = ''.join(text_typed).replace(' ', '')

    trials.append(int(correct == answer))

trials_correct = sum(trials)
trials_total = len(trials)

percent_correct = int((sum(trials)/float(len(trials))) * 100)
print('correct answers: %s/%s' % (sum(trials), len(trials)))
print('percent correct: %s%%' % percent_correct)

with open('output_%s.txt' % time_code, 'w') as text_file:
    text_file.write(
        '{}, {}, {}\n'.format(trials_correct, trials_total, percent_correct)
        )

mywin.close()

################################################################
#
#               END OF EXPERIMENT
#
################################################################
