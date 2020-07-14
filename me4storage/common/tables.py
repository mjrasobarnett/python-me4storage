from terminaltables import SingleTable

def display_table(header, items, style='default', column_padding=None):
    """
    Display a list of items as a table with a header.
    Following style are supported:
        default     Display as a simple table with a header
        bordered    Display as a bordered table with borders and a header
        basic       display without header, separate items with tab

    :param header:
    :param items:
    :param style
    """
    if not items:
        return
    t = format_table(header, items, style, column_padding)
    print(t)

def format_table(header, items, style='default', column_padding=None):
    """
    Format a list of items as a table with a header.
    Following styles are supported:
        default     Display as a simple table with a header
        bordered    Display as a bordered table with borders and a header
        basic       display without header, separate items with tab

    :param header:
    :param items:
    :param style:
    :param column_padding: left and right column padding
    :return: String containing a formatted list of items
    """
    if not items:
        return ''

    if style == 'default' or style == 'bordered':
        if header:
            items = [header] + items
        tab = SingleTable(items)

        if style != 'bordered':
            # Drop table borders
            tab.inner_column_border = False
            tab.outer_border = False
            tab.inner_heading_row_border = False
            if column_padding is not  None:
                tab.padding_left, tab.padding_right = column_padding

        return '\n'.join([line.rstrip() for line in tab.table.split('\n')])
    elif style == 'basic':
        return '\n'.join(['\t'.join(i) for i in items])
    else:
        raise RuntimeError(f'Bad table display style: {style}')
