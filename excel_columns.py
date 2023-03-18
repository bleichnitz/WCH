def column_letters():
    """
    This simply generates a list of spreadsheet column headers in the form of an array
    this is instead of manually creating the array (e.g. col_letters = ["A", "B", ... "AA", "AB"....]
    the char_prefixes ultimately determines how many columns will be searchable in the find_col_array_index() function
    the number of columns is calculated by 26*len(char_prefixes); where 26 = the number of letters in alphabet
    :return: array of column headers from A to EZ
    """

    char_prefixes = ["", "A", "B", "C", "D", "E"]
    col_letters = []
    for p in range(0, len(char_prefixes)):
        ch = "A"
        col_letters.append(char_prefixes[p] + "A")
        for i in range(25):
            new_ch = chr(ord(ch) + 1)
            characters = char_prefixes[p] + new_ch
            col_letters.append(characters)
            ch = new_ch
    return col_letters


def find_col_array_index(column_letter):
    """
    This function allows user to simply insert the column header letters from the spreadsheet, and outputs the
    corresponding array index so that the user does not need to manually count the columns of the spreadsheet; reduces
    counting errors which will lead to mis-identification and mis-placement of data in the reading and writing of
    information
    :param column_letter: user inputs the column letter that is associated with the data that needs to be located
    within a spreadsheet
    :return: corresponding array index (e.g. column C has an array index of 2;
    """

    col_letters = column_letters()
    index = col_letters.index(column_letter)
    return index
