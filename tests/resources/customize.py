# {% raw %}
# Example customize.py file for j2cli
# Contains potional hooks that modify the way j2cli is initialized


def j2_environment_params():
    """ Extra parameters for the Jinja2 Environment """
    # Jinja2 Environment configuration
    # http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment
    return dict(
        # Just some examples

        # Change block start/end strings
        block_start_string='<%',
        block_end_string='%>',
        # Change variable strings
        variable_start_string='<<',
        variable_end_string='>>',
        # Remove whitespace around blocks
        trim_blocks=True,
        lstrip_blocks=True,
        # Enable line statements:
        # http://jinja.pocoo.org/docs/2.10/templates/#line-statements
        line_statement_prefix='#',
        # Keep \n at the end of a file
        keep_trailing_newline=True,
        # Enable custom extensions
        # http://jinja.pocoo.org/docs/2.10/extensions/#jinja-extensions
        extensions=('jinja2.ext.i18n',),
    )


def alter_context(context):
    """ Modify the context and return it """
    # An extra variable
    context['ADD'] = '127'
    return context


def extra_filters():
    """ Declare some custom filters.

        Returns: dict(name = function)
    """
    return dict(
        # Example: {{ var | parentheses }}
        parentheses=lambda t: '(' + t + ')',
    )


def extra_tests():
    """ Declare some custom tests

        Returns: dict(name = function)
    """
    return dict(
        # Example: {% if a|int is custom_odd %}odd{% endif %}
        custom_odd=lambda n: True if (n % 2) else False
    )

# {% endraw %}
