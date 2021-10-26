from app import app
from flask import Flask, render_template, request, redirect, session, flash
import geocoder

from forms import StateEditForm, StateRegistrationRuleForm, ElectionForm, AdminUserForm
from models import db, User, State, Election, RegistrationRule

import os

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod == None:
    from api_keys import MAPQUEST_API_KEY
if is_prod:
    LOB_API_KEY = os.environ.get('LOB_API_KEY')
    EASYPOST_API_KEY = os.environ.get('EASYPOST_API_KEY')
    GOOGLE_CIVIC_API_KEY = os.environ.get('GOOGLE_CIVIC_API_KEY')
    MAPQUEST_API_KEY = os.environ.get('MAPQUEST_API_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')

# Views for Admin Routes


@app.route('/admin')
def admin_index():
    """Index page for Administrator"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    return render_template('admin_index.html', user=curr_user)


@app.route('/admin/users')
def admin_show_user_list():
    """Shows user list to those with administrator access"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    users = User.query.order_by(User.last_name).all()
    return render_template('admin_users.html', users=users, user=curr_user)


@app.route('/admin/users/<username>/edit', methods=['GET', 'POST'])
def admin_edit_user(username):
    """Admin site to edit specific user"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    user = User.query.get_or_404(username)
    form = AdminUserForm()
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.street_address.data = user.street_address
        form.city.data = user.city
        form.state_id.data = user.state_id
        form.zip_code.data = user.zip_code
        form.is_admin.data = user.is_admin
        return render_template('admin_edit_user.html', user=user, form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.username = form.username.data
            user.street_address = form.street_address.data
            user.city = form.city.data
            user.state_id = form.state_id.data
            user.zip_code = form.zip_code.data
            user.is_admin = form.is_admin.data
            full_address = f'{user.street_address} {user.city} {user.state_id} {user.zip_code}'
            g = geocoder.mapquest(full_address, key=MAPQUEST_API_KEY)
            if g.geojson['features'][0]['properties'].get('county'):
                county = g.geojson['features'][0]['properties'].get('county')
                user.county = county
            flash(f'Changed information for {user.username}', 'success')
            return redirect('/admin/users')


@app.route('/admin/states')
def admin_show_states():
    """Show List of States In Admin Mode with Links to Each State"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    states = State.query.all()
    return render_template('admin_states.html', user=curr_user, states=states)


@app.route('/admin/states/<state_id>')
def admin_show_state_info(state_id):
    """Admin Page for State Information"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    state = State.query.get_or_404(state_id)
    return render_template('admin_state_info.html', state=state, user=curr_user)


@app.route('/admin/states/<state_id>/edit', methods=['GET', 'POST'])
def admin_edit_state_info(state_id):
    """Admin Page to Edit State Info"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    state = State.query.get_or_404(state_id)
    form = StateEditForm()
    if request.method == 'GET':
        form.registration_url.data = state.registration_url
        form.elections_url.data = state.elections_url
        form.registration_in_person_deadline.data = state.registration_in_person_deadline
        form.registration_mail_deadline.data = state.registration_mail_deadline
        form.registration_online_deadline.data = state.registration_online_deadline
        form.absentee_application_in_person_deadline.data = state.absentee_application_in_person_deadline
        form.absentee_application_mail_deadline.data = state.absentee_application_mail_deadline
        form.absentee_application_online_deadline.data = state.absentee_application_online_deadline
        form.voted_absentee_ballot_deadline.data = state.voted_absentee_ballot_deadline
        form.check_registration_url.data = state.check_registration_url
        form.polling_location_url.data = state.polling_location_url
        form.absentee_ballot_url.data = state.absentee_ballot_url
        form.local_election_url.data = state.local_election_url
        form.ballot_tracker_url.data = state.ballot_tracker_url
        return render_template('admin_state_edit.html', state=state, form=form, user=curr_user)
    if request.method == 'POST':
        if form.validate_on_submit():
            state.registration_url = form.registration_url.data
            state.elections_url = form.elections_url.data
            state.registration_in_person_deadline = form.registration_in_person_deadline.data
            state.registration_mail_deadline = form.registration_mail_deadline.data
            state.registration_online_deadline = form.registration_online_deadline.data
            state.absentee_application_in_person_deadline = form.absentee_application_in_person_deadline.data
            state.absentee_application_mail_deadline = form.absentee_application_mail_deadline.data
            state.absentee_application_online_deadline = form.absentee_application_online_deadline.data
            state.voted_absentee_ballot_deadline = form.voted_absentee_ballot_deadline.data
            state.check_registration_url = form.check_registration_url.data
            state.polling_location_url = form.polling_location_url.data
            state.absentee_ballot_url = form.absentee_ballot_url.data
            state.local_election_url = form.local_election_url.data
            state.ballot_tracker_url = form.ballot_tracker_url.data
            db.session.commit()
            flash(f'Changed Information for {state.name}', 'success')
            return redirect(f'/admin/{state.id}')


