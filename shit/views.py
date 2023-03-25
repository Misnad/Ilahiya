from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from shit.models import Users, Posts, Drafts, Comments
from shit import db
import html

view = Blueprint('view', __name__)


@view.route('/')
def home():
    return render_template('index.html', all_posts=Posts.query.order_by(Posts.date.desc()).all(), user=current_user, users=Users.query)


@view.route('/write')
@login_required
def write():
    return render_template('write.html', all_drafts=Drafts.query.all(), user=current_user)


@view.route('/latest')
def latest():
    return redirect('/')


@view.route('/writer')
@login_required
def writer():
    args = request.args
    draft_id = args.get('draft')
    if draft_id == None:
        # Create an empty draft
        post_author = current_user.id
        post_content = ""
        post_title = ""
        new_content = Drafts(author=post_author, content=post_content, title=post_title)
        try:
            db.session.add(new_content)
            db.session.commit()
        except:
            return "Something went wrong!"
        draft_id = new_content.get_id()
    return render_template('writer.html', draft=Drafts.query.get(draft_id))


# TODO make javascript that saves automatically every minute.
@view.route('/save', methods=['POST'])
@login_required
def save():
    draft_id = int(request.form['id'])
    draft = Drafts.query.get_or_404(draft_id)
    draft.author = current_user.id
    draft.content = request.form['content']
    draft.title = request.form['title']
    if draft.title.strip() == "":
        flash("Heading can't be empty!", category='error')
        return render_template('writer.html', draft=Drafts.query.get(draft_id))
    try:
        db.session.commit()
        return redirect(url_for('view.write'))
    except:
        return "Something went wrong!"


@view.route('/publish', methods=['POST'])
@login_required
def publish():
    post_author = current_user.id
    post_content = html.escape(request.form['content'], quote=True)
    post_title = request.form['title']
    draft_id = int(request.form['id'])
    if post_title.strip() == "":
        flash("Heading can't be empty!", category='error')
        return render_template('writer.html', draft=Drafts.query.get(draft_id))
    new_content = Posts(author=post_author, content=post_content, title=post_title)
    try:
        db.session.add(new_content)
        db.session.delete(Drafts.query.get(draft_id))
        db.session.commit()
        return redirect('/write')
    except:
        return "Something went wrong!"


@view.route('/delete', methods=['GET'])
@login_required
def delete():
    args = request.args
    draft_id = args.get('draft')
    if Drafts.query.get(draft_id).author == current_user.id:
        try:
            db.session.delete(Drafts.query.get(draft_id))
            db.session.commit()
        except:
            return "Something went wrong!"
    return redirect('/write')


@view.route('/reader')
def reader():
    args = request.args
    post = Posts.query.get(args.get('post'))
    return render_template('reader.html', post=post, author=Users.query.get(post.author).name, content=html.unescape(post.content).split("\n"))

# TODOs
# [x] Click post to open full in new page
# [x] test on phone
# [x] Add git
# [ ] publish
# [ ] About page
# [ ] Ability to remove published posts