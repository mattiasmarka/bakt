from matplotlib import pyplot
import numpy

def loe_andmed(f):
    andmed = []
    for line in f:
        if len(line) == 0:
            break
        fields = line.strip().split(" ")
        if len(fields) <= 1:
             continue
        andmed.append([float(fields[1]),
                      float(fields[2]),
                      float(fields[3]),
                      int(fields[4]),
                      float(fields[5]),
                      float(fields[6]),
                      int(fields[7]),
                      float(fields[8]),
                      float(fields[9]),
                      float(fields[10])])
    return numpy.array(andmed)

with open("trotslenghtsdemo_h2.dat2", "r") as f:
     andmed = loe_andmed(f)

pyplot.figure(figsize=(6.4, 9.6), dpi=600)
N = 3
ax = pyplot.subplot(N, 1, 1)
ntrots = list(set(andmed[::, 3]))
for nt in sorted(ntrots):
    xandmed = andmed[numpy.where(andmed[::, 3] == nt)]
    ax.plot(xandmed[::, 0], xandmed[::, 4], "-", label = "ntrots = %d" % nt)
ax.legend()
ax.set_xlabel("Sidemepikkus (A)")
ax.set_ylabel("Energia (Ha)")

ax = pyplot.subplot(N, 1, 2)
ntrots = list(set(andmed[::, 3]))
axins = ax.inset_axes(
       [0.38, 0.3, 0.58, 0.48],
       ylim=(0, 1.59e-3 * 3))
for nt in sorted(ntrots):
    xandmed = andmed[numpy.where(andmed[::, 3] == nt)]
    ax.plot(xandmed[::, 0], abs(xandmed[::, 4] - xandmed[::, 5]), "-", label = "ntrots = %d" % nt)
    axins.plot(xandmed[::, 0], abs(xandmed[::, 4] - xandmed[::, 5]), "-")
ax.axhline(1.59e-3, linestyle="--", label="Keemiline täpsus")
axins.axhline(1.59e-3, linestyle="--")
ax.legend()
ax.set_xlabel("Sidemepikkus (A)")
ax.set_ylabel("Energia viga (Ha)")

ax = pyplot.subplot(N, 1, 3)
twinx = ax.twinx()
ntrots = list(sorted(ntrots))
ax.set_xticks([1, 2, 3, 4, 8, 10])
gates = [numpy.average(andmed[numpy.where(andmed[::, 3] == nt)][::, 6]) for nt in ntrots]
make_time = [numpy.average(andmed[numpy.where(andmed[::, 3] == nt)][::, 7]) / 60e9 for nt in ntrots]
transp_time = [numpy.average(andmed[numpy.where(andmed[::, 3] == nt)][::, 8]) / 60e9 for nt in ntrots]
run_time = [numpy.average(andmed[numpy.where(andmed[::, 3] == nt)][::, 9]) / 60e9 for nt in ntrots]
ax.plot(ntrots, gates, label="Väravate arv")
ax.set_xlabel("Trotterisammude arv")
ax.set_ylabel("Väravae arv")
twinx.plot(ntrots, make_time, "--", label="Koostamise aeg")
twinx.plot(ntrots, transp_time, "--", label="Transpileerimise aeg")
twinx.plot(ntrots, run_time, "--", label="Käiguaeg")
twinx.set_ylabel("Aeg (min)")
ax.legend()
twinx.legend(loc="lower right")

pyplot.savefig("trotslengths_h2.jpg")
