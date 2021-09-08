from random import randint

wind_dir=["N","NE","E","SE","S","SW","W","NE"]
wind_speed=["None" for i in range(12)]+["Light" for i in range(5)]+["Strong" for i in range(3)]
precipitation=["None" for i in range(12)]+["Light" for i in range(5)]+["Heavy" for i in range(3)]
temp=["Normal for season" for i in range(14)]+[str(round((randint(1,4)*10)/1.8))+"°C colder than normal" for i in range(3)]+[str(round((randint(1,4)*10)/1.8))+"°C hotter than normal" for i in range(3)]
months=["Hammer (Deepwinter)", "Alturiak (The Claw of Winter)", "Ches (The Claw of the Sunsets)", "Tarsakh (The Claw of the Storms)", "Mirtul (The Melting)", "Kythorn (The Time Of Flowers)", "Flamerule (Sumertide)", "Eleasias (Highsun)", "Eleint (The Fading)", "Marpenoth (Leafall)", "Uktar (The Rotting)", "Nightal (The Drawing Down)"]