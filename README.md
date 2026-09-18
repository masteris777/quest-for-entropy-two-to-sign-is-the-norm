# Two to Sign Is the Norm

**Article:** [Quest for Entropy #17 — "Two to Sign Is the Norm"](https://questforentropy.com/p/two-to-sign-is-the-norm) · also on [Substack](https://questforentropy.substack.com/p/two-to-sign-is-the-norm)

Companion code for the episode. The article ships with it as `article.md`; the
step-by-step walk through the mechanism, with every number, is
`explanation.md`; the table bench, the same machine with buttons, is
`bench/index.html` (open it in a browser, no server needed).

## Run it

Python 3.10+, with numpy, matplotlib and pillow.

    pip install numpy matplotlib pillow
    python run_all.py

The exams take seconds; the figures and the two animations take about a minute
and are written into `assets/`, replacing the shipped copies with identical ones.

## What is in here

| file | what it is |
|---|---|
| `table_logic.py` | the whole machine: the table, the turn, the meeting, the settlement, and its three exams |
| `article_worked.py` | one measurement with the numbers (`assets/tbl_worked.png`) |
| `article_tables.py` | the table sizes, the four cases of one tick, the ladder numbers |
| `article_signing.py` | the settlement tick by tick, with the toy's own unitdraws (`assets/tbl_signing.png`) |
| `article_who_signs.py` | one, two and three signers on a three-axis table (`assets/tbl_who_signs.png`) |
| `article_gifs.py` | the two animations in the article |
| `bench/index.html` | the table bench: every move, one button at a time, arithmetic written out |
| `run_all.py` | the exams, then every figure, in order |
| `expected_output/run_all.txt` | what a correct run prints, to diff against |

Nothing here rolls dice. Every unitdraw is a hash chain per thread, so the same
run prints the same numbers every time. The bench uses a small in-browser hash
instead of SHA-256, so its unitdraws differ from the Python's, and the counted
curves agree within counting noise.

## Scope

The table and its turns are standard quantum arithmetic written as a
spreadsheet, imported rather than derived. What this code demonstrates is the
last step only: the settlement, where two books sign in proportion to length
and a fact needs both signatures. The article's Confession section says exactly
where that line falls.

## Licence

MIT.
