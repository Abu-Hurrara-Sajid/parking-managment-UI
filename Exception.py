

# try:
    
#     num = float(input("Enter the number: "))

#     result = 100/ num  

# except ZeroDivisionError:
#     print("Error: You can't divide by zero!")

# except ValueError:
#     print("Error: Please enter valid numbers.")

# else:
   
#     print(f"The result is {result}")

# finally:
 
#     print("Execution complete.")

# try:
#     file =open("Exception.py",'r')
# except FileNotFoundError:
#     print("File not Found")


# try:
#     x=int(input("Enter a number: "))
# except ValueError:
#     print("This is not a number")
# else:
#     print("You entered :",x)
# finally:
#     print("Program ended")


# class UnderAgeError(Exception):
#        pass
# try:
#         age=int(input("Enter a number:"))
#         if age< 18:
#             raise UnderAgeError("you must be 18 or older")
#         else:
#           print("Eligible ")
# except UnderAgeError as e:
#         print (e)



# numbers = [10, 20, 30]

# try:
#     index = int(input("Enter an index to access the list: "))
#     print(f"The value at index {index} is {numbers[index]}")

# except IndexError:
#     print("Error: The index you entered is out of range!")

# except ValueError:
#     print("Error: Please enter a valid integer.")

# else:
#     print("Accessed the list successfully!")

# finally:
#     print("IndexError example complete.")





# student = {"name": "John", "age": 21, "course": "Math"}

# try:
#     key = input("Enter the key you want to access (name, age, course): ")
#     print(f"The value for '{key}' is {student[key]}")

# except KeyError:
#     print(f"Error: The key '{key}' does not exist in the dictionary!")

# else:
#     print("Accessed the dictionary successfully!")

# finally:
#     print("KeyError example complete.")




# try:
#     x = int(input("Enter a number: "))
#     print("You entered ",x)
# except ValueError:
#     print("Error: You did not enter a valid number.")
# finally:
#     print("Executed")


class UnderAgeError(Exception):
    

 while True: 
    try:
        age = int(input("Enter your age: "))
        if age < 18:
            raise UnderAgeError("You must be 18 or older to proceed.")
        else:
            print("Eligible!")
            break
    except UnderAgeError as e:
        print(e)
        print("Please try again.\n")
    except ValueError:
        print("Invalid input! Please enter a valid number.\n")




