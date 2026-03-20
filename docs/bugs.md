- [ ] replacing date parses date but replaces the name
```bash
(.venv) ❯ python -m SincedPy log
C - 21/03/26
lmao - 23/03/26
A - 20/10/00
B - 20/10/00

(.venv) ❯ python -m SincedPy mod C 2027-03-27

(.venv) ❯ python -m SincedPy log
2027-03-27 00:00:00 - 21/03/26
lmao - 23/03/26
A - 20/10/00
B - 20/10/00
```


