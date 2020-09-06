import requests
import hashlib
import sys

# Making the GET request to the API and returning a runtime error if the HTTP response isn't 200 - This might not be great practice?
def data_request(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f'Error fetching data from API: {res.status_code} - Check the API and try again')
    return res

# Just a lil boi to print the response
def read_response(response):
    print(response.text)


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())

    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


# Receives password argument to be hashed by SHA1 (what the API requires) - splices it, and returns the first 5 characters
def request_check(password):
    # Check password if it exists in API reponse
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Must send API the first 5 of hash
    # This grabs the first 5 characters of sha1password, puts it in the first_5 variable, and puts all characters after
    # the 5th into the tail varialbe
    first_5_characters, tail = sha1password[:5], sha1password[5:]
    response = data_request(first_5_characters)
    
    return get_password_leaks_count(response, tail)


# Main function
def main(args):
    # Loop through the arguments (passwords) passed to the file
    for password in args:
        # Grabbing the number of times the API has found the password in a data breach
        count = request_check(password)
        if count:
            print(f'{password} was found {count} times...You should PROBABLY change your password')
        else:
            print(f'Your password "{password}" was not found - Great job on making a solid password!')

    return 'Done!'

# Run program
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
