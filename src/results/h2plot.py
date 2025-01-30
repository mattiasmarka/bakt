import numpy
from matplotlib import pyplot

def load_data(f):
    next(f)
    data = []
    for line in f:
         fields = line.strip().split("\t")
         if len(fields) == 0:
             break
         data.append([])
         for field in fields:
             try:
                num = int(field)
             except:
                num = float(field)
             data[-1].append(num)
    return numpy.array(data)

chemical_accuracy = 1.59e-3

ntrots = lambda data: data[::, 1]
l = lambda data: data[::, 2]
h = lambda data: data[::, 3]
E = lambda data: data[::, 5]
fci_E = lambda data: data[::, 6]

if __name__ == "__main__":
   with open("h2demo.dat", "r") as f:
        data = load_data(f)
   fig, ax = pyplot.subplots(figsize=(1.5*6.4, 4.8))
   axins = ax.inset_axes(
       [0.12, 0.5, 0.68, 0.48],
       ylim=(0, chemical_accuracy * 2))
   ddata = data
   nt = ntrots(ddata)
   E_err = numpy.abs(fci_E(ddata) - E(ddata))
   ax.plot(nt, E_err)
   axins.plot(nt, E_err)
   ax.axhline(y = chemical_accuracy, color="k", linestyle="--", label="Keemiline täpsus")
   axins.axhline(y = chemical_accuracy, color="k", linestyle="--")
   axins.set_xticks(ax.get_xticks())
   ax.indicate_inset_zoom(axins, edgecolor="black")
   ax.set_xlabel("Trotterisammude arv")
   ax.set_ylabel("Energia viga (Ha)")
   fig.legend()
   fig.savefig("h2.jpg", dpi=1000)
