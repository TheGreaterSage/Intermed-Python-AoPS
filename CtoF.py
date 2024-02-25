temperature = float(input("Enter a temperature:"))
measurement = str(input("Is your temperature in C or F?"))

if measurement == "C" or measurement == "c" or measurement == "celcius" or measurement == "Celcius":
    temperature = temperature * 9.0/5.0 + 32
    print("Your temperature in F is ", temperature)

if measurement == "F" or measurement == "f":
    temperature = (temperature - 32) * 5.0/9.0
    print("Your temperature in C is ", temperature)


    
