import os

def logout():
    logout = input("Do you wish to log out your computer ? (yes / no): ") 
  
    if logout == 'no': 
        exit() 
    else: 
        os.system("shutdown -l") 



logout()