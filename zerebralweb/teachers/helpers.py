from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from datetime import timedelta, date


def send_course_invite_email(invite_url, student_name, course_name, student_email):
    plaintext = get_template('email/invite_student.txt')
    html = get_template('email/invite_student.html')

    d = Context({'invite_url': invite_url, 'student_name': student_name, 'course_name': course_name})

    subject, from_email, to = "You've been invited to a Zerebral course!", 'noreply@zerebral.com', student_email
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_current_week(begin_date, end_date):
    current_week = begin_date
    week_count = 1

    while current_week < end_date:
        if current_week <= date.today() <= (current_week + timedelta(days=7)):
            return week_count

        week_count += 1
        current_week += timedelta(days=7)

    return 1