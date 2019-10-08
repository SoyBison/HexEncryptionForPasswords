
#######################################PASSWORD MANAGER#########################################
Written by Coen D. "Technolibre" Needell, originally for use by Washington University in St. Louis Alumni
and Development offices. Released with permission.

######################################Table of Contents#########################################
1.Introduction..................................................................................
2.General Usage.................................................................................
3.Code Breakdown................................................................................
4.Security Rant.................................................................................
5.Modding Guide.................................................................................
################################################################################################
1. Introduction.................................................................................

	This program was built with the intention that it would be used as a password/login 
manager. It essentially just keeps a text file encrypted, and allows you to read it from the
command line. You can also add lines this way. This is a pretty simple program, and as of V1.0,
you cannot subtract lines.

	The encryption algorithm used is PBKDF2, a symmetric key encryption method. Meaning that
it can be unlocked with a single key, shared by all parties which want to access the encrypted
information. The first cipher of this kind was the Vigenere Cipher, which remained unbreakable
for three centuries after it was discovered. To understand the Vigenere Cipher, first you need
to know the Caesar Cipher. In the Caesar Cipher, to encrypt a message you would take each letter
in the message, and shift it along the alphabet by a fixed number of spaces, known only to the
intended recipient. This is testable in polynomial time. Theoretically one would only need to 
test the first couple words of the message against the numbers 1-26 in order to break the code.
The Vigenere Cipher is like the Caesar Cipher, except each letter in the message would have a
different Caesar shift applied to it, and you would move along a code word in order to get each
number. If your code word was "Able", you would shift the letters in the order: 1-2-12-5-1-2-12-5
and so on until you got to the end of the message. This method of doing things remained
unbreakable for 300 years. The Cipher, however was subject to user error, and was mathematically
broken in the 16th century. Despite this, the Confederate States of America used Vigenere during
the American civil war, and thus, their 'secret' messages were practically public knowledge 
among the union command. The cipher was eventually replaced by the one-time-pad, which is 
theoretically unbreakable. This is a technique where a randomly generated list of letters is
used as the vigenere key. Thus, each letter is encrypted seperately by random letter, and
the cipher can only be broken if a person has access to the original pad. Now, this is labor 
intensive, and requires the user to carry around a pad, which is subject to be stolen, burnt
photographed, and occasionally eaten. Enter the modern cryptographic hash function. With the
advent of computer miniaturization, we were able to cut the labor required to encrypt and
decrypt a message using the one-time pad and Vigenere methods drastically. This allows someone
to reliably generate a pad, given the same input, while at the same time, the correct pad cannot
be easily guessed, even by a computer. This input is the password that you put in when you log 
into things, it's the password you'll enter to use this program. Now, a problem came along with
this structure as well, the key, or hash, is always the same with the same password. So what's 
stopping a hacker from generating a dictionary of all the passwords and their hashes? This is,
as of 2005, doable by a home pc in polynomial time. That's a scary fact. So what do we do to 
make passwords safe again? We will put a "SALT" before our password to make it unreasonably hard
for a hacker to produces such a table, this brings us to the modern technique for encryption.
Recently, a new method has surfaced, but it isn't widespread yet, and this program uses the old
method to such a degree that it won't matter that much for a while. 

	Facts about this program's hashing and encrypting.
It uses a 256 bit hexadecimal SALT. This is so that the salt can be stored in plaintext, without
the risk of interpetation problems across machines that can arise using UTF-32 salts that some
cryptographers choose to use. Why is it so long? The longer the salt is, the more likely it is
to be unique, and that's the goal, so that a hacker cannot have a table for all passwords. The 
reason why you can totally trust an encryption scheme like this is, the key to the file is not
stored anywhere. It's generated on the spot, when you enter your password. Many authentication
schemes have the key stored, and keep the salt and the password hidden, allowing hackers to 
"Brute Force" guess the password. If you were to try and brute force this file, you would need
first to build a machine capable of telling when the file transforms from gibberish to english.
This is not really worth the effort since the thing you're storing here are passwords, which
aren't discernable english in the first place. It's also worth pointing out that the system
will generate a new SALT every time you run it. This added protection makes it harder for a
hacker to make a rainbow table just for you. This occurs not only every time a new line is added
but every time the file is read via the program as well.

	This program uses SHA512 encryption running 1000000 times. This is pretty serious. At the
