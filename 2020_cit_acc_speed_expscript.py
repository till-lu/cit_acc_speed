#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from psychopy.visual import Window, TextStim
from psychopy.core import wait, Clock, quit
from psychopy.event import clearEvents, waitKeys, Mouse
from psychopy.gui import Dlg
from time import gmtime, strftime
from codecs import open
from random import shuffle, choice, randint
from copy import deepcopy
from psychopy.iohub import launchHubServer
from numpy import mean, std
from datetime import datetime
from itertools import permutations

## for testing
testing = False # True for testing, False for real recording
###
main_ddline = 1 # sec
isi_min_max = (500, 800)
instruction_color = '#9999FF'
############ MAIN ITEMS - paste from JS

birthdays_items =  [u"FEB 25", u"APR 17", u"MAI 21", u"JUL 12", u"SEP 27", u"OKT 06", u"NOV 08", u"DEZ 19"]

#male_forenames = [u"Nico", u"Justin", u"Jakob", u"Gerald", u"Max", u"Mario", u"Jürgen", u"Ferdinand", u"Simon", u"Harald", u"Andre", u"Gregor", u"Martin", u"Julian", u"Berat", u"Robert", u"Leonard", u"Theodor", u"Arthur", u"Emir", u"Theo", u"Marcel", u"Lorenz", u"Moritz", u"Samuel", u"Stefan", u"Anton", u"Felix", u"Herbert", u"Clemens", u"Gerhard", u"Peter", u"Sascha", u"Richard", u"Günther", u"Ali", u"Johann", u"Nicolas", u"Leo", u"Alexander", u"Emanuel", u"Manfred", u"Klaus", u"Roland", u"Laurenz", u"Valentin", u"Dominik", u"Marvin", u"Helmut", u"Hamza", u"Viktor", u"Jonathan", u"Josef", u"Christoph", u"Markus", u"Pascal", u"Maximilian", u"Finn", u"Mathias", u"Rafael", u"Roman", u"Yusuf", u"Manuel", u"Oliver", u"Rene", u"Karl", u"Adam", u"Christopher", u"Jan", u"Kilian", u"Michael", u"Jonas", u"Werner", u"Kevin", u"David", u"Emil", u"Constantin", u"Noah", u"Bernhard", u"Bernd", u"Georg", u"Marco", u"Florian", u"Franz", u"Fabio", u"Wolfgang", u"Thomas", u"Vincent", u"Christian", u"Andreas", u"Erik", u"Johannes", u"Tobias", u"Benjamin", u"Ben", u"Sandro", u"Armin", u"Daniel", u"Reinhard", u"Benedikt", u"Amir", u"Gernot", u"Elias", u"Gabriel", u"Patrik", u"Andrej", u"Konstantin", u"Oskar", u"Sebastian", u"Matthias", u"Fabian", u"Hannes", u"Paul", u"Leon", u"Tim", u"Leopold", u"Adrian"]

#fem_forenames = [u"Sandra", u"Jacqueline", u"Johanna", u"Celine", u"Silvia", u"Ecrin", u"Verena", u"Sofia", u"Sophie", u"Hira", u"Cornelia", u"Valerie", u"Angelina", u"Lina", u"Miriam", u"Petra", u"Natalie", u"Simone", u"Isabella", u"Hanna", u"Emilia", u"Melina", u"Maja", u"Larissa", u"Anja", u"Angelika", u"Patricia", u"Claudia", u"Mia", u"Birgit", u"Astrid", u"Bettina", u"Antonia", u"Jessica", u"Klara", u"Nina", u"Elisabeth", u"Janine", u"Manuela", u"Charlotte", u"Olivia", u"Christina", u"Leonie", u"Katharina", u"Amina", u"Anastasia", u"Bernadette", u"Mila", u"Pia", u"Magdalena", u"Romana", u"Paula", u"Amelie", u"Kerstin", u"Ela", u"Jana", u"Jennifer", u"Lea", u"Susanne", u"Sara", u"Nadine", u"Lara", u"Jasmin", u"Mira", u"Ella", u"Yvonne", u"Marie", u"Theresa", u"Melanie", u"Alma", u"Tanja", u"Alina", u"Martina", u"Denise", u"Rebecca", u"Paulina", u"Franziska", u"Karin", u"Lena", u"Ines", u"Nicole", u"Michelle", u"Viktoria", u"Chiara", u"Bianca", u"Stefanie", u"Carina", u"Linda", u"Azra", u"Stella", u"Nora", u"Flora", u"Vanessa", u"Teresa", u"Sonja", u"Tamara", u"Anna", u"Ana", u"Andrea", u"Melissa", u"Lilly", u"Elif", u"Lisa", u"Clara", u"Teodora", u"Kristina", u"Anita", u"Leonora", u"Silke", u"Emma", u"Esila", u"Daniela", u"Veronika", u"Elena", u"Marina", u"Helena", u"Natascha", u"Elina", u"Carmen", u"Alexandra", u"Eva", u"Barbara", u"Maya", u"Tina", u"Valentina", u"Elisa", u"Sabine", u"Matilda", u"Doris", u"Julia", u"Rosa", u"Laura", u"Annika", u"Nisa", u"Iris", u"Zoe", u"Monika", u"Selina"]

