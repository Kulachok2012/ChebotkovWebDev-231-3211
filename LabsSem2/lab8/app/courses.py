from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

REVIEW_PARAMS = [
    'text', 'rating', 'course_id', 'user_id'
]

REVIEW_RATES = ['Ужасно', 'Плохо', 'Неудовлетворительно', 'Удовлетворительно', 'Хорошо', 'Отлично']


def params(param_type):
    return { p: request.form.get(p) or None for p in param_type }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

@bp.route('/')
def index():
    courses = CoursesFilter(**search_params()).perform()
    pagination = db.paginate(courses)
    courses = pagination.items
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = Course()
    categories = db.session.execute(db.select(Category)).scalars().unique().all()
    users = db.session.execute(db.select(User)).scalars().unique().all()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = Course()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        course = Course(**params(COURSE_PARAMS), background_image_id=image_id)
        db.session.add(course)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = db.get_or_404(Course, course_id)
    reviews = course.reviews if len(course.reviews) < 6 else course.reviews[-5:]
    current_user_review = db.session.execute(select(Review).where((Review.course_id == course_id) & (Review.user_id == current_user.id))).scalars().first()
    return render_template('courses/show.html', course=course, current_user_review=current_user_review, reviews=reviews, rates=REVIEW_RATES)


@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    course = db.get_or_404(Course, course_id)
    current_user_review = db.session.execute(select(Review).where((Review.course_id == course_id) & (Review.user_id == current_user.id))).scalars().first()
    return render_template('courses/reviews.html', course=course, current_user_review=current_user_review, rates=REVIEW_RATES)


@bp.route('/create_review', methods=['POST'])
@login_required
def create_review():
    try:
        local_params = params(REVIEW_PARAMS)
        local_params['rating'] = REVIEW_RATES.index(local_params['rating'])
        review = Review(**local_params)
        course = db.get_or_404(Course, local_params['course_id'])
        course.rating_num += 1
        course.rating_sum += local_params['rating']
        db.session.add(review)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()

    flash(f'Отзыв был успешно добавлен!', 'success')

    return redirect(url_for('courses.reviews', course_id=local_params['course_id']))
