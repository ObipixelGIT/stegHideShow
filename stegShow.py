# -*- coding: utf-8 -*-
# Author : Dimitrios Zacharopoulos
# All copyrights to Obipixel Ltd
# 10 May 2023

#/usr/bin/python3


# Print ASCII art
print("""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▄█▄░▄█░▄▄█░▄▄▄██░▄▄▄░█░████▀▄▄▀█░███░
█▄▄▀██░██░▄▄█░█▄▀██▄▄▄▀▀█░▄▄░█░██░█▄▀░▀▄
█▄▄▄██▄██▄▄▄█▄▄▄▄██░▀▀▀░█▄██▄██▄▄███▄█▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")


from PIL import Image

# Function to convert an integer to a binary string
def int_to_bin(n):
    return bin(n)[2:].zfill(8)

# Function to convert a binary string to an integer
def bin_to_int(b):
    return int(b, 2)

# Function to extract a hidden message from an image
def extract_message(image_path):
    # Open the image and convert it to RGB mode
    img = Image.open(image_path).convert('RGB')
    # Get the size of the image
    width, height = img.size
    # Iterate over the pixels in the image and extract the least significant bits
    pixels = list(img.getdata())
    message_bits = []
    for pixel in pixels:
        # Get the least significant bit of each color channel
        r, g, b = int_to_bin(pixel[0])[-1], int_to_bin(pixel[1])[-1], int_to_bin(pixel[2])[-1]
        # Add the least significant bits to the message bits list
        message_bits.extend([r, g, b])
        # If we have reached the end of the message, stop iterating
        if len(message_bits) >= 8 and message_bits[-8:] == ['0'] * 8:
            break
    # Convert the message bits to a string
    message = ''.join([chr(bin_to_int(''.join(message_bits[i:i+8]))) for i in range(0, len(message_bits), 8)])
    # Remove the delimiter from the end of the message
    message = message[:-1]
    return message

# Example usage
encoded_message = extract_message('image_encoded.png')
print(encoded_message)