surnms = [u"Bauer", u"Müllner", u"Langer", u"Petrovic", u"Huber", u"Mayer", u"Lehner", u"Brunner", u"Gruber", u"Pfeiffer", u"Nowak", u"Steiner", u"Tichy", u"Weiß", u"Swoboda", u"Traxler", u"Schmid", u"Urban", u"Holzer", u"Kainz", u"Stadler", u"Auer", u"Wieser", u"Hahn", u"Moser", u"Varga", u"Schuster", u"Leitner", u"Eder", u"Ziegler", u"Wimmer", u"Winkler", u"Schindler", u"Graf", u"Nikolic", u"Reiter", u"Hofer", u"Berger", u"Koch", u"Yilmaz", u"Schwarz", u"Bayer", u"Baumgartner", u"Schmidt", u"Haider", u"Kaufmann", u"Horvath", u"Djordjevic", u"Lechner", u"Maier", u"Todorovic", u"Weiss", u"Lang", u"Bruckner", u"Neumann", u"Wolf", u"Schober", u"Fuchs", u"König", u"Hofbauer", u"Pichler", u"Neubauer", u"Fischer", u"Toth", u"Strobl", u"Wagner", u"Schneider", u"Kraus", u"Vasic", u"Kern", u"Winter", u"Klein", u"Schubert", u"Weber", u"Frank", u"Braun", u"Werner", u"Kaiser", u"Haas", u"Zimmermann", u"Jovanovic", u"Koller", u"Novak", u"Hofmann", u"Richter", u"Binder", u"Seidl", u"Wittmann", u"Böhm", u"Walter", u"Unger", u"Aigner", u"Markovic", u"Wiesinger", u"Windisch", u"Wallner", u"Zach", u"Müller", u"Hoffmann", u"Riedl"]

###########################################################################
# self/other-reference items

targetref_words = ('VERTRAUT', 'MEIN', 'RELEVANT')
nontargref_words = ('UNVERTRAUT', 'FREMD', 'UNBEKANNT', 'ANDERE', 'SONSTIGES', 'IRRELEVANT')

key_pair = { 'always' : { 'nontarg': 'e', 'target' : 'i', 'descr' : 'E (linker Zeigefinger) und I (rechter Zeigefinger)' }}
key_assignment = choice(['rechten', 'linken'])
if key_assignment == 'rechten':
    other_key = 'linken'
else:
    other_key = 'rechten'

instruction_pair = { 'speed' : 'Versuchen Sie, so SCHNELL wie möglich zu antworten und so wenig Zeit wie möglich bis zu der Reaktion auf die gezeigten Wörter verstreichen zu lassen. Achten Sie also auf Geschwindigkeit und drücken Sie die Antworttaste so schnell wie es Ihnen möglich ist.', 'accuracy' : 'Versuchen Sie, so GENAU wie möglich zu antworten und bei der Reaktion auf die gezeigten Wörter so wenig Fehler wie möglich zu machen. Achten Sie also auf Genauigkeit und darauf, dass Sie immer die korrekte Antworttaste drücken.', 'control' : ' '}

instruction_reminder = { 'speed' : 'Achten Sie weiterhin auf Geschwindigkeit und antworten Sie so schnell wie es Ihnen möglich ist.', 'accuracy' : 'Achten Sie weiterhin auf Genauigkeit und drücken Sie stets die korrekte Antworttaste.', 'control' : ' '}


if testing:
    escape_key = 'escape'
    instr_wait = 0.1
else:
    escape_key = 'notallowed'
    instr_wait = 0.5


# EXECUTE all main functions here
def execute():
    start_input() # prompt to input stuff
    # now initiate stuff
    basic_variables() # basic variables assigned, calculated
    set_screen() # creates psychopy screen and stim objects
    # window opens
    item_selection() # select items
    create_file() # created output file
    create_item_base() # base of items to be presented
    set_block_info() # sets block text and related infos based on conditions
    win.mouseVisible = False # hide mouse

    next_block() # begin task & run until finished

    print("************** END OF EXPERIMENT **************")

    ending() # saves demographic & final infos, gives feedback

    waitKeys(keyList = ['b']) # press B to end the exp (prevents subject from closing window)
    quit()

def ending():
    full_duration = round( ( datetime.now() - start_date ).total_seconds()/60, 2)
    info = 'Danke für die Teilnahme. Wenn Sie möchten, können Sie gehen, aber bitte seien Sie leise dabei.\n\nKurze Information über den Test:\n\nIn dieser Studie versuchen wir, Ihre wirklichen selbstbezogenen Details (z.B. Ihren tatsächlichen Nachnamen) von solchen zu unterscheiden, die Ihnen nicht zugehörig sind (z.B. andere Nachnamen). Ziel dieses Tests ist es, anhand von Reaktionszeiten herauszufinden, wenn eine Person versucht, bestimmte Daten zu verschleiern bzw. zu verheimlichen. Dies geschieht auf Basis der Vermutung, dass Reaktionszeiten für die Ihnen präsentierten selbstbezogenen Details langsamer ausfallen, als im Falle anderer Namen oder Daten. Hauptanliegen dieser Studie ist es, zu zeigen, ob dies besser mit der Aufforderung zu einer möglichst schnellen Reaktion oder zu einer möglichst genauen Reaktion funktioniert.\n\nFür weitere Informationen wenden Sie sich bitte an den Versuchsleiter (oder schreiben Sie eine E-mail an Gaspar Lukacs).'

    data_out.write(dems + "/" +
      "/".join( [ str(nmbr) for nmbr in
      [practice_repeated['block1'],
      practice_repeated['block2'],
      practice_repeated['block3'],
      full_duration] ] ) +
      "\n")
    data_out.close()
    show_instruction( info )

def set_screen(): # screen properties
    global win, start_text, left_label, right_label, center_disp, instruction_page
    win = Window([1280, 1000], color='Black', fullscr = 1, units = 'pix', allowGUI = True) # 1280 1024
    start_text = TextStim(win, color=instruction_color, font='Verdana', text = u'Um anzufangen, bitte die Leertaste drücken.', pos = [0,-300], height=35, bold = True, wrapWidth= 1100)
    if key_assignment == 'rechten':
        left_label = TextStim(win, color='white', font='Verdana', text = 'unvertraut', pos = [-350,-160], height=35, alignHoriz='center')
        right_label = TextStim(win, color='white', font='Verdana', text = 'vertraut', pos = [350,-160], height=35, alignHoriz='center')
    else:
        left_label = TextStim(win, color='white', font='Verdana', text = 'vertraut', pos = [-350,-160], height=35, alignHoriz='center')
        right_label = TextStim(win, color='white', font='Verdana', text = 'unvertraut', pos = [350,-160], height=35, alignHoriz='center')
    center_disp = TextStim(win, color='white', font='Arial', text = '', height = 60)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, font='Verdana', color = instruction_color)


