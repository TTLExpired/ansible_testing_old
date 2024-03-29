import sys
import yaml
from pudb import set_trace
from xlrd import open_workbook


def convert_sheet_list(sheet, xrows, ycolumns):
    '''
    A function to convert the spreadsheet into a nested list.
    '''
    rows = []

    for first_row in range(0, xrows):
        row_counter = 0
        jump_counter = 0
        key_value = (sheet.cell(first_row, 0).value)

        if key_value != '':
            internal_value = []
            col_counter = sheet.ncols
            rows.insert(first_row, key_value)

        if key_value == '':
            row_counter += 1

        for col in range(1, ycolumns):
            data_value = (sheet.cell(first_row, col).value)
            if data_value != '':
                try:
                    data_value = str(int(data_value))
                except ValueError:
                    pass
                finally:
                    internal_value.append(data_value)
                    jump_counter += 1
        if jump_counter == col_counter * row_counter:  
            rows.append(internal_value)

    print(rows)
    return rows


def convert_list_dictionary(sheet, nested_list):
    '''
    A function to convert the list created earlier into a nested dictionary.
    '''
    global_dict = {}
    curr_dict = {}
    first_key = sheet.name

    for row in nested_list:
        curr_values_list = []
        if len(row) >= 1:
            key = str(row)
            for i in range(1, len(row)):
                if row[i] != '':
                    curr_values_list.append(row[i])
            curr_dict[key] = curr_values_list
    global_dict[first_key] = curr_dict

    return global_dict


def print_in_yaml_format(dictionary):
    '''
    Function to simply print dictinary in Yaml Format
    '''
    print(yaml.dump(dictionary, default_flow_style=False))


def input_to_file(dictionary):
    '''
    Function to create Yaml format into a file based on sheet name.
    '''
    book_name = sys.argv[1]
    book_name = book_name.split('.')
    book_name = book_name[0]

    with open(book_name, 'w') as f:
        f.write(yaml.dump(dictionary, default_flow_style=False))

    print('Data copied to {} '.format(book_name))


def main():
    '''
    the main function is simply taking the file name and sending it to
    convert it to a list, followed by a dictionary.
    '''
    book = open_workbook(sys.argv[1])
    sheet = book.sheet_by_index(0)
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols

    rows = convert_sheet_list(sheet, number_of_rows, number_of_columns)
    global_dict = convert_list_dictionary(sheet, rows)

    print(global_dict)
    # Let's test by printing rows
    # input_to_file(global_dict)


if __name__ == "__main__":
    main()
