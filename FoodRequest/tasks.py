from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_multi_format_email(base_prefix, template_prefix, template_ctxt, target_emails):

    subject_file = "{0}/{1}_subject.txt".format(base_prefix, template_prefix)
    txt_file = "{0}/{1}.txt".format(base_prefix, template_prefix)
    html_file = "{0}/{1}.html".format(base_prefix, template_prefix)

    subject = render_to_string(subject_file).strip()
    from_email = settings.EMAIL_FROM
    to_emails = target_emails
    bcc_email = settings.EMAIL_BCC
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails,
                                 bcc=[bcc_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
