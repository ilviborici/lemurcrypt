from cryptography.fernet import Fernet
import base64, os, hashlib, argparse

def main():

  banner()
  parser = argparse.ArgumentParser()

  parser.add_argument("--encrypt",  "-e",  help="For encryption of a file/folder")
  parser.add_argument("--decrypt",  "-d",  help="For decryption of a file/folder")
  parser.add_argument("--password", "-p",  help="Encryption key.")

  data = parser.parse_args()

  if(data.encrypt and data.password):
    m_key = data.password.encode()
    key = hashlib.md5(m_key).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode("utf-8"))
    if os.path.isdir(data.encrypt):
      directory = os.listdir(data.encrypt)
      os.chdir(data.encrypt)
      for file in directory:
          encrypt(file, key_64)

    else:
      encrypt(data.encrypt, key_64)

    print("\n"+" @-->--->--- Password: " + data.password + "\n"+" (You will not see it again!!)"+"\n")

  elif (data.decrypt and data.password):
    m_key = data.password.encode()
    key = hashlib.md5(m_key).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode("utf-8"))
    if os.path.isdir(data.decrypt):
      directory = os.listdir(data.decrypt)
      os.chdir(data.decrypt)
      for file in directory:
        decrypt(file, key_64)
    else:
      decrypt(data.decrypt, key_64)
  else:
    print("""
    
    Usage: rosebit.py [Option] [file]
    Example: rosebit.py -e file.txt -p 123
    
    """)
    
def encrypt(filename, key):
    extension = ".rose"
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)
            print(filename + " was encrypted.")
        os.rename(filename, filename+ extension)
    except Exception as e:
        print(e)
        quit()

def decrypt(filename, key):
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(filename, "wb") as file:
            file.write(decrypted_data)
            print(filename + " was decrypted.")
        
    except Exception as e:
        print(e)
        quit()
    os.rename(filename, os.path.splitext(filename)[0])


def banner():
    print("""      
       :                       ..,,..    ...,,..
      ,%,                .. ,#########::#########:,
      :#%%,           ,,:',####%%%%%%##:`::%%%%####,
     ,##%%%%,      ,##%% ,##%%%:::::''%' `::::%%####,
     %###%%;;,   ,###%%:,##%%:::''    '  . .`:::%%###,
    :####%%;;:: ,##%:' ,#%::''   .,,,..    . .`::%%%##,
    %####%;;::,##%:' ,##%''  ,%%########%     . `:::%%##,
    ######:::,##%:',####:  ,##%%:''     `%%,     .`::%%##,
    :#####%:'##%:',#####' ,###%' ,%%%%,%%,'%,     . ::%%###,,..
     #####%:,#%:'#######  %%:'%  %'  `%% %% %%,.     '::%%#######,
     `####%,#%:',####### ::' %   ' ,%%%%%%, ::%%.    . '::%%######
      `###'##%: ######## ,.   %%  %%,   ':: `:%%%  :  . .:::%%###'
      ,,::,###  %%%%%### ::  % %% '%%%,.::: .:%%%   #.  . ::%%%#'
,,,:::%%##:;#   `%%%%%## :% ,%, %   ':%%:'  #%%%' ,.:##.  ::%#'
::%%#####% %%:::  :::%%% `%%,'%%     ..,,%####' :%# `::##, ''
###%%::'###%::: .   `:::, `::,,%%%######%%'',::%##' ,:::%##
''''   ,####%:::. .  `::%,     '':%%::' .,::%%%#'   :::%%%##,
      :#%%'##%:::.  . . "%::,,.. ..,,,,::%%%###'  ,:%%%%####'
     ,###%%'###%:::: . . `::::::::::%%%#####'   ,::%####:'
     %###%%;'###%::::.   .`::%%%%%%%#####:'  ,,::%%##:'
     ####%;:;'####%:::::.   `:%######::'  ,,:::%%###
     %####;:;'######%%::::.           ,::::%%%####'
     `####%;:'`#########%%:::....,,:::%%%#######'
        ;#####;;'..;;:::#########::%%#########:"'
                       ~~~~``````''''~~~
    """)



if __name__ == "__main__":
    main()
    input("Press enter to exit")
