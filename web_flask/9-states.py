#!/usr/bin/python3
"""Starts a Flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Display a HTML page with states or a specific state's cities."""
    states = storage.all(State)
    if id is not None:
        key = "State." + id
        state = states.get(key)
        return render_template('9-states.html', state=state)
    states = sorted(states.values(), key=lambda s: s.name)
    return render_template('9-states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
