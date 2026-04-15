from core.user import User

if __name__ == "__main__":

    while True:
        print (f"{'='*50}")
        print("API Login")
        print(f"{'='*50}")
        print("\n1.login")
        print("2.register")
        print("3.exit")
        choice = input("please input your choice(1/2/3):")
        if choice == "1":
            username = input("please input your username:")
            password = input("please input your password:")
            user = User(username, password)
            ans = user.login()
            if ans:
                print(f"User {username} login successfully")
            else:
                print(f"User {username} login failed, please try again")

        elif choice == "2":
            username = input("please input your username:")
            password = input("please input your password:")
            user = User(username, password)
            ans = user.register()
            if ans:
                print(f"User {username} register successfully, please login continue")
                username = input("please input your username:")
                password = input("please input your password:")
                user = User(username, password)
                ans = user.login()
                if ans:
                    print(f"User {username} login successfully")
                else:
                    print(f"User {username} login failed, please try again")
            else:
                print(f"User {username} register failed, please try again")
        elif choice == "3":
            break
        else:
            print("wrong choice, please input your choice(1/2/3):")