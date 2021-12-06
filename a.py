import os 
os.chdir("uploads/")
listafotos=[]
for file in os.listdir():
     for foto in os.listdir(file):
         listafotos.append((file,foto))
print(listafotos)