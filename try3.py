for i in [0,1,2]:
            ## in general program we will match through usernames not mail ids stored data in database
            print ("Your mail id please !")
            #engine.say('Your mail id please !')
            #engine.runAndWait()
            #mail_id = SmartApi.myCommand(self)
            mail_id = raw_input("mail_id = ")
            ## taking the password for only 1 id , can be upgraded afterwards , for multiple users
            if mail_id == "chetna agarwal":
                ## taking password for the ids but only 3 attempts are allowed  
                flag = 3
                #engine.say("enter your password")
                #engine.runAndWait()
                password = raw_input("Enter your password = ")                  
                while (mail_id == "chetna agarwal"):
                    ## if password is correct then ask for device operations (3 attempts)
                    if password == "chetna":
                        ## it can be reomved only if we call lights or alarm function after it  , user_log for login confirmation
                        ## confirming the log in by voice output
                        state = "You are logged in " + mail_id
                        print (state)
                        ##engine.say(state)
                        ##engine.runAndWait()
                        obj_SmartApi.valid_func(password)
                        ##("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass="+password)
                    elif flag > 0:
                    ## for wrong attempts
                        flag =  flag - 1
                        engine.say("enter your password")
                        engine.runAndWait()
                        password = raw_input("Enter your password = ") 
                    else :
                        print ("Exceeded the number of attempts , Try Again")
                        engine.say("exceeded the number of attempts , try again")
                        engine.runAndWait()
                        sys.exit(0)
        else :
            print ("wrong attempts exceeded")
            print ("Exiting the program ")
            engine.say("exiting the program")
            engine.runAndWait()
            sys.exit(

    def commands(self):
        ## extracting variables from the command for user defined input
        ## call the function of base class for taking the input command through speech

        print ("1.to control devices please login ! , say home automation login \nto exit the console say exit")
        #engine.say("to control devices please login for login , say home automation login to exit the console say exit")
        #engine.runAndWait()

        ## >>>> #extract_command = str(SmartApi_try.myCommand(self))
        extract_command = raw_input('extract_command = ')
        ## this loop works fine and returns only expected value
        if re.search(r"home automation" , extract_command) and re.search(r"login" , extract_command) :

            ## once login and password are it should be in infinte loop 
            ## and after a fixed time say 5 mins the program ends 
            ## only 3 attempts are allowed for mail_id input
            for i in [0,1,2]:
                ## in general program we will match through usernames not mail ids
                ## that too from stored data in database
                print ("Your mail id please !")
                #engine.say('Your mail id please !')
                #engine.runAndWait()

                ## takes the input for mail_id

                ## >>>> extra   self.mail_id = SmartApi_try.myCommand(self)
                self.mail_id = 'chetna agarwal'

                ## taking the password for only 1 id , 
                ## that can be upgraded afterwards , for multiple users

                ## to check the mail id of user if mail id matches then ask for password only
                if self.mail_id == "chetna agarwal":

                    ## taking password for the ids but only 3 attempts are allowed  
                    flag = 3
                    engine.say("Enter your password")
                    engine.runAndWait()
                    password = raw_input("Enter your password = ")                  
                    while re.search("chetna agarwal" , str(self.mail_id)):
                        ## if password is correct then ask for device operations (3 attempts)
                        if password == "chetna":
                            ## it can be reomved only if we call lights or alarm function after it  , user_log for login confirmation
                            ## confirming the log in by voice output
                            print ("You are logged in %s" %(self.mail_id))
                            engine.say("You are logged in %s" %(self.mail_id))
                            engine.runAndWait()

                            try :
                                requests_out =  requests.get("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass="+password)
                                ## checking the output of both json and text to get the api_key
                                print ("json output of the response \n %s"%(requests_out.json))
                                ## in case of response 200 , print "ok"
                                if int(re.findall(r'[0-9]+', str(requests_out.json))[0]) == 200:
                                    print ("OK")
                                    while 1:
                                        ## taking out API key from the response 
                                        self.response = ast.literal_eval(requests_out.text)
                                        user_input = 'yes'
                                        while (re.search(user_input , 'yes')):
                                            ## which device to operate by user  
                                            print ("what do you want to control \n1. alarm  \n2. lights")
                                            engine.say("choose one of them what do you want to control alarm or lights")
                                            engine.runAndWait()                                             
                                            #>>>>>>>>>>>>>>>>>>>>>>>>>>>            #self.device_operate = SmartApi_try.myCommand(self)
                                            self.device_operate = raw_input("device operate = ")
                                            ## more devices can be added in this module at 
                                            if re.search(r'lights|light' , self.device_operate) :
                                                ## call lights
                                                ## checking the status of lights
                                                self.lights()
                                            elif re.search(r'alarm' , self.device_operate):
                                                print ("Module is incomplete") 
                                                engine.say("Module is incomplete")
                                                engine.runAndWait()
                                                ## call alarm function here
                                            else :
                                                print ("I cannot control %s " %self.device_operate)
                                                engine.say("I cannot control %s " %self.device_operate)
                                                engine.runAndWait()
                                            
                                            ## for another session
                                            print ("do you want to operate other devices , yes or no") 
                                            engine.say("do you want to operate other devices , yes or no")
                                            engine.runAndWait()
                                            #>>>>>>>>>>>>>>>>>>>>>>>>>>>           
                                            #user_input = SmartApi_try.myCommand(self)
                                            user_input =  raw_input("user_input = ")
                                            if re.search('no' , user_input) or re.search('logout',  user_input):
                                                print ("logging out of system")
                                                engine.say("logging out of system")
                                                engine.runAndWait()
                                                self.response['api_key'] = "0"
                                                self.commands()
                                            else :
                                                pass
                            except requests.exceptions.Timeout as e:
                                print ("Timeout ! Try Again !")
                                engine.say("timeout try again")
                                engine.runAndWait()
                                self.commands()
                            except requests.exceptions.TooManyRedirects:
                                print ("Too Many Requests passed , Try Again !")
                                engine.say("too many requests")
                                engine.runAndWait()
                                self.commands()
                            except requests.exceptions.RequestException as e:
                                print ("lost connectivity . Try Again !")
                                engine.say("lost connectivity try again")
                                engine.runAndWait()
                                self.commands()
                        elif flag > 0:
                        ## for wrong attempts
                            engine.say("Enter your password")
                            engine.runAndWait()
                            password = raw_input("Enter your password = ") 
                            flag = flag - 1
                        else :
                            print ("Exceeded the number of attempts , Try Again")
                            engine.say("Exceeded the number of attempts , Try Again")
                            engine.runAndWait()
                            sys.exit(0)
        
 
            ## we will exit  while loop only after flag becomes 0
            ## variable to check no of attempts  
            else :   
                print ("three wrong attempts for mail id , try again")
                engine.say("three wrong attempts for mail id , try again")
                engine.runAndWait()
                print ("Exiting the program ")
                engine.say("Exiting the program")
                engine.runAndWait()
                sys.exit()
   
            
        elif re.search(r'exit' , extract_command):
            print ("Exiting the console")
            engine.say("Exiting the console")
            engine.runAndWait()
            sys.exit()
        else :
            print ("Unexpected command given by user ")
            self.commands()
            engine.say("Unexpected command given by user")
            engine.runAndWait()            