def task_instructions( whichtext = ''):
    global main_item_info
    keys_info = 'Während des Tests sehen Sie Wörter in der Mitte des Bildschirms auftauchen. Sie müssen jedes Wort entweder mit der linken oder mit der rechten Antworttaste kategorisieren. Diese Tasten sind ' + key_pair['always']['descr'] + '. '
    inducer_info = 'Kategorisieren Sie Ausdrücke, die sich auf Vertrautheit beziehen, mit der ' + key_assignment + ' Taste. Diese Ausdrücke sind: ' + ', '.join(targetref_words).upper() + ' \nAuf der anderen Seite, kategorisieren Sie Ausdrücke, die sich auf Unvertrautheit beziehen, mit der ' + other_key + ' Taste. Diese Ausdrücke sind: ' + ', '.join(nontargref_words).upper()
    main_item_info = ' Kategorisieren Sie die folgenden Items als vertraut mit der ' + key_assignment + ' Taste: ' + ', '.join(the_targets).upper() + "\nKategorisieren Sie alle anderen Items als unvertraut mit der " + other_key + " Taste. (Diese andere Items sind: " + ', '.join(the_main_items).upper() + ". Zur Erinnerung: Sie leugnen, irgendwelche der anderen Items als relevant für Sie wahrzunehmen, also drücken Sie für alle diese die linke Taste.)"
    if whichtext == 'firstblock':
        return keys_info + '\n\nEs werden drei kurze Übungsrunden stattfinden. In der ersten Runde müssen Sie Ausdrücke kategorisieren, die mit Vertrautheit zu tun haben. '  + inducer_info
    elif block_num > 1:
        return  keys_info + inducer_info + '\n\nDie restlichen Items sind Nachnamen und Daten.' + main_item_info + '\n\nHinweis: achten Sie nur auf die Begriffe die mit der' + key_assignment + ' Taste kategorisiert werden müssen (' + ', '.join(the_targets + list(targetref_words)).upper() + ') und kategorisieren Sie alles andere mit der ' + other_key + ' Taste.'
    else:
        return  keys_info + inducer_info

def set_block_info():
    global block_info, block_num, incorrect, tooslow, move_on
    move_on = '\n\nUm weiterzugehen, drücken Sie die Leertaste.\n\nFalls nötig, drücken Sie die Taste ENTER (oder eine der Pfeiltasten) um die vollständigen Anweisungen erneut zu lesen.'
    block_info = [""]
    target_reminder = [
        "Zur Erinnerung: das als vertraut zu kategorisierende Item ist " +
        blcks_base[0][1]['word'].upper() +
        ". ",
        "Zur Erinnerung: das als vertraut zu kategorisierende Item ist " +
        blcks_base[1][1]['word'].upper() +
        ". "
      ]

    block_info.append( task_instructions('firstblock') + '\n\nUm weiterzugehen, drücken Sie die Leertaste.')

    block_info.append('Es folgt die zweite Übungsrunde. Es werden im Folgenden weitere Items hinzukommen:' + main_item_info + '\n\nUm sicherzustellen, dass Sie Ihre jeweiligen Antworten richtig kategorisieren, werden Sie für diese Aufgabe genügend Zeit haben. Sie müssen auf jedes Item korrekt antworten. Wählen Sie eine nicht korrekte Antwort (oder geben keine Antwort für mehr als 10 Sekunden ein), müssen Sie diese Übungsrunde wiederholen. \n\nZunächst wird die Kategorie ' + blcks_base[0][0]['categ'] +  " getestet, daher werden Ihnen auch in dieser Übungsrunde nur die damit verbundenen Items präsentiert. " + target_reminder[0] + move_on)

    block_info.append('Sie haben die zweite Übungsrunde geschafft. Nun folgt die dritte und letzte Übungsrunde. In dieser dritten Übungsrunde wird die Antwortzeit verkürzt sein. Eine bestimmte Anzahl an falschen Antworten ist aber erlaubt. Die Wörter (Angaben) "unvertraut", "vertraut" werden nicht mehr angezeigt, die Aufgabe bleibt jedoch dieselbe. Es werden nun sowohl die Ausdrück aus der ersten Übungsrunde als auch die Kategorie ' + blcks_base[0][0]['categ']+ ' aus der zweiten Übungsrunde gezeigt.\n\n ' + move_on)

    block_info.append("Gut gemacht. Nun beginnt der eigentliche Test. " + instruction_pair[crrnt_instr] + " Die Aufgabe bleibt dieselbe. Es wird zwei Blöcke, getrennt durch eine Pause, geben. Im ersten Block wird die Kategorie " +
      blcks_base[0][0]['categ'] +  " getestet, also werden Ihnen nur die damit verbundenen Items präsentiert. " +
      target_reminder[0] + "\n" + move_on)

    block_info.append(
      "Der erste Block ist nun beendet. Im zweiten Block wird die Kategorie " +
      blcks_base[1][0]['categ'] +
      " getestet. " +
      target_reminder[1] +
      "Abgesehen davon bleibt die Aufgabe dieselbe.\n" + instruction_reminder[crrnt_instr] + "\n" + move_on)



