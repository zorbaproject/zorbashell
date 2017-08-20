#!/usr/bin/python3

    #elif '/pinon' in command:
    #    pin = relay
    #    if len(command.split(' ')) > 1:
    #        pin = command.split(' ')[1]
    #    GPIO.setup(int(pin), GPIO.OUT)
    #    GPIO.output(int(pin), GPIO.HIGH)
    #    bot.sendMessage(chat_id, "Set "+str(pin)+" HIGH")
    #elif '/pinoff' in command:
    #    pin = relay
    #    if len(command.split(' ')) > 1:
    #        pin = command.split(' ')[1]
    #    GPIO.setup(int(pin), GPIO.OUT)
    #    GPIO.output(int(pin), GPIO.LOW)
    #    bot.sendMessage(chat_id, "Set "+str(pin)+" LOW")

#def my_callback(pin):
#    input_value = 0 #GPIO.input(pin)
#    print("The GPIO pin input "+str(pin)+" has value: "+str(input_value))
#    users = listusers()
#    if users != "":
#        for usr in users:
#            bot.sendMessage(usr, "The button on GPIO pin "+str(pin)+" changed value: "+str(input_value))


#os.system('modprobe w1-gpio')

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(button, GPIO.BOTH)
#GPIO.add_event_callback(button, my_callback)

