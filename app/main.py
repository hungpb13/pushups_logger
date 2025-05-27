from .models import Workout, User
from . import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route("/new_workout")
@login_required
def new_workout():
    return render_template("new_workout.html")


@main.route("/new_workout", methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')

    workout = Workout(pushups=pushups, comment=comment, author=current_user)

    db.session.add(workout)
    db.session.commit()

    flash("Your workout has been added!", "primary")

    return redirect(url_for('main.all_workouts'))


@main.route("/all_workouts")
@login_required
def all_workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = user.workouts

    return render_template("all_workouts.html", workouts=workouts, user=user)


@main.route("/workout/<int:workout_id>/update", methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    if request.method == 'POST':
        workout.pushups = request.form.get('pushups')
        workout.comment = request.form.get('comment')

        db.session.commit()

        flash("Your workout has been updated!", "success")

        return redirect(url_for('main.all_workouts'))

    return render_template('update_workout.html', workout=workout)


@main.route("/workout/<int:workout_id>/delete", methods=['GET'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    db.session.delete(workout)
    db.session.commit()

    flash("Your workout has been deleted!", "danger")

    return redirect(url_for('main.all_workouts'))