# Asceding cloze reviews

Anki addon to order reviews of cloze notes in ascending cloze ordinal order.

**\*\*\* NOTE: I have not double checked the long term effects of the scheduling of the cards but it seems to do what I want when using the v3 scheduler, I have not tested it with v1 and v2 schedulers! Use at your own peril (backups are made if you want to revert)!  \*\*\***

## Use case

When studying cloze notes that are sequential in nature reviewing in ascending cloze ordinal order is preferable.

### Subject notes with hidden inactive clozes

One note generation strategy is keeping one cloze note per "subject", rather than lots of small notes, using a cloze template that hides all inactive clozes (e.g. [Flexible cloze 2](https://ankiweb.net/shared/info/1889069832), [Cloze (Hide all)](https://ankiweb.net/shared/info/1709973686), [Enhanced Cloze (for Anki 2.1)](https://ankiweb.net/shared/info/1990296174), etc.). This allows using Anki as the primary "note keeping location" rather than having the actual notes somewhere else (in OneNote, markdown files etc.) and have to create Anki notes for quizzing as a separate step. It also greatly improves maintainability (at lecture: "hmm, I seem to remember it was X, not Y, now where is that Anki note so I can ammend it?"). During reviewing it adds the posibility to easily look up related info ("so if it wasn't ABX X for Y, for what was ABX X used?"). This while following the general **card** principles of making individual cards "atomic" and brief.

```text
# ACLS

## Terminology

Bla: {{c1::bla}}
Bla: {{c2::bla}}

## Drugs

Epi: {{c3::bla}}
Amiodarone: {{c4::bla}}

## Process

Unwitnessed arrest: {{c5::
1. Bla
2. Bla
}}

```

If cards `c2` and `c5` are due it makes sense to review `c2` before `c5` as the answer of `c2` may be used in `c5`,

### Nested clozes

Example: given the following note:

```text
Anemia types tree - main divisions and how to differentiate: {{c1::MCV
<80: Microcytic, mech & etiology: {{c2::insuff/defective Hb prod - IDA, lead poison, thalassemia, iron defic}}
80-100: Normocytic, mech & etiology: {{c3::RBC ↓prod or ↑loss - hemolysis, blood loss, aplastic anemia, chronic disease}}
>100: Macrocytic, mech & etiology: {{c4::defective DNA synth/repair - megaloblastic: B12 or folate defic (hypersegm NGc); non-megaloblastic: e.g. liver disease (non-hypersegm NGc))}}
}}
```

Similarly, if cards `c1` and `c3` are due it is preferable to review `c1` before `c3`, as `c3` will expose the answer of `c1`.

## Use

For best use, run before starting the day's reviewing.

1. Select the relevant deck in the main window or the browser
2. Select `Sort due clozes ascending` from main window tool bar or context menu in the browser tree menu.

## Addon logic

The addon changes the due dates in the data base, this means that when synced to `ankiweb` it can be reviewed in ascending order in any reviewer (desktop, AnkiDroid, AnkiMobile).

1. The addon creates a backup of the collection (i.e. all notes/cards and their scheduling) - you can restore to this backup through `Switch Profile → Open Backup` selecting the most recent one (should have a filename correspoding to the time the addon was run).
2. In the selected deck (and subdecks): get all **cloze cards** due for **review today** that has not yet been reviewed (i.e. new cards and cards which have at least one review today are not included).
3. For the selected cards: per note **due** cards have due time set in 1s intervals in cloze ordinal order (the highest ordinal will have due time "now", the lowest ordinal "now - Xs").

The effect of this is as follows (when refering to "cards" below this includes only the cards due today):

- The cards will be marked as "learning" in the GUI, red in the main window.
- Cards from the same note will be reviewed in asceding cloze ordinal order.
- When reviewing a deck with multiple cloze **notes**, cards will come from "all cloze notes" at once, i.e. not "first all cards of one note, then all from the next note".
- Once a card has been reviewed it will return to its normal status (e.g. "learned" or "learning") and will be scheduled for the next review as per normal (Anki built in scheduling or users modified scheduling).
