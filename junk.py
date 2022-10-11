

# def resolve_unk(input_list: list, start_index):
#     """
#
#     :param input_list: A dict representing the token indices of a sentence as keys and the language code of the token
#     as values.
#     :return: A dict with UNK elements resolved. (if possible)
#     """
#     for index, elem in enumerate(input_list[start_index:]):
#         # print(index, elem)
#         if elem[1] == 'UNK':
#             # print(index)
#
#             # if index == 0 get language of next token
#             if index == 0:
#                 new_elem = (elem[0], input_list[index+1][1])
#                 input_list[index] = new_elem
#                 start_index == index + 1
#
#             # if index == len(list)-1 get language of previous token
#             elif index == len(input_list)-1:
#                 new_elem = (elem[0], input_list[index-1][1])
#                 input_list[index] = new_elem
#                 start_index == index + 1
#
#             # if surrounding tokens have the same language EXCEPT UNK get the language of the surrounding tokens
#             elif input_list[index-1][1] == input_list[index+1][1] != "UNK":
#                     new_elem = (elem[0], input_list[index-1][1])
#                     input_list[index] = new_elem
#                     start_index == index + 1
#             else:
#                 # unresolved
#                 new_elem = elem
#                 start_index = index
#
#     if start_index <= len(input_list) - 1:
#         return resolve_unk(input_list, start_index)
#     else:
#         return input_list




def resolve_unk(input_list: list):
    """

    :param input_list: A list of tuples representing the indices and the language code of the token of a sentence.
    as values.
    :return: A dict with UNK elements resolved. (if possible)
    """
    new_list = []
    for index, elem in enumerate(input_list):
        # print(index, elem)
        if elem[1] == 'UNK':
            # print(index)
            # if index == 0 get language of next token
            if index == 0 and index+1 <= (len(input_list)-1):
                new_elem = (elem[0], input_list[index+1][1])
                new_list.append(new_elem)

            # if index == len(list)-1 get language of previous token
            elif index == len(input_list)-1:
                new_elem = (elem[0], input_list[index-1][1])
                new_list.append(new_elem)

            # if surrounding tokens have the same language EXCEPT UNK get the language of the surrounding tokens
            elif index + 1 <= (len(input_list) - 1) and input_list[index-1][1] == input_list[index+1][1]:
                if input_list[index-1][1] != "UNK":
                    new_elem = (elem[0], input_list[index-1][1])
                    new_list.append(new_elem)
                # unresolved
                else:
                    new_list.append(elem)
            else:
                # unresolved
                new_list.append(elem)

        else:
            new_list.append(elem)

    return new_list








my_list = [(0, 'UNK'), (1, 'UNK'), (2, 'LA'), (3, 'EN'), (4, 'UNK'), (5, 'EN'), (6, 'UNK')]
# my_list = [(0, 'EN'), (1, 'EN'), (2, 'EN'), (3, 'UNK'), (4, 'UNK'), (5, 'LA'), (6, 'LA')]
print(resolve_unk(my_list))