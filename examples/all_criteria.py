from klotan import match, criteria

template = {
    1: "bonjour", # Simple equality matching
    2: criteria.equals("bonjour"), # This is strictly the same
    2: { # It will compare every key of the template
        "x": 3, # You can use any primitive types
        "y": criteria.between(5, 12) # This criteria expects a number between 5 and 12
    },
}

value = {
    1: "bonjour",
    2: {
        "x": 3,
        "y": 6
    }
}

print(match.match(template, value).to_string())
assert match.match(template, value)

person_template = {
    # The gender can be either M, F or N/A
    "gender": criteria.is_in("M", "F", "N/A"),
    # Expects a name starting with a capital letter, followed by 1 to 15 letters
    "name": criteria.regex("[A-Z][a-z]{1,15}"),
    # Jeanne Calment still holds the world record
    "age": criteria.between(0, 122),
    # Matches all emails
    "email": criteria.is_email(),
    # Optional field, matches if value is an URL
    match.optional("personal_website"): criteria.is_url(),
    # Matches valid IBANs
    "iban": criteria.is_valid_iban(),
    # Matches valid credit card numbers
    "credit_card": criteria.is_valid_credit_card_number(),
    # We only accept people without debts !
    "amount_of_money": criteria.is_positive(),
    # This criteria will accept anything
    "bonus": criteria.accept(),
}

# Those are of course, fake information
person = {
    "gender": "M",
    "name": "Bob",
    "age": 18,
    "email": "bob.dupont@gmail.com",
    "personal_website": "https://bob.dupont.fr/",
    "iban": "FR68 1009 6000 7018 7224 1164 C75",
    "credit_card": "4929609419559701",
    "bonus": lambda: 0,
}

print(match.match(person_template, person).to_string())
assert match.match(person_template, person)