def start_input():
    global subj_id, dems, condition, gender, categories, true_probes, true_forename, true_surname, true_birthday
    input_box = Dlg(title=u'Grunddaten', labelButtonOK=u'OK', labelButtonCancel=u'Abbrechen')
    input_box.addText(text=u'')
    input_box.addField(label=u'c.', tip = '1-12')
    input_box.addField(label=u'VP', tip = 'Ziffern')
    input_box.addText(text=u'')
    input_box.addText(text=u'Bitte ausfüllen:')
    input_box.addField(label=u'Geschlecht', initial = '', choices=[u'männlich',u'weiblich', u'divers'] )
    input_box.addField(label=u'Geburtstag', initial ='Monat', choices=[u'JAN', u'FEB', u'MÄR', u'APR', u'MAI', u'JUN', u'JUL', u'AUG', u'SEP', u'OKT', u'NOV', u'DEZ'])
    input_box.addField(label = '', initial = '', choices=["%.2d" % i for i in range(1,32)])
    input_box.addField(label=u'Alter', tip = 'Ziffern')
    input_box.addField(label=u'Händigkeit', initial = '', choices=[u'rechtshändig',u'linkshändig'], tip = '(bevorzugte Hand zum Schreiben)' )
    input_box.addText(text=u'')
    input_box.addText(text=u'Ihr Name:')
    input_box.addText(text=u'(Jeweils nur einen Namen, kein Doppelname!)')
    input_box.addField(label=u'Vorname')
    input_box.addField(label=u'Nachname')
    input_box.addText(text=u'')
    input_box.show()
    if input_box.OK:
        stop = False
        try:
            condition = int(input_box.data[0])
        except ValueError:
            condition = 99
            print("Condition must be a number!")
        ## CONDITIONS:
        # 1: speed, forename1st
        # 2: speed, surname1st
        # 3: accuracy, forename1st
        # 4: accuracy, surname1st
        # 5: control, forename1st
        # 6: control, surname1st
        if condition not in range(1,7): # range(1,13):
            if testing:
                condition = 1 # set value for testing to skip Dlg input box
                print("condition was not set, now set to " + str(condition) + " for testing.")
            else:
                print("condition was not set correctly (should be 1/2/3/4/5/6)")
                stop = True
        try:
            subj_num = int(input_box.data[1])
        except ValueError:
            if testing:
                subj_num = 99 # set value for testing to skip Dlg input box
                print("subj_num was not set, now set to " + str(subj_num) + " for testing.")
            else:
                print("vp (subject number) was not set correctly (should be simple number)")
                stop = True
        try:
            age = int(input_box.data[5])
        except ValueError:
            if testing:
                age = 11 # set value for testing to skip Dlg input box
                print("age was not set, now set to " + str(age) + " for testing.")
            else:
                print("age was not set correctly (should be simple number)")
                stop = True
        true_forename = input_box.data[7]
        true_surname = input_box.data[8]
        if len(true_forename) < 2:
            print('forename less than 2 chars')
            if testing:
                true_forename = 'Till'
            else:
                stop = True
        elif not true_forename.isalpha():
            print('forename is not alphabetic only')
            stop = True

        if len(true_surname) < 2:
            print('surname less than 2 chars')
            if testing:
                true_surname = 'Lubczyk'
            else:
                stop = True
        elif not true_surname.isalpha():
            print('surname is not alphabetic only')
            stop = True
        if stop:
            print("\nTry again with correct inputs.\n")
            quit()
        subj_id = str(subj_num).zfill(2) + "_" + str(strftime("%Y%m%d%H%M%S", gmtime()))
        if input_box.data[2] == 'weiblich':
            gender = 2
        elif input_box.data[2] == 'männlich':
            gender = 1
        else:
            gender = 3
        true_birthdaymonth = input_box.data[3]
        true_birthdayday = input_box.data[4]
        true_birthday = ' '.join([true_birthdaymonth, str(true_birthdayday)])
        dems = 'dems/gender/age/hand/reps1/rep2/rep3/drtn' + '\t' + str(gender) + '/' + str(age)  + '/' + input_box.data[6]

        categories = ['Datum', 'Nachname']
        true_probes = {categories[0]: true_birthday.lower(),  categories[1]: true_surname.lower() }
        confirm_dlg()
    else:
        quit()

def confirm_dlg():
    global start_date
    confirm_input = Dlg(title=u'Confirmation', labelButtonOK=u'JA', labelButtonCancel=u'Nein')
    input_feed = u'Bitte bestätigen Sie, dass Ihr Vor- und Nachname richtig geschrieben wird und Ihr Geburtstag korrekt ist:\n\n ' + true_forename.upper() + ' ' + true_surname.upper() + '\n\n' + true_birthday.upper()
    confirm_input.addText(text='')
    confirm_input.addText(text=input_feed)
    confirm_input.addText(text='')
    confirm_input.show()
    if confirm_input.OK:
        start_date = datetime.now()
    else:
        start_input()

noneword = 'Keine'
def prune():
    global items_to_filt
    birthdays = birthdays_items
    birthdays = [bd.lower() for bd in birthdays]
    birthdays.sort()
    surnames = [sn.lower() for sn in surnms]
    surnames.sort()
    item_base_temp = {}
    for cat_ind, categ in enumerate(categories):
        probe = true_probes[categ]
        container = [birthdays, surnames][cat_ind]
        final8 = [probe]
        maxdif = 0
        container = [ elm for elm in container if elm[0] != probe[0] ]
        while len(final8) < 8  and maxdif < 99:
            temps = [ elm for elm in container if abs(len(probe)-len(elm)) <= maxdif ]
            if len(temps) > 0:
                final8.append( choice(temps) )
                container = [ elm for elm in container if elm[0] != final8[-1][0] ]
            else:
                maxdif += 1
        item_base_temp[categ] = final8[1:] + [noneword]
    items_to_filt = item_base_temp

