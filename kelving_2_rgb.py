from math import log, pow,ceil
# from myutils import constrainValue,mapValue

MIN_TEMPERATURE = 1000
MAX_TEMPERATURE = 12000
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 100
MIN_COMPONENT = 0
MAX_COMPONENT = 255


def mapValue(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
def constrainValue(x,out_min,out_max):
    return min(max(out_min,x),out_max)

def scaled_2_brightness(rgb,brightness = MAX_BRIGHTNESS):
    brightness = int(ceil(constrainValue(brightness,MIN_BRIGHTNESS,MAX_BRIGHTNESS)))
    rgb = map(lambda x: constrainValue(x,MIN_COMPONENT,MAX_COMPONENT), rgb)
    rgb = map(lambda x : mapValue(brightness,MIN_BRIGHTNESS,MAX_BRIGHTNESS,MIN_COMPONENT,x),rgb)
    return tuple(map(int,rgb))

    
def kelvin_2_rgb(kelvin, brightness = MAX_BRIGHTNESS):
    temperature = int(constrainValue(kelvin,MIN_TEMPERATURE,MAX_TEMPERATURE))
    brightness = int(ceil(constrainValue(brightness,MIN_BRIGHTNESS,MAX_BRIGHTNESS)))
    red,green,blue = 255.0,.0,255.0

    temperature *= 0.01
    
    if temperature > 66.0 :
        red = temperature - 60.0
        red = 329.698727466 * pow(red,-0.1332047592)
        green = 288.1221695283 * pow(temperature - 60.0, -0.0755148492)
        
    else:
        green = (99.4708025861 * log(temperature)) - 161.1195681661

    if temperature<65 :
        if temperature <= 19.0:
            blue = 0
        else:
            blue = (138.5177312231 * log(temperature - 10.0)) - 305.0447927307    
            
   
    return scaled_2_brightness([red,green,blue],brightness)



def kelvin_2_rgb_TH(kelvin, brightness = MAX_BRIGHTNESS):
    temperature = constrainValue(kelvin,MIN_TEMPERATURE,MAX_TEMPERATURE)
    brightness = ceil(constrainValue(brightness,MIN_BRIGHTNESS,MAX_BRIGHTNESS))
    red,green,blue = 255.0,.0,255.0

    temperature *= 0.01
    
    if temperature > 66.0 :
        # red = 329.698727466 * pow(temperature - 60.0,-0.1332047592)
        red = 329.698727446 * pow(temperature - 60.0,-0.1332047592)
        green = 288.1221695283 * pow(temperature - 60.0, -0.0755148492)
        
    else:
        green = (99.4708025861 * log(temperature)) - 161.1195681661

        if temperature <= 19.0:
            blue = 0
        else:
            blue = (138.5177312231 * log(temperature - 10.0)) - 305.0447927307    
            
    return scaled_2_brightness([red,green,blue],brightness)

# ////////////////////////////////////////////////////////////////
# //
# //  Neil Bartlett formulas
# //
def kelvin_2_rgb_NB(kelvin, brightness = MAX_BRIGHTNESS):

    t = constrainValue(kelvin,MIN_TEMPERATURE,MAX_TEMPERATURE)
    brightness = ceil(constrainValue(brightness,MIN_BRIGHTNESS,MAX_BRIGHTNESS))
    red,green,blue = 0.0,.0,0.0

    t *= 0.01

    if (t <= 66):

        red = 255
        green = t - 2
        green = -155.25485562709179 - 0.44596950469579133 * green + 104.49216199393888 * log(green)
        blue = 0
        if (t > 20):
            
            blue = t - 10
            blue = -254.76935184120902 + 0.8274096064007395 * blue + 115.67994401066147 * log(blue)
            
    
    else:
    
        red = t - 55.0
        red = 351.97690566805693 + 0.114206453784165 * red - 40.25366309332127 * log(red)
        green = t - 50.0
        green = 325.4494125711974 + 0.07943456536662342 * green - 28.0852963507957 * log(green)
        blue = 255
    

    return scaled_2_brightness([red,green,blue],brightness)

   

if __name__ == "__main__":

    texto_menu="""
    KELVIN 2 RGB

Turn kelvin to RGB

Algorithms (0,1,2)
Kelvin [1000.0,6500.0]
Brightness [.0,100.0]

Usage:
    6500
    6500,50.0
    0,6500,50.0


"""
    print(texto_menu)
    algorithms = (kelvin_2_rgb,kelvin_2_rgb_NB,kelvin_2_rgb_TH)
    while True:

        try:
            algorithm = -1
            user_input = input("\nUser : ").strip()
            parts = user_input.split(",")
            # print(parts,len(parts))
            if len(parts)==3:
                algorithm = int(parts[0])
                kelvin = float(parts[1])
                brightness =float(parts[2])
            elif len(parts) ==2:
                kelvin = float(parts[0])
                brightness =float(parts[1])
            elif len(parts) == 1:
                kelvin = float(user_input)
                brightness = 100.0
            else:
                raise Exception("Too many arguments.")
            
       

        except KeyboardInterrupt:
            input("\nAdiós!\nPulsa enter para salir")
            break
        except Exception as e:
            print("Error, intenta de nuevo\n", e)

        else:
            if algorithm in range(len(algorithms)):
                funcs = (algorithms[algorithm])
               
            else:
                funcs = algorithms
                
                for func in funcs:
                    rgb = func(kelvin,brightness)
                    print(f"Kelvin = {kelvin:.2f} Brightness = {brightness:.2f} RGB = ",rgb)
            