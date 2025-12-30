#!/usr/bin/env python3

"""
    Python module to list, read and write 7zip format files.    
    https://py7zr.readthedocs.io/en/latest/api.html
"""

import os
import py7zr

def main():

    # Loop over all files on current working directory.
    for file_name in os.listdir(os.getcwd()):

        if  py7zr.is_7zfile(file_name):
            
            print(f'{file_name} is a 7Zip file.')

            zip_file = py7zr.SevenZipFile(file_name)

            print('Contains: ')
            for name in zip_file.getnames():
                print(name)

            if zip_file.needs_password():

                print(f'Sorry, {zip_file.filename} requires password!')

                # Let's try some passwords.
                for password in ['ka', 'kb', 'kc', 'kk', 'kl']:
                    try:
                        print(f'Trying password {password}')
                    
                        zip_file = py7zr.SevenZipFile(file_name, password=password)
                        zip_file.extractall()
                        
                        # Exit loop with first password success.
                        print(f'Password {password} was OK')
                        break

                    except Exception as e:
                        print("Error", e)

            else:
                zip_file.extractall()

        else:
            print(f'Sorry, {file_name} not a 7Zip file.')

if __name__ == '__main__':
    main()

##END##