def item_selection():
    global w_selected
    prune()
    selection_instr = TextStim(win, text = 'Sehen Sie sich die untenstehende Liste an und wählen Sie in jeder Kategorie (Datum und Nachname) maximal zwei Elemente aus, die für Sie persönlich wichtig oder sinnvoll erscheinen oder die sich in irgendeiner Weise von den übrigen Elementen unterscheiden: zum Beispiel der Name oder der Geburtstag eines Freundes oder einer Ihnen bekannten Person. Wenn sich in einer bestimmten Kategorie keine solchen Elemente befinden, wählen Sie einfach "Keine" aus. Sie können wählen (oder die Wahl aufheben), indem Sie auf den Namen klicken.', color=instruction_color, pos=(0,230), wrapWidth=1150, height = 30)
    ok_button = TextStim(win, text = 'OK', bold = True, color=instruction_color, pos=(250,-290), height = 30)
    maus = Mouse()
    textstim_dicts = {}
    w_counts = {}
    w_selected = {}
    none_clicked = {}
    wdth = -300
    for categ in categories:
        textstim_dicts[categ] = {}
        hght = 50
        for i in range(len(items_to_filt[categ])):
            textstim_dicts[categ][i] = TextStim(win, text = items_to_filt[categ][i].capitalize(), height = 30, color='white', pos = (wdth, hght ))
            hght -= 40
        wdth += 200
        w_counts[categ] = 0
        w_selected[categ] = []
        none_clicked[categ] = False
    change = False
    while True:
        for categ in categories:
            for i in range(len(textstim_dicts[categ])):
                current_stim = textstim_dicts[categ][i]
                if maus.isPressedIn(current_stim, buttons=[0]):
                    if current_stim.text == noneword:
                        if current_stim.bold == True:
                            current_stim.bold = False
                            none_clicked[categ] = False
                            change = True
                        elif w_counts[categ] == 0:
                            current_stim.bold = True
                            none_clicked[categ] = True
                            change = True
                    elif none_clicked[categ] == False:
                        if current_stim.bold == True:
                            current_stim.bold = False
                            w_counts[categ] -= 1
                            w_selected[categ].remove(current_stim.text)
                            change = True
                        elif w_counts[categ] < 2:
                            current_stim.bold = True
                            w_counts[categ] += 1
                            w_selected[categ].append(current_stim.text)
                            change = True
                current_stim.draw()
        ok_button.draw()
        selection_instr.draw()
        win.flip()
        if maus.isPressedIn( ok_button, buttons = [0] ):
            do_break = True
            for categ in categories:
                if  none_clicked[categ] == False and w_counts[categ] == 0:
                    do_break = False
            if do_break:
                break
            else:
                instruction_page.setText('Bitte wählen Sie mindestens ein Element in jeder Kategorie!')
                instruction_page.draw()
                win.flip()
                wait(2)
        if change == True:
            change = False
            wait(0.3)
            clearEvents()
    for categ in categories:
        w_selected[categ] = [ ws.lower() for ws in w_selected[categ] ]

def trm(raw_inp):
    return [w for w in raw_inp.replace(',', ' ').split(' ') if w != ''][:2]

def create_item_base():
    global blcks_base, stims_base, targetrefs, nontargrefs, the_targets, the_main_items, task_probes
    stim_base_tmp = {}
    the_targets = []
    task_probes = []
    the_main_items = []
    for categ in categories:
        stim_base_tmp[categ] = []
        words_temp = []
        filtered_items = [ itm.upper() for itm in items_to_filt[categ] if itm not in w_selected[categ] + [noneword] ]
        shuffle(filtered_items)
        if guilt == True:
            words_temp = [true_probes[categ]] + filtered_items[:5]
        else:
            words_temp = filtered_items[:6]
        for idx, itm in enumerate(words_temp): ## create basic dictionaries for the 6 crucial items, with types and categories
            if idx == 0:
                itmtype = "probe"
                the_main_items.append(itm)
                task_probes.append(itm)
            elif idx == 1:
                itmtype = "target"
                the_targets.append(itm)
            else:
                itmtype = "irrelevant" + str(idx-1)
                the_main_items.append(itm)
            stim_base_tmp[categ].append({'word': itm, 'item_type': itmtype, 'categ': categ })
    stims_base = deepcopy(stim_base_tmp)
    the_main_items.sort()
    if blocks_order == 0:
        blcks_base_temp = [ stim_base_tmp[categories[0]], stim_base_tmp[categories[1]] ]
    else:
        blcks_base_temp = [ stim_base_tmp[categories[1]], stim_base_tmp[categories[0]] ]
    blcks_base = deepcopy(blcks_base_temp)

    targetrefs = []
    nontargrefs = []
    for ref_word in targetref_words:
        targetrefs.append({'word': ref_word, 'item_type': 'targetref', 'categ': 'inducer' })
    for ref_word in nontargref_words:
        nontargrefs.append({'word': ref_word, 'item_type': 'nontargref', 'categ': 'inducer' })

def main_items():
    global blcks_base, crrnt_phase
    print('main_items()')
    crrnt_phase = 'main'
    block_stim_base = blcks_base.pop(0)
    main_stims = add_inducers(block_stim_base)
    return [dct for sublist in main_stims for dct in sublist] # flatten

def rndmz_details(block_stim_base):
    item_order=[]
    prev_last = '' # prev order is the item order of the previous trial sequence
    for i in range(0,18):# each i represents a sequence of 6 trials
        item_order_temp = deepcopy(block_stim_base) # create a temporary item order, this represents the item order WITHIN one trial sequence
        shuffle(item_order_temp) # shuffle this
        while prev_last == item_order_temp[0]: # if the last one of the previous block is the first of this one
            shuffle(item_order_temp) # reshuffle
        item_order.append(deepcopy(item_order_temp)) # make this the item order for this trial sequence
        prev_last = item_order_temp[-1]
    return item_order

