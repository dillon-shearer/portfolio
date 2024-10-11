import panel as pn

def get_content(back_callback):
    """
    Returns the content for the 'Healthcare Access' story.
    """
    title = 'Healthcare Access'
    description = """
    An in-depth look at healthcare accessibility across different regions and demographics.
    """

    # Initialize the progress bar
    progress = pn.indicators.Progress(
        name='Progress',
        value=100,
        max=100,
        bar_color='success',
        sizing_mode='stretch_width'
    )

    back_button = pn.widgets.Button(name='← Back to Home', button_type='primary', css_classes=['sidebar-link'])
    back_button.on_click(back_callback)

    content = [
        pn.pane.Markdown(f"## {title}", sizing_mode='stretch_width'),
        progress,
        pn.pane.Markdown(description, sizing_mode='stretch_width'),
        pn.pane.Markdown("### Content coming soon...", sizing_mode='stretch_width'),
        back_button
    ]

    return content