time of writing the NIST standards for SHA512 is to run it ~20000 times. This combined with the
long SALT makes your encryption (barring a huge technological breakthrough) too hard to break for
your average hacker. The fact that I used a non-standard encryption method should confound many
hackers as well, which affords an additional level of protection. The only part of this program
which does not employ the state-of-the-art in encryption is the key-derivation function. It uses
PBKDF2 which, while effective, is a little outdated, and has been usurped by argon2 and scrypt.
Despite this, the extra protection afforded by the added iterations and the abnormal salt should
make up for this. At the time of writing, windows 7 machines have trouble running scrypt in
openssl via python, and argon2 is propriatary.
#################################################################################################
2. General Usage.................................................................................

	You can use this program by simply running the attached "Password_Manager.exe" It will
then encrypt the first .txt file it finds in the same folder as the .exe . This will work with any
.txt file, so long as it's the first one in the folder alphabetically. It doesn't need to be called
"SECRET STUFF.txt", you can feel free to rename it. Then, if the program finds a txt file, it will
ask you for the password. If the file is in plain-text, the program will encrypt it with your
password. If it's encrypted, it will be decrypted with your password, then the entire document 
will be displayed in the command line. If you need to copy the passwords to some field, you can
also open the encrypted file at this time, and things will be in plaintext. If you'd like to change
the password at this point, you can close the program and run it again, it will act as though it's
a new file to encrypt. You can also take this time to add lines en masse to the file.
	Back in the command line interface, you will see the input statement: "Press 'n' to enter
or Enter to re-encrypt." If you enter "n", the program will have you type in a new line to be put
into the document. If you just press "Enter" the program will re-encrypt the document, and it will
be safe from prying eyes.
	Due to the nature of modern encryption, if you forget your password, the document should
be considered to be gone forever. Technically we could concievably crack it, and contact me should
this become necessary, but there's no guarantee. 

	If you'd like to distribute this program, make sure to send everything in the containing
file. The readme is important so that people know how to use the program, and the libs/python3.6.dll
are necessary for the .exe to work. For a simple distribution consider zipping all the files 
into a redistributable archive. 

#################################################################################################
3.Code Breakdown.................................................................................

	The code itself is broken out into four functions, encrypt(), decrypt(), filechk(), and
main(). The first two are pretty self-explanatory. encrypt() will encrypt your file, decrypt() 
will decrypt it. Filechk() is a simple way to find the file you want to encrypt. main() strings
the above together so that you, the user, needs to only run one program in order to use this system.
If you wish to gain a better understanding of how they work together, I have left comments in the
source code, which is included in this folder.

##################################################################################################
4.Security Rant...................................................................................

	The following is a short editorial on the state of computer security.
	If you want something to be secure, the security of your encryption or authentication is
only as strong as your encryption key, or your authentication password. Even systems like 
2-factor authentication are vulnerable to simple carelessness and usage of weak passwords. In 
general, longer and more complicated is better, but people have trouble remembering those. Personally
I like to prescribe the "XKCD method", to come up with a number of random words, and string them 
together. These are easy to remember, and hard to crack. The example Randall Munroe gave when he
came up with the method was "Correct Horse Battery Staple" Also don't be afraid to use spaces and
punctuation. Just adding spaces to a password can add up to 5 orders of magnitude to the memory
cost of cracking them. The point is, even if you have a cryptographically strong password to all
your accounts, but you use this program with a short, password that's just an english word with a
number tacked on at the end, you will compromise all of your accounts. Please encrypt responsibly.

##################################################################################################
5.Modding Guide...................................................................................

The main thing I can think of that you'd like to do with this program is to make it stronger in the
future. This is pretty simple, just adjust the parameters under the key deriving function. Increase
iterations, or even change the function to something better in the future. I have the compiler set
with cx_freeze, so you need that in python in order to do this. Besides that, the list of required
modules is in the source code. I wrote it in python 3.6, but it runs fine on python 3.7, there's 
just some issues with cx_freeze in python 3.7 at the moment. Just read my documentation and comments.
And make sure you unencrypt your stuff before changing out the .exe. 

