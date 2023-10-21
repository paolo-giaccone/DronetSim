close all
clear all
clc
% Dati dei valori
msg01_thr_tot = [0
    42648.70717103242
27545.193115838116
56055.57066754085
38207.017361393395
44333.54863762362
43104.14826590589]' /1e3

msg01_thr_rel = [0
3442.279131273174
14378.346628144614
21069.07661639127
8338.86698938691
14959.172853185886
6572.618352602672
    ]'/1e3; % delta msg 0.1

msg01_thr_UAV = [0
 39206.42803975925
13166.8464876935
34986.49405114958
29868.150372006487
29374.37578443774
36531.529913303224
    ]'/1e3; % delta msg 0.1


msg015_thr_tot = [0
    12393.674841594
11696.852808452924
18992.382076752714
31495.467699062945
14358.986526268453
20648.531591270923
    ]'/1e3; % delta msg 0.15

msg015_thr_rel = [0,
   5551.68722356334
2811.1220837994597
10148.672775565834
18464.25660841005
6629.846597885375
9037.131692931129
    ]'/1e3; % delta msg 0.15

msg015_thr_UAV = [0
   6841.98761803066
8885.730724653466
8843.709301186878
13031.211090652892
7729.139928383078
11611.399898339794
    ]'/1e3; % delta msg 0.15


msg025_thr_tot = [0
    8458.067718473554
7097.975683982619
8395.703123624371
14787.282872732383
11742.66312722004
13649.797975741269    ]'/1e3; % delta msg 0.25

msg025_thr_rel = [0
   2875.9126946464744
1526.1858979211775
1894.896123991199
5358.931184890286
6114.018945137047
6141.05044960357
    ]'/1e3; % delta msg 0.25

msg025_thr_UAV = [0
   5582.15502382708
5571.789786061441
6500.806999633172
9428.351687842096
5628.644182082992
7508.7475261376985
    ]'/1e3; % delta msg 0.25

msg035_thr_tot = [0
    7078.953078812757
4519.42967985423
4936.6965367458615
4951.17839403509
6059.335662355763
9916.548070004737
    ]'/1e3; % delta msg 0.35

msg035_thr_rel = [0
2823.1034434067637
346.9271745946193
578.7851112046872
968.5120441713977
645.4685126344355
1417.7635755703336
    ]'/1e3; % delta msg 0.35

msg035_thr_UAV = [0
    4255.849635405993
4172.50250525961
4357.911425541174
3982.6663498636917
5413.867149721327
8498.784494434403
    ]'/1e3; % delta msg 0.35

msg05_thr_tot = [0
    3979.833520832686
3158.8789310194284
3464.9130218132104
3784.0228066002774
3145.585380656654
8656.627305080365
    ]'/1e3; % delta msg 0.5

msg05_thr_rel = [0
    354.4790990215348
160.90804206265184
103.01092767552788
382.65399167867974
750.2401913635123
1935.8305276642438
    ]'/1e3; % delta msg 0.5

msg05_thr_UAV = [0
  3625.3544218111515
2997.970888956777
3361.9020941376825
3401.3688149215977
2395.3451892931416
6720.79677741612
    ]'/1e3; % delta msg 0.5

msg07_thr_tot = [0
    2777.2033128791886
2458.2292725364823
2639.525848879967
2225.168284568916
2553.3500055319087
6388.590592025205
    ]'/1e3; % delta msg 0.7

msg07_thr_rel = [0
     136.8476994752064
93.46879363256586
109.98024370333194
246.29725287213193
523.3014145613099
601.1453352824215
    ]'/1e3; % delta msg 0.7

msg07_thr_UAV = [0
     2640.3556134039823
2364.7604789039165
2529.5456051766346
1978.8710316967843
2030.0485909705988
5787.445256742784
    ]'/1e3; % delta msg 0.7

msg085_thr_tot = [0
    2079.1961464669084
1774.6650644686465
1674.9409170936024
1875.420884907883
2075.6002661531065
5605.222971302921
    ]'/1e3; % delta msg 0.85

