from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdeCGqDOC-uJg7AX4EaGOzfQvTPtWTPnrjp11x3rd2ptlLuRZJ-UTDhDWnUltw5rE_22BQaYJ0EcD_3ErsUmILBdcrAWzFquS2j4sZwvj3VpzFDUi0_WIr2cop93LHuyvetkqD4EdvHjNxpW8rn2Gu3C9qwU1CKlzwtsD3KHdw1zEI5YQ='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
