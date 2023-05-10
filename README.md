# stegHideShow
Steganography scripts for encoding text into an image file and decoding text from an image file.
Two scripts: stegHide.py and stegShow.py

## How the stegHide.py script works?
The stegHide.py script uses the Python Imaging Library (PIL) to hide a message in an image by modifying the least significant bits of the RGB values of each pixel in the image. The script first opens the image specified by the image_path argument, converts it to RGB mode, and gets its width and height. It then prompts the user to enter the message to be hidden in the image, and converts the message to binary using the int_to_bin function.

The script then adds a delimiter (eight zeroes) to the end of the binary message to mark the end of the message. It checks if the length of the binary message is less than or equal to the number of pixels in the image (width times height times three, since each pixel has three color channels), and raises a ValueError if the message is too large to be hidden in the image.

The script then iterates over the pixels in the image, and for each pixel, modifies the least significant bit of each color channel (red, green, and blue) to store a bit from the message. It does this by first getting the binary representation of the pixel values using the int_to_bin function, and then replacing the least significant bit of each color channel with a bit from the message.

Finally, the script creates a new image with the same size and mode as the original image, sets its pixel values to the modified pixel values, and saves the new image with a different filename that indicates that it contains an encoded message.

Note that this method of hiding a message in an image is not secure, since it is relatively easy for an attacker to detect and extract the hidden message. More secure methods of steganography (hiding messages in other types of media) exist, but they are beyond the scope of this script.

## How the stegShow.py script works?
The stegShow.py scripts also uses the Python Imaging Library (PIL), however now it is used to extract the hidden message from the encoded image, that was encoded using the hide_message function in the previous script. The script first opens the encoded image specified by the image_path argument, converts it to RGB mode, and gets its width and height.

The script then iterates over the pixels in the image, and for each pixel, extracts the least significant bit of each color channel (red, green, and blue) to recover the hidden message. It does this by first getting the binary representation of the pixel values using the int_to_bin function, and then getting the last (least significant) bit of each color channel.

The extracted message bits are stored in a list, and the script stops iterating over the pixels when it encounters the delimiter (eight zeroes) at the end of the message. The script then converts the message bits to a string using the bin_to_int function and the chr function, and removes the delimiter from the end of the message.

Finally, the script returns the extracted message as a string.

Note that this method of extracting a hidden message from an image is not secure, since it is relatively easy for an attacker to detect and extract the hidden message. More secure methods of steganography (hiding messages in other types of media) exist, but they are beyond the scope of this script.

## Preparation

The following Python modules must be installed:
```bash
pip3 install Pillow
```

## Permissions

Ensure you give the scripts permissions to execute. Do the following from the terminal:
```bash
sudo chmod +x stegHide.py
sudo chmod +x stegShow.py
```

## stegHide.py Usage
*** this will use the image.png, copy the image, then encode the user input message into a new image called image_encoded.png

```bash
 sudo python3 stegHide.py                                                                                   
Password:
Enter the message to encode: This is the secret message!
Message hidden in image
```

## stegShow.py Usage
*** this will decode the hidden message from the image_encoded.png file

```bash
 sudo python3 stegShow.py                                                                                   
This is the secret message!
```

## Sample stegHide.py script
```python
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
```

## Sample stegShow.py script
```python
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
```

## Disclaimer
"The scripts in this repository are intended for authorized security testing and/or educational purposes only. Unauthorized access to computer systems or networks is illegal. These scripts are provided "AS IS," without warranty of any kind. The authors of these scripts shall not be held liable for any damages arising from the use of this code. Use of these scripts for any malicious or illegal activities is strictly prohibited. The authors of these scripts assume no liability for any misuse of these scripts by third parties. By using these scripts, you agree to these terms and conditions."

## License Information

This library is released under the [Creative Commons ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/). You are welcome to use this library for commercial purposes. For attribution, we ask that when you begin to use our code, you email us with a link to the product being created and/or sold. We want bragging rights that we helped (in a very small part) to create your 9th world wonder. We would like the opportunity to feature your work on our homepage.

