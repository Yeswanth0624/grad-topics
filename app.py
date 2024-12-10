from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'


class Ranger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    power = db.Column(db.Integer, nullable=False)
    dummy_card = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Ranger {self.id} - {self.name}>'
    
# Routes for Todo
@app.route('/')
def landing_page():
    return render_template("mainpage.html")

@app.route('/assignment/about/')
def about():
    return render_template("/assignment/about.html")


@app.route('/assignment/homepage/')
def Home_page():
      # Fetch event data from the database



    return render_template('assignment/homepage.html')


@app.route('/assignment/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))  # Use url_for here
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('assignment/index.html', tasks=tasks)

@app.route('/assignment/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))  # Use url_for here
    except:
        return 'There was a problem deleting that task'

@app.route('/assignment/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('index'))  # Use url_for here
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('assignment/update.html', task=task)
@app.route('/assignment/manage-events/', methods=['GET', 'POST'])
def manage_events():
    if request.method == 'POST':
        # Handle adding a new ranger card
        card_name = request.form['card_name']
        color = request.form['color']
        power = request.form['power']
        dummy_card = request.form['dummy_card']

        new_card = Ranger(name=card_name, color=color, power=power, dummy_card=dummy_card)

        try:
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('manage_events'))
        except:
            return 'There was an issue adding your card'

    else:
        # Handle filtering and sorting
        filter_color = request.args.get('filter_color')
        sort_power = request.args.get('sort_power')

        query = Ranger.query

        if filter_color:
            query = query.filter_by(color=filter_color)

        if sort_power == 'asc':
            query = query.order_by(Ranger.power.asc())
        elif sort_power == 'desc':
            query = query.order_by(Ranger.power.desc())

        cards = query.all()
        return render_template('assignment/events.html', cards=cards)

@app.route('/assignment/update-event/<int:id>', methods=['GET', 'POST'])
def update_event(id):
    card = Ranger.query.get_or_404(id)

    if request.method == 'POST':
        card.name = request.form['card_name']
        card.color = request.form['color']
        card.power = request.form['power']
        card.dummy_card = request.form['dummy_card']

        try:
            db.session.commit()
            return redirect(url_for('manage_events'))
        except:
            return 'There was an issue updating the card'

    else:
        return render_template('assignment/update_event.html', card=card)

@app.route('/assignment/delete-event/<int:id>', methods=['GET'])
def delete_event(id):
    card_to_delete = Ranger.query.get_or_404(id)

    try:
        db.session.delete(card_to_delete)
        db.session.commit()
        return redirect(url_for('manage_events'))
    except:
        return 'There was a problem deleting that card'

if __name__ == "__main__":
    app.run(debug=True)
