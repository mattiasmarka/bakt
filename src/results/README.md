Failis `bounds.jpg` on kujutatud energia vea sõltuvus akna suuruesest.
Akna all peame silmas energiavaheimikku, millest energiat otsitakse.
Joonis on tehtud H2 tasakaalu geomeetri jaoks.
Bittide arv valitud selline, et QFT potentsiaalne viga oleks väiksem kui keemiline täpsus.
Leidsin, et keemilise täpsuse saavutamiseks peab bittide arv olema -ceil(log_2 (keemiline täpsus / (energia ülempiir - energia alampiir))).
Viimane asjaolu tuleb sellest, et QFT viga pole suure tõenäosusega suurem kui 2^{-n-1}, kus n on bittide arv (vt KLM).
Bittide arv on iga akna jaoks erinev.
Piisavate trotterisammude arvu juures peaks energia viga olema väiksem kui keemiline täpsus iga akna suuruse jaoks --- seda ei õnnestunud saavutada <=12 trotterisammuga.

Failis `h2.jpg` on kujutatud energia vea sõltuvus trotterisammude arvust.
Akna suuruseks on võetud 1 Ha.

Fail `lih.jpg` on sama, mis `h2.jpg`, kuid LiH jaoks.
