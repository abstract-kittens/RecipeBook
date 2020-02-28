import pymorphy2
morph = pymorphy2.MorphAnalyzer()

#s = """фелиное куре 500 грамм масло 120 грамм помидор 1 штука 
#        соль по вкусу жопа гнома 2 киллограмма"""
def parser_ingred(s):
    names = []
    mass = []
    mer  = []
    rez = []
    name = ""
    merName = ""
    lastitem = ""
    s = s.split()
    
    for item in s:
        
        if (item.isnumeric() == True):
            mass.append(item)
            names.append(name.rstrip())
            name = ""
            
        else:
            name += item + " "            
            if(lastitem.isnumeric() == True):
                forms = morph.parse(item)
                mer.append(forms[0].normal_form)
                name=""
                
            elif(lastitem == "по" and item == "вкусу"):
                mass.append('0')
                merName = lastitem + " " + item
                mer.append(merName)
                name=""
                merName="" 
        lastitem = item 
    i = 0
    while i < len(names):
        rez.append([names[i], mass[i], mer[i]])
        i += 1
    return rez
    #print(rez)

#s = "шаг 1 возьмите гнома шаг 2 отрежте гному жопу шаг 3 повторите шаг 1 и добавьте больше жоп в блюдо" 
def parser_step(s):
    rez = []
    number = 1
    temp = ""
    
    s = s.split();
    for i in range(len(s)):
        if(s[i] == "шаг" and s[i+1] == str(number)):
            if(temp != ''):
                rez.append(temp.rstrip())
            temp = "Шаг "
#            print(temp, number)
            number += 1  
        else:
            temp += s[i] + " "
            #print(temp)
    rez.append(temp.rstrip())
    return rez
#    print(rez)
        
        
    
    
#parser_step(s)    
#parser(s)
        