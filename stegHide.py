# -*- coding: utf-8 -*-
# Author : Dimitrios Zacharopoulos
# All copyrights to Obipixel Ltd
# 10 May 2023

#/usr/bin/python3


# Print ASCII art
print("""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▄█▄░▄█░▄▄█░▄▄▄██░██░██▄██░▄▀█░▄▄
█▄▄▀██░██░▄▄█░█▄▀██░▄▄░██░▄█░█░█░▄▄
█▄▄▄██▄██▄▄▄█▄▄▄▄██░██░█▄▄▄█▄▄██▄▄▄
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")


from PIL import Image

# Function to convert an integer to a binary string
def int_to_bin(n):
    return bin(n)[2:].zfill(8)

# Function to convert a binary string to an integer
def bin_to_int(b):
    return int(b, 2)

# Function to hide a message in an image
def hide_message(image_path):
    # Open the image and convert it to RGB mode
    img = Image.open(image_path).convert('RGB')
    # Get the size of the image
    width, height = img.size
    # Ask user for the message to encode
    message = input('Enter the message to encode: ')
    # Convert the message to binary
    message_bin = ''.join([int_to_bin(ord(c)) for c in message])
    # Add a delimiter at the end of the message to mark its end
    message_bin += '00000000'
    # Check if the message can fit in the image
    if len(message_bin) > width * height * 3:
        raise ValueError('Message too large to be hidden in image')
    # Iterate over the pixels in the image and hide the message bits in the least significant bits
    pixels = list(img.getdata())
    new_pixels = []
    message_index = 0
    for pixel in pixels:
        if message_index >= len(message_bin):
            # If we have hidden all the message bits, add the remaining pixels to the new image
            new_pixels.append(pixel)
        else:
            # Get the binary representation of the pixel values
            r, g, b = int_to_bin(pixel[0]), int_to_bin(pixel[1]), int_to_bin(pixel[2])
            # Replace the least significant bit of each color channel with a message bit
            r = r[:-1] + message_bin[message_index]
            message_index += 1
            if message_index >= len(message_bin):
                # If we have hidden all the message bits, add the remaining pixels to the new image
                new_pixels.append((bin_to_int(r), bin_to_int(g), bin_to_int(b)))
            else:
                g = g[:-1] + message_bin[message_index]
                message_index += 1
                if message_index >= len(message_bin):
                    new_pixels.append((bin_to_int(r), bin_to_int(g), bin_to_int(b)))
                else:
                    b = b[:-1] + message_bin[message_index]
                    message_index += 1
                    new_pixels.append((bin_to_int(r), bin_to_int(g), bin_to_int(b)))
    # Create a new image with the same size and mode as the original image
    new_img = Image.new('RGB', (width, height))
    # Set the pixel values of the new image
    new_img.putdata(new_pixels)
    # Save the new image with a different filename
    new_img.save(image_path[:-4] + '_encoded.png')
    print('Message hidden in image')

# Example usage
hide_message('image.png')