###################################################################################################
Written using PyCharm by JetBrains, by Coen D. Needell, for WUSTL A&D. 
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                      `                                                                                               
                                                     ##                                                                                               
                                                   `@@                                                                                                
                                                  ;@@:                                                                                                
                                                 #@@@                                                                                                 
                                               `@@@@                                                                                                  
                                              '@@@@`                                                                                                  
                                        +    @@@@@`                                                                                                   
                                        @@@@@@@@@                                                                                                     
                                        @@@@@@@@`                                                                                                     
                                        @@@@@@@.                                               :.                                                     
                                        @@@@@@.                                                 @`                                                    
                                       ,@@@@@` @                        `#@@                    @@                                                    
                                       @@@@@  ,@                      .@@@@,                    @@`                                                   
                                      +@@@@;  @@                   `+@@@@@                      +@#       @                                           
                                      @@@@#  #@@                 #@@@@@@#                       `@@       @@                                          
                                     #@@@@   @@:              '@@@@@@@@.                         @@+      ;@                                          
                                     @@@@,  @@@            '@@@@@@@@@'                           @@@       @@                                         
                                    :@@@@  `@@#         `@@@@@@@@@@+                             ;@@,      @@                                         
                                    @@@@.  @@@`       :@@@@@@@@@@@                               `@@@   ;  +@'                                        
                                    @@@@  ,@@@     `#@@@@@@@@@@@,                                 @@@   @+ :@@                                        
                                   :@@@'  @@@;   ;@@@@@@@@@@@@`                                   @@@.  @@,.@@                                        
                                   @@@@  '@@@ .@@@@@@@@@@@@#                                      #@@@  '@@`@@;                                       
                                   @@@@  @@@@@@@@@@@@@@@@#                            '           :@@@   @@@@@@                                       
                                  ,@@@; @@@@@@@@@@@@@@@#                              @           `@@@`  @@@@@@                                       
                                  @@@@` @@@@@@@@@@@@@+                                +#           @@@#   @@@@@                                       
                                  @@@@ @@@@@@@@@@@@;                                  .@           @@@@   ;@@@@                                       
                                 ,@@@@@@@@@@@@@@@'                                     @+          #@@@    @@@@,                                      
                                 @@@@@@@@@@@@@@#                                       @@          `@@@'   ;@@@#                                      
                                 @@@@@@@@@@@@@`                                        #@;          @@@@    @@@@;                                     
                                 @@@@@@@@@@@#                                          :@@          +@@@    '@@@@,                                    
                                `@@@@@@@@@@+                                            @@          `@@@'    @@@@@                                    
                                .@@@@@@@@@;                                             @@'          @@@@    @@@@@`                                   
                                :@@@@@@@@.                                              #@@          @@@@    @@@@@#                                   
                                '@@@@@@@                                                .@@`         '@@@`   @@@@@@                                   
                                +@@@@@@                       ;                          @@@         `@@@+   @@@@@@.                                  
                                #@@@@@                       :@                          @@@          @@@@   @@@@@@#                                  
                                #@@@@.                       +@.                         ;@@@         @@@@   @@@@@@@                                  
                                #@@@@`                       #@.                          @@@ ,.      @@@@   @@@@@@@                                  
                                +@@@@                        @@,                          @@@@@+      @@@@   @@@@@@@                                  
                                '@@@@                        @@;              #           `@@@@;      @@@@   @@@@@@@                                  
                                ,@@@@;                       @@:              @.           @@@@;      @@@@   @@@@@@'                                  
                                 @@@@@                       @@'              @#           #@@@;      @@@@  @@@@@@@`                                  
                                 @@@@@@                      @@#              @@           ,@@@:      @@@@@#@@@@@@@                                   
                                  @@@@@@                     @@#              @@            @@@'      @@@@@@@@@@@@+                                   
                                  ;@@@@@@                    @@@              @@.           @@@#     `@@@@@@@@@@@@                                    
                                   @@@@@@@.                  @@#              #@;           @@@@     @@@@@@@@@@@@                                     
                                    @@@@@@@+                 @@#              +@@           +@@@    @@@@@@@@@@@@                                      
                                    `@@@@@@@@                @@+              :@@           +@@@:  @@@@@@@@@@@@                                       
                                     ,@@@@@@@@:             .@@+              .@@           #@@@@@@@@@@@@@@@@#                                        
                                      .@@@@@@@@@.           #@@+              `@@           @@@@@@@@@@@@@@@@:                                         
                                        #@@@@@@@@@`        `@@@+               @@           @@@@@@@@@@@@@@#                                           
                                         ,@@@@@@@@@@`      @@@@'               @@`         @@@@@@@@@@@@@'                                             
                                           +@@@@@@@@@@'  `@@@@@:               @@'       ;@@@@@@@@@@@@;                                               
                                             @@@@@@@@@@@@@@@@@@                @@@     `@@@@@@@@@@@#`                                                 
                                              .@@@@@@@@@@@@@@@@                @@@   ,@@@@@@@@@@@`  :'#`                                              
                                                ;@@@@@@@@@@@@@@                @@@@@@@@@@@@@@@@.`#@@@@@,                                              
                                                  #@@@@@@@@@@@@.               @@@@@@@@@@@@@@;`@@@@@@@@`                                              
                                         ,          #@@@@@@@@@@@               @@@@@@@@@@@@+`@@@@@@@@@@                                               
                                        @@@+`         .@@@@@@@@@,              @@@@@@@@@@+ #@@@@@@@@@@@                                               
                                        ,@@@@@#:`       +@@@@@@@@`             @@@@@@@@@ ,@@@@@@@@@@@@@                                               
                                         @@@@@@@@@#      .@@@@@@@@`            @@@@@@@, '@@@@@@@@@@@@@'                                               
                                         @@@@@@@@@@@#`     @@@@@@@@`           @@@@@@+ '@@@@@@@@@@@@@@                                                
                                         @@@@@@@@@@@@@#     @@@@@@@@#';:,...``#@@@@@@ `@@@@@@@@@@@@@@@                                                
                                         +@@@@@@@@@@@@@@.    @@@@@@@@@@@@@@@@@@@@@@@; @@@@@@@@@@@@@@@'                                                
                                         :@@@@@@@@@@@@@@@,    @@@@@@@@@@@@@@@@@@@@@@;'@@@@@@@@@@@@@@@                                                 
                                         `@@@@@@@@@@@@@@@@:    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                 
                                          @@@@@@@@@@@@@@@@@'.``@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                  
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                                  
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                   
                                          .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                    
                                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                     
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                      
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                       
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                                                        
                                              #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                                          
                                               ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                                            
                                                `@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                             
                                                  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                             
                                                    `+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`                                                            
                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                                           
                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                                          
                                                        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'                                                         
                                                        +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                        
                                                        :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                       
                                                        ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                                     
                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@;                                                    
                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                   
                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@;                                                  
                                                       .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@;                                                  
                                                       +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'                                                  
                                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                                  
                                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                   
                                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                    
                                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`                                                    
                                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                                     
                                                      .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                      
                                                      ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                                      
                                                      '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                       
                                                      +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+.                                                        
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                                
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`                                                               
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                                                               
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                               
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`                                                              
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                              
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                              
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                                             
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                             
                                                      #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                                            
                                                      +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                            
                                                      '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                           
                                                      ;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                                                          
                                                      ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                         
                                                      .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                        
                                                      `@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@;                                                      
                                                      `@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`                                                    
                                                      .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                   
                                                     `@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                                                  
                                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                                 
                                                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                 
                                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                
                                                   '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                   #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@;                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                               
                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                   +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                
                                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                                                
                                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                                
                                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                 
                                                    :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                 
                                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                 
                                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                                 
                                                     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                  
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                  
                                                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                   
                                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'                                                   
                                                       .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                    
                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                     
                                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'                                                     
                                                         ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                      
                                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                                                      
                                                          `@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                                       
                                                           ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                        
                                                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                         
                                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                                                         
                                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                          
                                                              '@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                           
                                                              ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                           
                                                              `;'@@@@@@@@@@@@@@@@@@@@@@@;..                                                           
                                                                   `#@@@@@@@@@@@@@@@@:                                                                
                                                                      @@@@@@@@@@@@@#                                                                  
                                                                       @@@@@@@@@@@+                                                                   
                                                                        @@@@@@@@@@                                                                    
                                                                        `@@@@@@@@                                                                     
                                                                         ,@@@@@@                                                                      
                                                                          '@@@@                                                                       
                                                                           +@@`                                                                       
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
