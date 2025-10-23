# Gearsbot
Το GearsBot, γνωστό και με την πλήρη ονομασία του "Generic Educational Robotics Simulator" (Gears), είναι ένας ισχυρός, τρισδιάστατος (3D) προσομοιωτής ρομποτικής. Δημιουργός και κύριος προγραμματιστής του είναι ο Cort Wee, συνιδρυτής της εταιρείας A Posteriori, ο οποίος το ανέπτυξε γύρω στο 2020-2021 ως εξέλιξη του προγενέστερου 2D προσομοιωτή EV3DevSim ενσωματώνοντας μια ρεαλιστική μηχανή φυσικής με σκοπό να παρέχει μια ακόμα πιο ρεαλιστική και ευέλικτη πλατφόρμα. Το Gears διατίθεται ως ελεύθερο λογισμικό ανοιχτού κώδικα (FOSS) υπό την άδεια GNU General Public License v3.0 (GPL-3.0) και αποτελεί ένα σύγχρονο εκπαιδευτικό εργαλείο. Προσφέρει ένα ολοκληρωμένο περιβάλλον που γεφυρώνει τον εικονικό με τον φυσικό προγραμματισμό. Συγκεκριμένα, επιτρέπει τη σχεδίαση, τη δοκιμή και τον προγραμματισμό σε Python ρομπότ που βασίζονται στα ενεργά στοιχεία του πακέτου LEGO Mindstorms EV3 και βρίσκεται σε συνεχή και ενεργή ανάπτυξη. Try it out at https://gears.aposteriori.com.sg ... or the latest version from github (https://quirkycort.github.io/gears/public/)  

# Προσπάθεια οργάνωσης μιας σειράς οδηγών διαβαθμισμένης πολυπλοκότητας για το GearsBot Simulator.
## worldScripts
https://gears.aposteriori.com.sg/?worldScripts=world_challenges  
https://gears.aposteriori.com.sg/?worldScripts=challenges_basic  
https://gears.aposteriori.com.sg/?worldScripts=world_Test.js  
  
# Line Following
## Κάθε πειραματική διάταξη ορίζεται από τις παρακάτω τρεις παραμέτρους:  
S (Sensors): Το πλήθος των αισθητήρων χρώματος (Color Sensors).  
A (Ahead): Η απόσταση look-ahead του αισθητήρα από τον άξονα των κινητήριων τροχών.  
G (Ground): Το ύψος τοποθέτησης του αισθητήρα από το έδαφος.  

Για τη συστηματική καταγραφή και σύγκριση, κάθε διαμόρφωση λαμβάνει έναν μοναδικό κωδικό της μορφής R_#S#A#G. Για παράδειγμα, η διαμόρφωση R_1S3A1G περιγράφει μια διάταξη με: 
1S = 1 αισθητήρα χρώματος.  
3A = 3 μονάδες LEGO (LU) απόσταση look-ahead.  
1G = 1 μονάδα LEGO (LU) ύψος από το έδαφος.  

Κωδικοποίηση και Χαρακτηριστικά των Ρομποτικών Διατάξεων
#S#A#G  (S)  (a,b,c)  (A)  (G)  Παρατηρήσεις
1S0A1G  1  (0, -5.8, 3.6)	0  (0 εκ.)  1  (0.8 εκ.)  Δοκιμή 0A  
1S1A1G	1  (0, -5.8, 4.4)	1 (0.8 εκ.) 	1 (0.8 εκ.)  Δοκιμή 1A  
1S2A1G	1  (0, -5.8, 5.2)	2 (1.6 εκ.) 	1 (0.8 εκ.)  Δοκιμή 2A  
**1S3A1G**	1  (0, -5.8, 6.0)	3 (2.4 εκ.) 	1 (0.8 εκ.)  **Βασική Διάταξη 1S**  
1S4A1G	1  (0, -5.8, 6.8)	4 (3.2 εκ.) 	1 (0.8 εκ.)  Δοκιμή 4A  
1S5A1G	1  (0, -5.8, 7.6)	5 (4.0 εκ.) 	1 (0.8 εκ.)  Δοκιμή 5A  
1S3A2G	1  (0, -5.0, 6.0)	3 (2.4 εκ.) 	2 (1.6 εκ.)  Δοκιμή 2G  
1S3A3G	1	(0, -4.2, 6.0)	3 (2.4 εκ.) 	3 (2.4 εκ.)  Δοκιμή 3G  
2S3A1G	2	(-2, -5.8, 6.0) & (2, -5.8, 6.0)	3 (2.4 εκ.) 	1 (0.8 εκ.)  Βασική Διάταξη 2S  
3S3A1G	3	(-2, -5.8, 6.0) & (2, -5.8, 6.0) & (0, -5.8, 6.0)	3 (2.4 εκ.)  1 (0.8 εκ.)  Βασική Διάταξη 3S  

