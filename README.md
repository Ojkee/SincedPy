# SincedPy

CLI tool for simple task / record tracking with categories, deadlines and undo support.

The project is designed as a command-driven CLI application.


# Features

CLI task management
- categories
- deadlines
- recurring deadlines (-d/-w/-m/-y)
- statuses (ongoing/done/canceled)
- undo system
- local storage


# Commands

### ADD
```bash
add name                              # adds record 
add name @category                    # adds record that belongs to category
add name DD-MM-YYYY                   # adds record with deadline
add name DD-MM-YYYY -[d/w/m/y] number # adds recurring record, number is optional, eg. -w 8 => every 8 weeks, You can use @category
```

### LOG
```bash
log            # logs all
log name       # logs records with name
log -[d/w/m/y] # logs records in day/week/month/year
log @category  # logs records from category
log status     # logs records with status
```


### MODIFY
```bash
mod name new_name   # modifies name
mod name @category  # modifies category
mod name DD-MM-YYYY # modifies deadline
mod status          # modifies status
```

### REMOVE
```bash
REMOVE!       # removes all
rem name      # removes by name
rem @category # removes all from category
rem status    # removes all by status
```

### Undo
```bash
undo # undo last undoable command, cannot undo 'undo', stackable
```


# Installation

### Download 
```bash
git clone https://github.com/Ojkee/SincedPy.git
cd SincedPy
python -m venv .venv
```


### Activate Linux/MacOS
```bash
source .venv/bin/activate
```


### Activate Windows
```batch
.venv\Scripts\activate
```


### Install
```bash
pip install -e .
```


# License
MIT License.