@app.route('/admin/state/<state_id>/rules/<int:rule_id>/delete', methods=['POST'])
def remove_rule_from_state(state_id, rule_id):
    """Removes Voter Registration Rule from a state"""
    state = State.query.get_or_404(state_id)
    rule = RegistrationRule.query.get_or_404(rule_id)
    state.registration_rules.remove(rule)
    db.session.commit()
    flash(f'Removed rule from {state.name}', 'success')
    return redirect(f'/admin/states/{state_id}')


@app.route('/admin/rules')
def admin_show_registration_rules():
    """Shows Admin Page for Voter Registration Rules"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    rules = RegistrationRule.query.all()
    return render_template('admin_rules.html', user=curr_user, rules=rules)


@app.route('/admin/rules/new', methods=['GET', 'POST'])
def admin_add_registration_rule():
    """Admin Feature - Add new Voter Registration Rule"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    states = State.query.all()
    form = StateRegistrationRuleForm()
    if request.method == 'POST':
        new_rule = RegistrationRule(rule=form.rule.data)
        db.session.add(new_rule)
        db.session.commit()
        state_list = list(request.form.listvalues())[2:]
        new_rule.states.clear()
        for item in state_list:
            new_rule.states.append(State.query.get(item[0]))
        db.session.commit()
        flash(f'Voter Registration Rule Added', 'success')
        return redirect('/admin/rules')
    if request.method == 'GET':
        return render_template('admin_new_rule.html', states=states, user=curr_user, form=form)


@app.route('/admin/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
def admin_edit_registration_rule(rule_id):
    """Admin Feature - Edit Voter Registration Rule"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    edit_rule = RegistrationRule.query.get_or_404(rule_id)
    form = StateRegistrationRuleForm()
    states = State.query.all()
    if request.method == 'GET':
        form.rule.data = edit_rule.rule
        return render_template('admin_edit_reg_rule.html', form=form, rule=edit_rule, user=curr_user, states=states)
    if request.method == 'POST':
        edit_rule.rule = form.rule.data
        state_list = list(request.form.listvalues())[2:]
        edit_rule.states.clear()
        for item in state_list:
            edit_rule.states.append(State.query.get(item[0]))
        db.session.commit()
        flash('Successfully changed rule', 'success')
        return redirect('/admin/rules')


@app.route('/admin/rules/<int:rule_id>/delete', methods=['POST'])
def admin_delete_registration_rule(rule_id):
    """Admin Feature - Delete Voter Registration Rule"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    deleted_rule = RegistrationRule.query.get_or_404(rule_id)
    db.session.delete(deleted_rule)
    db.session.commit()
    flash(f'Registration Rule deleted', 'success')
    return redirect('/admin/rules')


@app.route('/admin/elections')
def admin_show_elections():
    """Admin Feature - Show lists of all elections in each state"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    elections = Election.query.order_by(Election.state_id, Election.date).all()
    return render_template('admin_elections.html', user=curr_user, elections=elections)


@app.route('/admin/elections/new', methods=['GET', 'POST'])
def admin_new_election():
    """Admin Feature Adding New Election"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    form = ElectionForm()
    if form.validate_on_submit():
        name = form.name.data
        state_id = form.state_id.data
        date = form.date.data
        new_election = Election(name=name, date=date, state_id=state_id)
        db.session.add(new_election)
        db.session.commit()
        flash(
            f'Election added on {new_election.full_date} in {new_election.state.name}', 'success')
        return redirect('/admin/elections')
    return render_template('admin_new_election.html', user=curr_user, form=form)


@app.route('/admin/elections/<int:election_id>/edit', methods=['GET', 'POST'])
def admin_edit_election(election_id):
    """Admin Feature - Edit Election Information"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    form = ElectionForm()
    election = Election.query.get_or_404(election_id)
    if request.method == 'GET':
        form.name.data = election.name
        form.date.data = election.date
        form.state_id.data = election.state_id
        return render_template('admin_edit_election.html', user=curr_user, election=election, form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            election.name = form.name.data
            election.date = form.date.data
            election.state_id = form.state_id.data
            db.session.commit()
            flash(
                f'Election on {election.full_date} in {election.state.name} successfully changed', 'success')
            return redirect('/admin/elections')


@app.route('/admin/elections/<int:election_id>/delete', methods=['POST'])
def admin_delete_election(election_id):
    """Admin Feature - Delete Election"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    deleted_election = Election.query.filter(
        Election.id == election_id).first()
    db.session.delete(deleted_election)
    db.session.commit()
    flash(f'Election deleted', 'success')
    return redirect('/admin/elections')