msg085_thr_rel = [0
    143.68428654446114
65.38239711200276
67.6743804886304
351.6414159202281
72.40466044720138
723.6748147586396
    ]'/1e3; % delta msg 0.85

msg085_thr_UAV = [0
   1935.5118599224472
1709.2826673566437
1607.266536604972
1523.779468987655
2003.1956057059049
4881.5481565442815
    ]'/1e3; % delta msg 0.85


msg1_thr_tot = [0
    2009.1911299657888
1322.0813276286851
2322.9343548921506
2005.3432665118444
1654.8244906258874
3291.3873042270125
    ]'/1e3; % delta msg 1

msg1_thr_rel = [0
    405.4421562711233
118.64832427436919
373.1621453642009
93.07500393092948
88.36441454798428
304.69144703603905
    ]'/1e3; % delta msg 1

msg1_thr_UAV = [0
   1603.7489736946654
1203.433003354316
1949.7722095279498
1912.2682625809148
1566.460076077903
2986.6958571909736
    ]'/1e3; % delta msg 1


msg2_thr_tot = [0
    686.6404607461792
864.7085345945493
870.5767227975441
783.006911044258
799.9288952093148
3449.998961125309
    ]'/1e3; % delta msg 2

msg2_thr_rel = [0
    31.936765616101354
50.3713709472553
27.784363493538642
84.19429151013527
124.43338369922674
1305.8070498036527
    ]'/1e3; % delta msg 2

msg2_thr_UAV = [0
    654.7036951300778
814.337163647294
842.7923593040055
698.8126195341227
675.495511510088
2144.1919113216563
    ]'/1e3; % delta msg 2

msg4_thr_tot = [0
    382.4091778202677
571.0336908573472
346.9433090162559
278.9514706485622
255.6323619745295
1938.6742626246053
    ]'/1e3; % delta msg 4

msg4_thr_rel = [0
    15.608537870215008
16.79510855462786
0.0
16.408910038150715
8.814909033604465
698.7567686753907
    ]'/1e3; % delta msg 4

msg4_thr_UAV = [0
 366.8006399500527
554.2385823027194
346.9433090162559
262.54256061041144
246.81745294092502
1239.9174939492145
    ]'/1e3; % delta msg 4

lambda = [0 1/4 1/2 1 1/.85 1/0.7 1/0.5 1/0.35 1/.25 1/0.15 1/0.1];% 12.5]; % I valori di lambda corrispondenti

