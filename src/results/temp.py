with open("temp.dat", "r") as f:
     with open("trotslenghtsdemo_h2.dat", "r") as g:
         for (line, gline) in zip(f, g):
             fields = line.split(" ")
             gfields = gline.split(" ")
             print(*gfields[:5], fields[8], fields[11][:-2], *gfields[5:])