def add_inducers(block_stim_base):
    word_assignment = {}
    # First we want to assign which words get an inducer. We want each word to get an inducer in half (9) of the trials. In addition, we want half of the words in one trial sequence (3) to have an inducer. Thus we make 9 permumtations of yes/no.
    yesno_perm = list(set(permutations('yyynnn')))
    shuffle(yesno_perm)
    options = yesno_perm[:9]
    blck_rev = []     # create an empty list for the reversed block
    for opt in options: # then we loop through to create the reverse
        optz_new = list(range(6))
        for index, item in enumerate(opt):
            if (item == "n"):
                optz_new[index] = "y"
            else:
                optz_new[index] = "n"
        blck_rev.append(deepcopy(optz_new)) # everytime add the current reversed line to the reversed block
    blck1 = options[0:3] + blck_rev[0:3] # because we wanna split them up in 3 we create blcks of 6 which are each  time 3 lines and then the reverse of those 3 lines
    blck2 = options[3:6] + blck_rev[3:6]
    blck3 = options[6:9] + blck_rev[6:9]
    shuffle(blck1)
    shuffle(blck2)
    shuffle(blck3)
    #create final block
    blck_fin = blck1 + blck2 + blck3
    for indx, dct in enumerate(block_stim_base): #assign the yes/nos to the words
        word_assignment[ dct['word'] ] = [opt[indx] for opt in blck_fin] # combine them to create an inducer assignment for all 18 trial sequences and assign them to the dict
    #  We then need to decide which inducer is shown thus we make a list
    inducer_lists = inducer_randomized() # randomize 6 lists of inducer words
    inducer_per_main = {}
    for dct in block_stim_base:
            inducer_per_main[ dct['word'] ] = inducer_lists.pop()
    # now insert the inducers
    final_item_order = []
    for t_indx, trial_seq in enumerate(rndmz_details(block_stim_base)): # trial sequence represents the order in which the x amount of words are presented within one sequence (n=6) of trials
        final_temp = []
        for i_indx, item in enumerate(trial_seq): # item represents each individual word (or trial)
            if word_assignment[item["word"]][t_indx] == "y": # check if the word should get an inducer
                inducer_pick= inducer_per_main[item["word"]].pop(0) # pick the right inducer
            # then we should delete this element so inducer so we use pop
                final_temp.append(inducer_pick) # append the inducer to our item order
            final_temp.append(item) # append the item to our item order
        final_item_order.append(deepcopy(final_temp)) # create final item order list
    return final_item_order

def inducer_randomized(): # 6 possible inducer orders
    targetrefs_perm = list(permutations(targetrefs)) # 3 x 2 = 6 arrangements
    shuffle(targetrefs_perm)
    nontarg_temp = deepcopy(nontargrefs)
    shuffle(nontarg_temp)
    nontargrefs_perm1 = list(permutations(nontarg_temp[:3])) # 3 x 2 = 6
    nontargrefs_perm2 = list(permutations(nontarg_temp[3:])) # 3 x 2 = 6
    nontargrefs_perm = []
    for i in range(3): # 6/2 = 3
        nontargrefs_perm.append(nontargrefs_perm1.pop(0)+nontargrefs_perm2.pop(0))
        nontargrefs_perm.append(nontargrefs_perm2.pop(0)+nontargrefs_perm1.pop(0))
    shuffle(nontargrefs_perm)
    inducer_lists = []
    for trefs, ntrefs in zip(targetrefs_perm, nontargrefs_perm):
        trefs = list(trefs)
        ntrefs = list(ntrefs)
        lst_temp = ntrefs
        nums = list(range(len(trefs+ntrefs)))
        insert_locs = []
        for i in range(len(trefs)): # tref never repeats successively
            new_rand = choice(nums)
            insert_locs.append(new_rand)
            nums = [n for n in nums if abs(n-new_rand) > 1]
        for loc in sorted(insert_locs): # trefs to the 3 locs
            lst_temp.insert( loc, trefs.pop() )
        inducer_lists.append(deepcopy(lst_temp))
    return inducer_lists

def inducer_items():
    print('inducer_items()')
    blck_itms_temp = deepcopy(targetrefs + nontargrefs + targetrefs + nontargrefs) # inducers x2
    shuffle(blck_itms_temp) # shuffle it, why not
    safecount = 0 # just to not freeze the app if sth goes wrong
    stim_dicts_f = [] # in here the final list of dictionary items is collected, one by one
    while len(blck_itms_temp) > 0: # stop if all items from blck_itms_temp were use up
        dict_item = blck_itms_temp[0]
        safecount += 1
        if safecount > 911:
            print('break due to unfeasable safecount')
            break
        good_indexes = [] # will collect the indexes where the dict item may be inserted
        dummy_dict = [{ 'word': '-', 'item_type': '-' }] # dummy dict to the end
        for f_index, f_item in enumerate(stim_dicts_f + dummy_dict):
            if dict_item['word'] in diginto_dict(stim_dicts_f, f_index, 'word', 4):
                continue # if there is, continue without adding the index as good index
            good_indexes.append(f_index) # if did not continue above, do add as good index
        if len(good_indexes) == 0:
            print('no good_indexes - count', safecount)
            shuffle(blck_itms_temp) # reshuffle
        else: # if there are good places, choose one randomly, insert the new item, and remove it from blck_itms_temp
            stim_dicts_f.insert( choice(good_indexes) , blck_itms_temp.pop(0))
    return stim_dicts_f # return final list (for blck_items var assignment)


