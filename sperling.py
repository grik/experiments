#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
name:
sperling.py

type:
script

description:
This script allows to conduct a cognitive experiment which is a replication
of an experiment originaly designed by George Sperling.
'''

from psychopy import visual, event, core, sound, gui
import random
import datetime
import csv


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
fontsize_stimuli = 70
fontsize_instruction = 30

instruction_text = u'Za chwilę zostaną Ci zaprezentowane tablice ze znakami. '
instruction_text += u'Każda tablica będzie miała trzy rzędy. '
instruction_text += u'Po prezentacji każdej tablicy usłyszysz jeden z '
instruction_text += u'trzech dźwięków: wysoki, średni lub niski. \n'
instruction_text += u'Twoim zadaniem będzie przypomnienie sobie oraz zapisanie '
instruction_text += u'znaków z rzędu wskazanego przez wysokość dźwięku: '
instruction_text += u'odpowiednio: najwyższego rzędu, średniego lub dolnego. \n'
instruction_text += u'\nAby rozpocząć naciśnij spację. '

# with mask or without after the stimulus
mask_appear = True

# how many trials in one experiment
n_trials = 2

# matrix size: x rows, y columns
x, y = 3, 4

########################
# Available signs

# # numbers
# signs = '1234567890'

# # Polish upper cases (without diacritics)
# signs = 'ABCDEFGHIJKLMNOPRSTUWZ'

# # English upper cases
# signs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# English upper cases (consonants only, without 'Y')
signs = 'BCDFGHJKLMNPQRSTVWXZ'
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

    Od tego miejsca program sam przemieli zmienna 'stimuli_raw' tak, zeby dalo
    sie ja wyswietlic za pomoca psychopy.

stimuli = []
mask = ''.join([i + '\n' for i in mask_raw])

for stimulus_raw in stimuli_raw:
    stimuli.append(''.join([i + '\n' for i in stimulus_raw]))

trials = []
'''


signs_list = []
for char in signs:
    signs_list.append(char)

mask = ''
for i in range(x):
        for j in range(y):
            mask += '# '
        mask += '\n'


def generateStimulus(row, signs_list, x, y):
    random.shuffle(signs_list)
    stimulus = ''
    stimulus_list = []
    n = 0
    for i in range(x):
        verse = ''
        for j in range(y):
            verse += signs_list[j+n] + ' '
        n += y
        stimulus_list.append(verse)
    correct = ''.join(stimulus_list[row])
    correct = correct.replace(' ', '')
    stimulus = ''.join(i + '\n' for i in stimulus_list)
    return stimulus, correct

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
    pos=(0, 0), height=fontsize_instruction, wrapWidth=win_width*0.9
    )

mask = visual.TextStim(
    win=mywin,
    text=mask, font='Monospace',
    pos=(0, 0), height=fontsize_stimuli
    )

empty = visual.TextStim(
    win=mywin,
    text='', font='Monospace',
    pos=(0, 0), height=fontsize_stimuli
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
for i in range(n_trials):

    # randomly choose which row will be recalled
    row = random.randint(0, 2)

    # set current stimulus
    stimulus, correct = generateStimulus(row, signs_list, x, y)

    print(correct)

    # prepare matrix of signs which will be displayed
    matrix = visual.TextStim(
        win=mywin,
        text=stimulus, font='Monospace',
        pos=(0, 0), height=fontsize_stimuli
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
        pos=(0, -100), height=fontsize_stimuli
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

if not trials:
    'Quitting, not even one trial acquired'
else:
    trials_correct = sum(trials)
    trials_total = len(trials)

    percent_correct = int((sum(trials)/float(len(trials))) * 100)
    print('correct answers: %s/%s' % (sum(trials), len(trials)))
    print('percent correct: %s%%' % percent_correct)

    scores = [trials_correct, trials_total, percent_correct]

    info = {
        'kierunek(p=psycho/c=cogni/i=inny/n=nie studiuje)': 'i',
        'wiek': 21,
        'plec(k/m)': 'k'
        }
    box = gui.DlgFromDict(dictionary=info, title='Dane')
    if not (box.OK):
        core.quit()

    register = []
    register.append(info['plec(k/m)'])
    register.append(info['wiek'])
    register.append(info['kierunek(p=psycho/c=cogni/i=inny/n=nie studiuje)'])

    with open('output/output_%s.csv' % time_code, 'w') as text_file:
        save = csv.writer(text_file)
        save.writerow(scores + register)

mywin.close()


################################################################
#
#               END OF EXPERIMENT
#
################################################################