% Numero di esperimenti
n_esperimenti = size(msg01_thr_UAV', 1);
conf = 0.5;
alpha = 1-conf;
pLo = alpha/2;
pUp = 1-alpha/2;
ts = tinv(conf, n_esperimenti-1);

% Calcola le medie dei punti per ogni valore di lambda
av4_tot = mean(msg4_thr_tot, 2);
av2_tot = mean(msg2_thr_tot, 2);
av1_tot = mean(msg1_thr_tot, 2);
av085_tot = mean(msg085_thr_tot, 2);
av07_tot = mean(msg07_thr_tot, 2);
av05_tot = mean(msg05_thr_tot, 2);
av035_tot = mean(msg035_thr_tot, 2);
av025_tot = mean(msg025_thr_tot, 2);
av015_tot = mean(msg015_thr_tot, 2);
av01_tot = mean(msg01_thr_tot, 2);

av = [0, av4_tot, av2_tot, av1_tot, av085_tot, av07_tot, av05_tot, av035_tot, av025_tot, av015_tot, av01_tot]

% Calcola la deviazione standard dei punti per ogni valore di lambda
dv4_tot = std(msg4_thr_tot,0, 2);
dv2_tot = std(msg2_thr_tot,0, 2);
dv1_tot = std(msg1_thr_tot, 0,2);
dv085_tot = std(msg085_thr_tot,0, 2);
dv07_tot = std(msg07_thr_tot,0, 2);
dv05_tot = std(msg05_thr_tot,0, 2);
dv035_tot = std(msg035_thr_tot,0, 2);
dv025_tot = std(msg025_thr_tot, 0, 2);
dv015_tot = std(msg015_thr_tot,0, 2);
dv01_tot = std(msg01_thr_tot,0, 2);

% Calcola gli intervalli di confidenza
CI_tot(1, :) = 0 + ts * 0
CI_tot(2, :) = av4_tot + ts * dv4_tot
CI_tot(3, :) = av2_tot + ts * dv2_tot
CI_tot(4, :) = av1_tot + ts * dv1_tot
CI_tot(5, :) = av085_tot + ts * dv085_tot
CI_tot(6, :) = av07_tot + ts * dv07_tot
CI_tot(7, :) = av05_tot + ts * dv05_tot
CI_tot(8, :) = av035_tot + ts * dv035_tot
CI_tot(9, :) = av025_tot + ts * dv025_tot
CI_tot(10, :) = av015_tot + ts * dv015_tot
CI_tot(11, :) = av01_tot + ts * dv01_tot

% Calcola le medie dei punti per ogni valore di lambda
av4_rel = mean(msg4_thr_rel, 2);
av2_rel = mean(msg2_thr_rel, 2);
av1_rel = mean(msg1_thr_rel, 2);
av085_rel = mean(msg085_thr_rel, 2);
av07_rel = mean(msg07_thr_rel, 2);
av05_rel = mean(msg05_thr_rel, 2);
av035_rel = mean(msg035_thr_rel, 2);
av025_rel = mean(msg025_thr_rel, 2);
av015_rel = mean(msg015_thr_rel, 2);
av01_rel = mean(msg01_thr_rel, 2);

av_rel=[0,av4_rel, av2_rel, av1_rel, av085_rel, av07_rel, av05_rel, av035_rel, av025_rel, av015_rel, av01_rel]

% Calcola la deviazione standard dei punti per ogni valore di lambda
dv4_rel = std(msg4_thr_rel,0, 2);
dv2_rel = std(msg2_thr_rel,0, 2);
dv1_rel = std(msg1_thr_rel, 0,2);
dv085_rel = std(msg085_thr_rel, 0,2);
dv07_rel = std(msg07_thr_rel, 0,2);
dv05_rel = std(msg05_thr_rel,0, 2);
dv035_rel = std(msg035_thr_rel,0, 2);
dv025_rel = std(msg025_thr_rel, 0, 2);
dv015_rel = std(msg015_thr_rel,0, 2);
dv01_rel = std(msg01_thr_rel,0, 2);

% Calcola gli intervalli di confidenza
CI_rel(1, :) = 0 + ts * 0
CI_rel(2, :) = av4_rel + ts * dv4_rel
CI_rel(3, :) = av2_rel + ts * dv2_rel
CI_rel(4, :) = av1_rel + ts * dv1_rel
CI_rel(5, :) = av085_rel + ts * dv085_rel
CI_rel(6, :) = av07_rel + ts * dv07_rel
CI_rel(7, :) = av05_rel + ts * dv05_rel
CI_rel(8, :) = av035_rel + ts * dv035_rel
CI_rel(9, :) = av025_rel + ts * dv025_rel
CI_rel(10, :) = av015_rel + ts * dv015_rel
CI_rel(11, :) = av01_rel + ts * dv01_rel


av4_UAV = mean(msg4_thr_UAV, 2);
av2_UAV = mean(msg2_thr_UAV, 2);
av1_UAV = mean(msg1_thr_UAV, 2);
av085_UAV = mean(msg085_thr_UAV, 2);
av07_UAV = mean(msg07_thr_UAV, 2);
av05_UAV = mean(msg05_thr_UAV, 2);
av035_UAV = mean(msg035_thr_UAV, 2);
av025_UAV = mean(msg025_thr_UAV, 2);
av015_UAV = mean(msg015_thr_UAV, 2);
av01_UAV = mean(msg01_thr_UAV, 2);

av_UAV=[0, av4_UAV, av2_UAV, av1_UAV, av085_UAV, av07_UAV, av05_UAV, av035_UAV, av025_UAV, av015_UAV, av01_UAV]

% Calcola la deviazione standard dei punti per ogni valore di lambda
dv4_UAV = std(msg4_thr_UAV,0, 2);
dv2_UAV = std(msg2_thr_UAV,0, 2);
dv1_UAV = std(msg1_thr_UAV, 0,2);
dv085_UAV = std(msg085_thr_UAV,0, 2);
dv07_UAV = std(msg07_thr_UAV,0, 2);
dv05_UAV = std(msg05_thr_UAV,0, 2);
dv035_UAV = std(msg035_thr_UAV,0, 2);
dv025_UAV = std(msg025_thr_UAV, 0, 2);
dv015_UAV = std(msg015_thr_UAV,0, 2);
dv01_UAV = std(msg01_thr_UAV,0, 2);

% Calcola gli intervalli di confidenza
CI_UAV(1, :) = 0 + ts * 0
CI_UAV(2, :) = av4_UAV + ts * dv4_UAV
CI_UAV(3, :) = av2_UAV + ts * dv2_UAV
CI_UAV(4, :) = av1_UAV + ts * dv1_UAV
CI_UAV(5, :) = av085_UAV + ts * dv085_UAV
CI_UAV(6, :) = av07_UAV + ts * dv07_UAV
CI_UAV(7, :) = av05_UAV + ts * dv05_UAV
CI_UAV(8, :) = av035_UAV + ts * dv035_UAV
CI_UAV(9, :) = av025_UAV + ts * dv025_UAV
CI_UAV(10, :) = av015_UAV + ts * dv015_UAV
CI_UAV(11, :) = av01_UAV + ts * dv01_UAV


Blu_p = "#0072BD"; % Blu pastello
Rosa_p = "#EDB120"; % Rosa pastello
Verde_p = "#A2142F"; % Verde pastello

% Disegna il grafico degli intervalli di confidenza
figure;

hold on;
grid on;
lambda = round(lambda, 1);
% Aggiungi i delimitatori personalizzati (molot) per gli intervalli di confidenza
%errorbar(lambda, av, CI_tot,  'Color', Blu_p, 'LineStyle', '-', 'LineWidth', 1);
line(lambda, av, 'Color', Blu_p, 'Marker', '.', 'MarkerSize', 20,'LineStyle', '-', 'LineWidth', 2);
%errorbar(lambda, av_UAV, CI_UAV, 'Color', Rosa_p, 'LineStyle', '-', 'LineWidth', 1);
line(lambda, av_UAV, 'Color', Rosa_p, 'Marker', '.','MarkerSize', 20, 'LineStyle', '-', 'LineWidth', 2);
line(lambda, av_rel, 'Color', Verde_p, 'Marker', '.', 'MarkerSize', 20,'LineStyle', '-', 'LineWidth', 2);
errorbar(lambda, av_rel, CI_rel, 'Color', Verde_p, 'LineStyle', '-', 'LineWidth', 1);

xlabel('Generation Rate [s^{-1}]', 'Interpreter', 'tex', 'FontSize', 12);
ylabel('BitLoss [kbps]', 'Interpreter', 'tex', 'FontSize', 12);

xticks(lambda);
xtickangle(90)

%ylim([-1; 100])
set(gca,'FontSize',16)

% Mostra la legenda
legend('Bit Loss TOT', ... %'Confidence interval Th_{TOT}', 
    'Bit Loss UAVs', ... %'Confidence interval Th_{UAV}', 
    'Bit Loss Relay','Confidence interval B\_loss_{Relay}', 'Max Datarate');

% Imposta le dimensioni desiderate per l'immagine rettangolare
larghezza = 4600; % Larghezza desiderata dell'immagine in pixel
altezza = 2400; % Altezza desiderata dell'immagine in pixel
set(gcf, 'PaperPosition', [0 0 larghezza/100 altezza/100]);

% Salva l'immagine in formato rettangolare (ad esempio, PNG)
nome_file = 'bitloss without miss pers';
formato_file = 'png';
saveas(gcf, nome_file, formato_file);