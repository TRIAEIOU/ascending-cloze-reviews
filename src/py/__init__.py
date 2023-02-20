import sys, time, datetime
from aqt import mw, gui_hooks
from aqt.qt import QAction
from anki.scheduler import QueuedCard
from anki.scheduler.v3 import QueuedCards
from anki.cards import Card, BackendCard
from aqt.browser.sidebar import SidebarItemType
from anki.notes import Note
from anki.consts import MODEL_CLOZE, QUEUE_TYPE_REV, QUEUE_TYPE_DAY_LEARN_RELEARN, QUEUE_TYPE_PREVIEW
from .version import *

CVER = get_version()
NVER = "1.0.0"

OCR_MENU = "Sort due clozes ascending"

def order(parent):
    # Create a root backup
    mw.col.create_backup(backup_folder=mw.pm.backupFolder(),
        force=True,
        wait_for_completion=True,
    )

    # Dict of nid's and their cloze cards
    notes = {}

    # The different card related types
    qcards: QueuedCards # https://github.com/ankitects/anki/blob/5551a37f036d99ddbe36702020d23633ae2d82d0/proto/anki/scheduler.proto#L101
    qcard: QueuedCard # https://github.com/ankitects/anki/blob/5551a37f036d99ddbe36702020d23633ae2d82d0/proto/anki/scheduler.proto#L107
    bcard: BackendCard # https://github.com/ankitects/anki/blob/5551a37f036d99ddbe36702020d23633ae2d82d0/proto/anki/cards.proto#L28

    TODAY = int(time.mktime(datetime.date.today().timetuple()))
    # Run only on selected col
    qcards = parent.col.sched.get_queued_cards(fetch_limit=9999999)
    # get_queued_cards returns Sequence(QueueCard → protobuf/BackendCard)
    for qcard in qcards.cards:
        bcard = qcard.card
        note = notes[bcard.note_id] if notes.get(bcard.note_id) else {
            'type': Note(mw.col, None, bcard.note_id).note_type(),
            'bcards': [],
            'min': sys.maxsize,
            'max': 0
        }
        # Assuming BackendCard mtime_secs is last review time
        # Only reschedule cloze notes that haven't been reviewed today
        if note['type']['type'] == MODEL_CLOZE and bcard.mtime_secs < TODAY:
            note['bcards'].append(bcard)
        notes[qcard.card.note_id] = note

    updated = []
    due = int(time.mktime(datetime.datetime.now().timetuple()))
    for nid, note in notes.items():
        bcard: BackendCard
        for bcard in sorted(note['bcards'], key=lambda c: c.template_idx, reverse=True):
            card = Card(mw.col, None, bcard)
            if card.queue in (QUEUE_TYPE_REV, QUEUE_TYPE_DAY_LEARN_RELEARN):
                card.queue = QUEUE_TYPE_PREVIEW
            card.due = due
            #print(f"update card {card.id}: queue: {card.queue}, type: {card.type}, due: {card.due}")
            updated.append(card)
            due -= 1

    mw.col.update_cards(updated) # takes Sequence(Anki/python Card)

def add_to_menu(title, parent, menu):
    action = QAction(title, menu)
    action.triggered.connect(lambda: order(parent))
    menu.addAction(action)
    return menu

action = QAction(OCR_MENU, mw)
action.triggered.connect(lambda: order(mw))
mw.form.menuTools.addAction(action)

gui_hooks.browser_sidebar_will_show_context_menu.append(lambda sb, menu, itm, i: add_to_menu(OCR_MENU, sb, menu) if itm.item_type == SidebarItemType.DECK else menu)

if strvercmp(CVER, NVER) < 0:
    set_version(NVER)