def practice_items():
    print('practice_items()')
    blck_itms_temp = []
    if blocks_order == 0:
        blck_itms_temp += deepcopy(stims_base[categories[0]])
    else:
        blck_itms_temp += deepcopy(stims_base[categories[1]])
    if block_num == 3:
        blck_itms_temp += deepcopy(targetrefs + nontargrefs) #get inducers
        if blocks_order == 0:
            blck_itms_temp += deepcopy(stims_base[categories[0]])
        else:
            blck_itms_temp += deepcopy(stims_base[categories[1]])
    shuffle(blck_itms_temp) # shuffle it, why not
    # below the pseudorandomization to avoid close repetition of similar items (same item type)
    safecount = 0 # just to not freeze the app if sth goes wrong
    stim_dicts_f = [] # in here the final list of dictionary items is collected, one by one
    while len(blck_itms_temp) > 0: # stop if all items from blck_itms_temp were use up (added to stim_dicts_f and removed with pop() )
        dict_item = blck_itms_temp[0] # assign first dictionary item as separate variable; for easier access below
        safecount += 1
        if safecount > 911:
            print('break due to unfeasable safecount')
            break
        good_indexes = [] # will collect the indexes where the dict item may be inserted
        dummy_dict = [{ 'word': '-', 'item_type': '-' }] # dummy dict to the end; if the item is to be inserted to the end, there is no following dict that could cause an unwanted repetition
        for f_index, f_item in enumerate(stim_dicts_f + dummy_dict): # check all potential indexes for insertion in the stim_dicts_f as it is so far (plus 1 place at the end)
            if dict_item['item_type'] in diginto_dict(stim_dicts_f, f_index, 'item_type', 1): # checks whether there is preceding or following identical item_type around the potential index (see diginto_dict function)
                continue # if there is, continue without adding the index as good index
            good_indexes.append(f_index) # if did not continue above, do add as good index
        if len(good_indexes) == 0: # if by chance no good indexes found, print notification and reshuffle the items
            print('no good_indexes - count', safecount) # this should normally happen max couple of times
            blck_itms_temp.insert( len(blck_itms_temp), blck_itms_temp.pop(0) ) # move first element to last, and let's hope next first item is luckier and has place
        else: # if there are good places, choose one randomly, insert the new item, and remove it from blck_itms_temp
            stim_dicts_f.insert( choice(good_indexes) , blck_itms_temp.pop(0))
    return stim_dicts_f # return final list (for blck_items var assignment)



def diginto_dict(dct, indx, key_name, min_dstnc):
    if indx - min_dstnc < 0: # if starting index is negative, it counts from the end of the list; thats no good
        strt = 0 # so if negative, we just set it to 0
    else:
        strt = indx - min_dstnc # if not negative, it can remain the same
    return [ d[key_name] for d in dct[ strt : indx+min_dstnc ] ] # return all values for the specified dict key within the specified distance (from the specified dictionary)



def basic_variables():
    global stopwatch, blocks_order, instr_order, guilt, block_num, all_main_rts, kb_device, crrnt_instr, practice_repeated, firsttime
    stopwatch = Clock()
    guilt = 1 # always guilty
    #if condition in [5,6,7,8,10,12]:
    #    guilt = 1
    #else:
    #    guilt = 0
    if condition <= 2 :
        instr_order = 'speed'
        crrnt_instr = 'speed'
    elif condition > 2 and condition <= 4:
        instr_order = 'accuracy'
        crrnt_instr = 'accuracy'
    elif condition > 4:
        instr_order = 'control'
        crrnt_instr = 'control'
    if condition in [1,3,5]:
        blocks_order = 0 # forename1st
    else:
        blocks_order = 1 # surname1st
     ## CONDITIONS:
        # 1: speed, forename1st
        # 2: speed, surname1st
        # 3: accuracy, forename1st
        # 4: accuracy, surname1st
        # 5: control, forename1st
        # 6: control, surname1st
    block_num = 0
    all_main_rts = { 'probe' : [], 'irrelevant': [] }
    practice_repeated = { 'block1' : 0, 'block2': 0, 'block3': 0}
    firsttime = True
    io = launchHubServer()
    kb_device = io.devices.keyboard

# create output file, begin writing, reset parameters
def create_file():
    global data_out
    f_name = 'speed_acc_cit' + str(condition) + "_" + subj_id + '.txt'
    data_out=open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "condition", "phase", "block_number", "trial_number", "stimulus_shown", "category", "stim_type", "response_key", "rt_start", "incorrect", "too_slow", "press_duration", "isi", "date_in_ms" ] ) + "\n" )
    print("File created:", f_name)

def str_if_num( num_val ):
    if isinstance(num_val, str) or isinstance(num_val, unicode):
        return num_val
    else:
        return str( num_val*1000 )

def add_resp():
    global incorrect, tooslow
    data_out.write( '\t'.join( [ subj_id, str(condition), crrnt_phase, str(block_num), str(trial_num+1), stim_text, stim_current["categ"], stim_type, resp_key, str_if_num(rt_start), str(incorrect), str(tooslow), str_if_num(press_dur), str_if_num( isi_min_max[0]/1000 + isi_delay ), str(strftime("%Y%m%d%H%M%S", gmtime())) ] ) + '\n' )
    print("resp key:", resp_key, "for stim:", stim_text, "incorrect:", incorrect, "rt_start:", rt_start)

def start_with_space():
    start_text.draw() # start with space
    center_disp.setText("+")
    center_disp.draw()
    draw_labels()
    win.flip()
    inst_resp = waitKeys(keyList = ['space',escape_key])
    end_on_esc(inst_resp[0])
    draw_labels()
    win.flip()
    wait(isi_min_max[0]/1000)

def draw_labels():
    if block_num <= 2:
        left_label.draw()
        right_label.draw()

def assign_keys():
    global targetkey, nontargetkey
    if key_assignment == 'rechten':
        targetkey = key_pair['always']['target']
        nontargetkey = key_pair['always']['nontarg']
    else:
        targetkey = key_pair['always']['nontarg']
        nontargetkey = key_pair['always']['target']

def next_block():
    global ddline, block_num, rt_data_dict, crrnt_instr, blck_itms, firsttime, crrnt_phase
    if len(blcks_base) > 0:
        crrnt_phase = 'practice'
        if block_num == 0:
            rt_data_dict = {}
            assign_keys()
        if block_num in [0,4,5] or practice_eval():
            block_num+=1
        if block_num == 1:
            blck_itms = inducer_items()
            ddline = main_ddline
        elif block_num == 2:
            if firsttime:
                firsttime = False
            blck_itms = practice_items()
            ddline = 10
        elif block_num == 3:
            blck_itms = practice_items()
            ddline = main_ddline
        else:
            blck_itms = main_items()
        if testing == True:
            blck_itms = blck_itms[0:5]
        run_block()


