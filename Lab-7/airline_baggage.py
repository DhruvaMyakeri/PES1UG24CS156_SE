def parse_booking(code):
    airline, flight, seat = code.split('-')
    return airline.upper(), int(flight), seat[-1].upper()

def total_weight(weights_csv):
    return sum(float(w) for w in weights_csv.split(','))

def tag_label(name):
    parts = name.split()
    return parts[0][0].upper() + '. ' + parts[1].upper()

def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    result = parse_booking(user_input)
    print("Airline, Flight and Seat Letter:", result)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    result = total_weight(user_input)
    print("Total Weight:", result)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    result = tag_label(user_input)
    print("Tag Label:", result)

if __name__ == "__main__":
    main()
