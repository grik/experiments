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

color_background = 'gray'

# width and height of the window in pixels (it matters only if fullscr == False
# win_width, win_height = 2560, 1440
win_width, win_height = 1000, 700

# create main window
mywin = visual.Window(
    [win_width, win_height],
    monitor='testMonitor',
    winType='pyglet',
    units='pix',
    fullscr=fullscr,
    rgb=color_background
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
fontsize_instruction = 35

color_font = 'white'
bolded_font = False

instruction_text = u'Za chwilę zostaną Ci zaprezentowane tablice ze znakami. '
instruction_text += u'Każda tablica będzie miała trzy rzędy. '
instruction_text += u'Po prezentacji każdej tablicy usłyszysz jeden z '
instruction_text += u'trzech dźwięków: wysoki, średni lub niski. \n'
instruction_text += u'Twoim zadaniem będzie przypomnienie sobie oraz '
instruction_text += u'zapisanie znaków z rzędu wskazanego przez wysokość '
instruction_text += u'dźwięku, odpowiednio: najwyższego rzędu, średniego lub '
instruction_text += u'dolnego. \n'
instruction_text += u'Błędnie wprowadzone znaki kasuj za pomocą klawisza '
instruction_text += u'BACKSPACE, a ostateczną decyzję zatwierdzaj za pomocą '
instruction_text += u'przycisku ENTER. \n'
instruction_text += u'\nJeśli nie pamiętasz znaków lub nie masz pewności - '
instruction_text += u'zgaduj. Musisz coś wprowadzić.\n'
instruction_text += u'\nPo naciśnięciu spacji usłyszysz przykłady dźwięków. '

end_text = u'Koniec eksperymentu. Dziękujemy za udział w badaniu. :)\n'
end_text += u'Proszę zawołaj eksperymentatora. Nie wstawaj jeszcze z miejsca.'

# with mask or without after the stimulus
mask_appear = True

# cue
fixation_point = False

# how many trials in one experiment
n_trials = 20

# matrix size: x rows, y columns
x, y = 3, 3

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
init_gap_time = 2.0

# stimulus exposure time, matrix of signs (in seconds)
exposure_time_matrix = 0.5

# Stimulus-onset asynchrony - time between the stimulus and the mask
soa_mask = 0.0

# stimulus exposure time, matrix of signs (in seconds)
exposure_time_mask = 0.25

# gap between mask (or matrix) and the sound
time_before_sound = 0.0

# for how long play the sound
sound_duration = 0.25

# gap between sound played and the recalling stage
time_after_sound = 0.0

# Inter Trial Interval, time between an answer and next stimulus (in seconds)
iti = 1.5

# collect all settings in one list to write it to the output file
settings = [
    n_trials, int(mask_appear), x, y, signs,
    init_gap_time, exposure_time_matrix, soa_mask, exposure_time_mask,
    time_before_sound, sound_duration, time_after_sound, iti
    ]

settings_labels = [
    'n_trials', 'mask_appear', 'x', 'y', 'signs',
    'init_gap_time', 'exposure_time_matrix', 'soa_mask', 'exposure_time_mask',
    'time_before_sound', 'sound_duration', 'time_after_sound', 'iti'
    ]

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

signs_list = []
for char in signs:
    signs_list.append(char)

mask_text = '\n'.join(' '.join(['#' for j in range(y)]) for i in range(x))


def generateStimulus(row, signs_list, x, y):
    random.shuffle(signs_list)

    stimulus = '\n'.join(
        ' '.join([signs_list[i*y+j] for j in range(y)]) for i in range(x)
        )
    correct = ''.join([signs_list[row*y+i] for i in range(y)])
    return stimulus, correct

trials = []
letters = []

# ### END OF GENERATE STIMULI
################################

################################
# ### CONSTANT BOARDS

# instruction text wrap is 90% of the window width
instruction = visual.TextStim(
    win=mywin,
    text=instruction_text,
    font='Monospace',
    pos=(0, 0), height=fontsize_instruction, wrapWidth=win_width*0.9,
    color=color_font, bold=bolded_font
    )

mask = visual.TextStim(
    win=mywin,
    text=mask_text, font='Monospace',
    pos=(0, 0), height=fontsize_stimuli,
    color=color_font, bold=bolded_font
    )

fix = visual.TextStim(
    win=mywin,
    text='+', font='Monospace',
    pos=(0, 0), height=fontsize_stimuli,
    color=color_font, bold=bolded_font
    )

empty = visual.TextStim(
    win=mywin,
    text='', font='Monospace',
    pos=(0, 0), height=fontsize_stimuli,
    color=color_font, bold=bolded_font
    )

end = visual.TextStim(
    win=mywin,
    text=end_text, font='Monospace',
    pos=(0, 0), height=fontsize_instruction,
    color=color_font, bold=bolded_font
    )
# ### END OF CONSTANT BOARDS
################################

################################
# ### SOUNDS

volume_main = 1.5

high = sound.Sound(
    value='C', sampleRate=44100, secs=sound_duration, bits=8, octave=6
    )
high.setVolume(volume_main * 0.05)

mid = sound.Sound(
    value='C', sampleRate=44100, secs=sound_duration, bits=8, octave=4
    )
mid.setVolume(volume_main * 0.25)

low = sound.Sound(
    value='C', sampleRate=44100, secs=sound_duration, bits=8, octave=2
    )
low.setVolume(volume_main * 0.5)

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
while True:
    keys_list = event.getKeys()
    if 'space' in keys_list:
        break
    elif 'escape' in keys_list:
        quit_experiment = True
        break

if not quit_experiment:
    empty.draw()
    mywin.flip()

    for snd in sounds:
        snd.play()
        core.wait(1.0)

    visual.TextStim(
        win=mywin,
        text=u'Naciśnij spację aby rozpocząć eksperyment.', font='Monospace',
        pos=(0, 0), height=fontsize_instruction,
        color=color_font, bold=bolded_font
        ).draw()
    mywin.flip()

    while True:
        keys_list = event.getKeys()
        if 'space' in keys_list:
            break
        elif 'escape' in keys_list:
            quit_experiment = True
            break

if not quit_experiment:
    if fixation_point:
        fix.draw()
    else:
        empty.draw()
    mywin.flip()
    core.wait(init_gap_time)

# iterate across all stimuli
for i in range(n_trials):

    if quit_experiment:
        break

    # randomly choose which row will be recalled
    row = random.randint(0, 2)

    # set current stimulus
    stimulus, correct = generateStimulus(row, signs_list, x, y)

    print(correct)

    # prepare matrix of signs which will be displayed
    matrix = visual.TextStim(
        win=mywin,
        text=stimulus, font='Monospace',
        pos=(0, 0), height=fontsize_stimuli,
        color=color_font, bold=bolded_font
        )

    # diplay the matrix of signs
    matrix.draw()
    mywin.flip()
    core.wait(exposure_time_matrix)

    # diplay the mask (if set)
    if mask_appear:
        # time gap between the matrix and the mask
        if soa_mask > 0.0:
            core.wait(soa_mask)
        mask.draw()
        mywin.flip()
        core.wait(exposure_time_mask)
    else:
        # even when no mask is applied it has to be the same amount of time
        empty.draw()
        mywin.flip()
        core.wait(exposure_time_mask)

    # play the sound indicating the row to be recalled
    if time_before_sound > 0.0:
        empty.draw()
        mywin.flip()
        core.wait(time_before_sound)

    # (re)set the empty space to fill
    # it has to be list because python doesn't allow: 'ab_'[2]='c'
    text_typed = []
    for i in range(x-1):
        text_typed.append(' ')
        text_typed.append(' ')
    text_typed.append(' ')

    # set counter to navigate which letter is the participant filling
    counter = 0

    # prepare the board with empty spaces to fill
    visual.TextStim(
        win=mywin,
        text=''.join(text_typed), font='Monospace',
        pos=(0, -160), height=fontsize_stimuli,
        color=color_font, bold=bolded_font
        ).draw()
    mywin.flip()

    sounds[row].play()

    if time_after_sound > 0.0:
        core.wait(time_after_sound)

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
                pos=(0, -160), height=fontsize_stimuli,
                color=color_font, bold=bolded_font
                ).draw()
            mywin.flip()
        # if all signs are inputed, go to another trial
        elif 'return' in keys_list:
            if counter == x*2:
                break
        # read sign pressed
        else:
            if counter < x*2:
                text_typed[counter] = keys_list[0].upper()
                if len(keys_list[0]) == 1:
                    visual.TextStim(
                        win=mywin,
                        text=''.join(text_typed), font='Monospace',
                        pos=(0, -160), height=fontsize_stimuli,
                        color=color_font, bold=bolded_font
                        ).draw()
                    mywin.flip()
                    counter += 2

    # break the experiement if appropriate key was pressed (by default: escape)
    if quit_experiment:
        break

    answer = ''.join(text_typed).replace(' ', '')

    trials.append(int(correct == answer))
    letters.append(sum([correct[i] == answer[i] for i in range(len(correct))]))

    if fixation_point:
        fix.draw()
    else:
        empty.draw()
    mywin.flip()
    core.wait(iti)

if not trials:
    print('Quitting, not even one trial acquired')
    mywin.close()
else:
    end.draw()
    mywin.flip()

    while 'escape' not in event.getKeys():
        pass

    mywin.close()
    trials_correct = sum(trials)
    letters_correct = sum(letters)

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

    register_labels = ['gender', 'age', 'faculty']

    with open('output.csv', 'a') as text_file:
        save = csv.writer(text_file)
        save.writerow(
            [time_code, letters_correct, trials_correct] +
            settings + register + trials + letters
            )

    with open('output_header.csv', 'a') as text_file:
        save = csv.writer(text_file)
        save.writerow(
            ['time_code', 'letters_correct', 'trials_correct'] +
            settings_labels + register_labels +
            ['trials' for i in range(len(trials))] +
            ['letters' for i in range(len(letters))]
            )

core.quit()
mywin.close()


################################################################
#
#               END OF EXPERIMENT
#
################################################################
