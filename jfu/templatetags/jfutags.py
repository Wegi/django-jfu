from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import Library, Context, loader
import django

register = Library()

@register.simple_tag( takes_context = True )
def jfu(
        context,
        template_name = 'jfu/upload_form.html',
        upload_handler_name = 'jfu_upload',
        *args, **kwargs
    ):
    """
    Displays a form for uploading files using jQuery File Upload.

    A user may use both a custom template or a custom upload-handling URL
    name by supplying values for template_name and upload_handler_name
    respectively.

    Any additionally supplied positional and keyword arguments are directly
    forwarded to the named custom upload-handling URL.
    """
    context.update( {
        'JQ_OPEN'  : '{%',
        'JQ_CLOSE' : '%}',
        'upload_handler_url': reverse(
            upload_handler_name, args = args, kwargs = kwargs
        ),
    } )

    # Use the request context variable, injected
    # by django.core.context_processors.request,
    # to generate the CSRF token.
    context.update( csrf( context.get('request') ) )

    t = loader.get_template( template_name )

    # Fix deprecation error from django 1.9.0 and upwards.
    # Credit for fix goes to https://github.com/willson556
    if django.VERSION >= (1, 8):
        if isinstance(context, Context):
            context = context.flatten()
    else:
        if not isinstance(context, Context):
            context = Context(context)

    return t.render(context)
