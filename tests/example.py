from Sequence_Generator import Digits

input_sequence = 251219
input_range_min = 0
input_range_max = 50
input_image_width = 500
input_range = (input_range_min, input_range_max)

digit_sequence = Digits(input_sequence, input_range, input_image_width,
                   image_quantity=5, show_result=True)
digit_sequence.generate()