<img width="1274" height="771" alt="R_EV3_1S3A1G" src="https://github.com/user-attachments/assets/b3b802c0-484e-49e6-af4f-83ada01a93e8" />

[R_1S3A1G](https://chzarafidis.github.io/gears/R_1S3A1G.json) 


### Simple Curves
<img width="1680" height="1050" alt="Turns-SimpleCurves" src="https://github.com/user-attachments/assets/ed604113-2f14-4ba3-bc7f-6d2a103517e3" />

[R_1S3A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S3A1G.json&worldScripts=world_challenges)    
[R_SingleFollower](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_SingleFollower.json&worldScripts=world_challenges) 

[R_2S3A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_2S3A1G.json&worldScripts=world_challenges)  
[R_DoubleFollower](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_DoubleFollower.json&worldScripts=world_challenges)  
  
[R_3S3A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_3S3A1G.json&worldScripts=world_challenges)  
  
[R_1S0A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S0A1G.json&worldScripts=world_challenges)  
[R_1S1A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S1A1G.json&worldScripts=world_challenges)  
[R_1S2A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S2A1G.json&worldScripts=world_challenges)  
[R_1S4A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S4A1G.json&worldScripts=world_challenges)  
[R_1S5A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S5A1G.json&worldScripts=world_challenges)  

[R_1S3A2G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S3A2G.json&worldScripts=world_challenges)  
[R_1S3A3G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S3A3G.json&worldScripts=world_challenges)  

## Sharp Turns
<img width="1680" height="1003" alt="Turns-Sharp" src="https://github.com/user-attachments/assets/e870e593-54da-488e-8268-73b5586a237c" />

[R_1S3A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S3A1G.json&worldScripts=world_challenges)  
[R_3S3A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_3S3A1G.json&worldScripts=world_challenges)  
  
[R_1S0A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S0A1G.json&worldScripts=world_challenges)  
[R_1S1A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S1A1G.json&worldScripts=world_challenges)  
[R_1S2A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Simple.json&robotJSON=https://chzarafidis.github.io/gears/R_1S2A1G.json&worldScripts=world_challenges)  
[R_1S4A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S4A1G.json&worldScripts=world_challenges)  
[R_1S5A1G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S5A1G.json&worldScripts=world_challenges)  

[R_1S3A2G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S3A2G.json&worldScripts=world_challenges)  
[R_1S3A3G](https://gears.aposteriori.com.sg/index.html?worldJSON=https://chzarafidis.github.io/gears/W_Sharp.json&robotJSON=https://chzarafidis.github.io/gears/R_1S3A3G.json&worldScripts=world_challenges)  

# Εργαλεία:
## URL Generator:
(https://gears.aposteriori.com.sg/genURL.html)

## Filters: 
[f.json](f.json)  
https://gears.aposteriori.com.sg/index.html?filterBlocksJSON=https://chzarafidis.github.io/gears/f.json  

[filter.json](filter.json)  
https://gears.aposteriori.com.sg/index.html?filterBlocksJSON=https://chzarafidis.github.io/gears/filter.json  

[filter_tw_sleep.json](filter_tw_sleep.json)  
https://gears.aposteriori.com.sg/index.html?filterBlocksJSON=https://chzarafidis.github.io/gears/filter_tw_sleep.json

## custom worlds
https://github.com/QuirkyCort/gears/tree/master/samples/custom%20worlds/customMap_noGroundDemo.json  
https://github.com/QuirkyCort/gears/tree/master/samples/custom%20worlds  
https://quirkycort.github.io/gears/samples/custom%20worlds/customMap_noGroundDemo.json  

## Training_Wheels:
https://quirkycort.github.io/gears/public/ev3dev2/Training_Wheels.py  
https://github.com/QuirkyCort/gears/tree/master/public/ev3dev2/Training_Wheels.py  

## world_challenges:
https://github.com/QuirkyCort/gears/tree/master/public/js/worlds/extra/world_challenges.js  
https://quirkycort.github.io/gears/public/js/worlds/extra/world_challenges.js  

## worldScripts:
https://gears.aposteriori.com.sg/index.html?worldJSON=https://files.aposteriori.com.sg/get/B9GeeMU54M.json&filterBlocksJSON=https://files.aposteriori.com.sg/get/YaRSZ9WSdZ.json&worldScripts=challenges_basic  
https://github.com/QuirkyCort/gears/blob/master/public/js/worlds/extra/world_challenges.js  