def practice_eval():
    global rt_data_dict
    is_valid = True
    if first_wrong == True:
        is_valid = False
    elif block_num != 2:
        types_failed = []
        if block_num == 1:
            min_ratio = 0.8
        else:
            min_ratio = 0.6
        for it_type in rt_data_dict:
            it_type_feed_dict = { 'targetref': "sich auf Vertrautheit beziehende Ausdrücke",
        'nontargref': "sich auf Unvertrautheit beziehende Ausdrücke",
        'main_item': "als unvertraut zu kategorisierende Namen",
        'target': "als vertraut zu kategorisierende Namen" }
            rts_correct = [ rt_item for rt_item in rt_data_dict[it_type] if rt_item > 0.15 ]
            corr_ratio = len( rts_correct )/ len( rt_data_dict[it_type] )
            if corr_ratio < min_ratio:
              is_valid = False
              types_failed.append(
                " " +
                it_type_feed_dict[it_type] +
                " (" + str( int( corr_ratio // 0.01 ) ) +
                "% korrekt)"
              )
            if is_valid == False:
                block_info[block_num] = "Sie müssen diese Übungsrunde wiederholen, da Sie zu wenige richtige Antworten gegeben haben.\n\nSie benötigen mindestens " + str( int(min_ratio*100) ) + "% richtige Antworten für jeden der Antworttypen, jedoch haben Sie nicht genügend richtige Antworten für folgende(n) Antworttyp(en) gegeben:" + ", ".join(types_failed) +  ".\n\nMachen Sie sich keine Sorgen, wenn Sie diese Übungsrunde mehrmals wiederholen müssen." + move_on
    if is_valid == False:
        practice_repeated['block' + str(block_num)] += 1
    rt_data_dict = {}
    return is_valid

def show_instruction(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    inst_resp = waitKeys(keyList = ['space', escape_key])
    end_on_esc(inst_resp[0])

def show_block_instr():
    instruction_page.setText( block_info[block_num] )
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    show_again = ['left', 'up', 'right', 'down','return']
    inst_resp = waitKeys( keyList = [ 'space', escape_key ] + show_again )
    end_on_esc( inst_resp[0] )
    if inst_resp[0] in show_again:
        show_instruction( task_instructions() + '\n\nUm weiterzugehen, drücken Sie die Leertaste.' )
        show_block_instr()

def run_block():
    global block_num, trial_num, stim_current, stim_text, stim_type, incorrect, tooslow, first_wrong, show_feed, ddline, isi_delay, resp_key, rt_start, press_dur
    show_block_instr()
    first_wrong = False
    print("len(blck_itms):", len(blck_itms))
    start_with_space()
    for trial_num in range(len(blck_itms)): # go through all stimuli of current block
        print("------- Trial number:", trial_num, "In block:", block_num, "C:", condition, "ord:", blocks_order)
        stim_current = blck_itms[trial_num]
        incorrect = 0
        tooslow = 0
        stim_type = stim_current["item_type"]
        stim_text = stim_current["word"]
        isi_delay = randint(1, isi_min_max[1]-isi_min_max[0]) / 1000
        wait(isi_delay) # wait ISI
        center_disp.setText(stim_text.upper())
        draw_labels()
        center_disp.draw()
        win.callOnFlip(stopwatch.reset)
        kb_device.clearEvents()
        clearEvents()
        win.flip()
        response = waitKeys(maxWait = ddline, keyList=[targetkey, nontargetkey, escape_key], timeStamped=stopwatch)
        if not response:
            rt_start = stopwatch.getTime()
            resp_key = '-'
            tooslow += 1
            show_tooslow()
        else:
            resp_key = response[0][0]
            rt_start = response[0][1]
            end_on_esc(resp_key)
            if resp_key == targetkey:
                if stim_type in ("target", "targetref"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
                    show_false()
            elif resp_key == nontargetkey:
                if stim_type[:10] in ("probe","irrelevant", "nontargref"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
                    show_false()
        draw_labels()
        win.flip()
        wait(isi_min_max[0]/1000)
        press_dur = '-' # remains this if none found, or not with correct key
        for ke in kb_device.getReleases(): # get io keypress events for duration
            try:
                if ke.key == resp_key: # if matches the pygame key, should be fine
                    press_dur = ke.duration # store io keypress duration
            except Exception:
                pass
            break
        add_resp() # store trial data
        if block_num == 2: # check if comprehension check has to be repeated
            if (incorrect+tooslow) > 0:
                first_wrong = True
                break
        if block_num > 5:
            break
        else:
            collect_rts()
    next_block()

def collect_rts(): # for practice evaluation & dcit calculation
    global rt_data_dict, all_main_rts, rt_start
    if (incorrect+tooslow) > 0:
        rt_start = -9
    if crrnt_phase == 'practice':
        if stim_type[:10] in ("probe","irrelevant"):
            group_type = 'main_item'
        else:
            group_type = stim_type
        if group_type not in rt_data_dict:
            rt_data_dict[group_type] = []
        rt_data_dict[group_type].append(rt_start)
    if crrnt_phase == 'main' and stim_type[:10] in ("probe","irrelevant") and incorrect != 1 and tooslow != 1 and rt_start > 0.15 and rt_start < main_ddline:
        all_main_rts[ stim_type[:10] ].append(rt_start)

def show_false():
    center_disp.text = 'Falsch!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(0.5)
    center_disp.color = 'white'
def show_tooslow():
    center_disp.text = 'Zu langsam!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(0.5)
    center_disp.color = 'white'


# end session
def end_on_esc(escap):
    if escap == escape_key : # escape
        print("Trying to escape?")
        instruction_page.setText('Sure you want to discontinue and quit the experiment?\n\nPress "y" to quit, or press "n" to continue.')
        instruction_page.draw()
        win.flip()
        wait(1)
        quit_resp = waitKeys(keyList = ['y', 'n'])
        if quit_resp[0] == 'y':
            print("************ ESCAPED ************")
            data_out.close()
            win.close()
            quit()
        else:
            clearEvents()
            print("Continuing...")



# EXECUTE
execute()
