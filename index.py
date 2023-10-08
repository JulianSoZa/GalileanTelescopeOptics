from packages import main, triplet, interpolation

print('Escoja el sistema de procesamiento: \n 1. Sistema Principal \n 2. Sistema Triplete \n 3. Interpolación')
n = input()

if(n == '1'):
    main.main_system()

elif(n == '2'):
    triplet.triplet_system()
    
elif(n == '3'):
    interpolation.interpolation_system()