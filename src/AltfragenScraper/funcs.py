import logging

def return_breakline(width):
    """Returns a line of ------- corresponding to the width of the logbox in order to visually break text apart"""
    width = width-24  # 20 since padx=10, 4 because... well, I don't know, some weird default padding in the textbox
    count = round(width/8)  # One - character takes up 8 pixels, hence pixels/8
    return '\n' + '-'*count + '\n'


def placeholder():
    print("This is a placeholder")


def get_data_str(data, format_is_selected="{}.*{}", format_not_selected="{}. {}"):
    string = ''
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    for i, id in enumerate(data['question_order']):
        question = data[id]
        index = i + 1  # Since enumerate starts at 0

        # Prints question
        string += "{}. {}\n".format(index, question['question'])
        
        for i, answer in enumerate(question['answers']):
            # Prints answer as two different strings depending on whether answer was selected or not
            if question['is_selected'][i] is True:
                string += "{}.*{}\n".format(ALPHABET[i], answer)
            else:
                string += "{}. {}\n".format(ALPHABET[i], answer)
            
        string += '\n'
    
    return string[:-2]  # Remove last \n