def return_breakline(width):
    """Returns a line of ------- corresponding to the width of the logbox in order to visually break text apart"""
    width = width-24  # 20 since padx=10, 4 because... well, I don't know, some weird default padding in the textbox
    count = round(width/8)  # One - character takes up 8 pixels, hence pixels/8
    return '\n' + '-'*count + '\n'


def placeholder():
    print("This is a placeholder")