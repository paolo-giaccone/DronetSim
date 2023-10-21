close all
clear all
clc
% Dati dei valori
msg01_thr_tot = [0
    34010.025962575906
45883.447159541276
52411.18754895389
56055.57066754085
49685.14599961721
69567.38943489155]' /1e3

msg01_thr_rel = [0
    5685.251255269663
4904.49992716601
21069.07661639127
15794.353754571948
23885.540540541268
4593.13093712439
    ]'/1e3; % delta msg 0.1

msg01_thr_UAV = [0
    29416.89502545152
40198.19590427162
47506.68762178788
34986.49405114958
33890.79224504527
45681.84889435029
    ]'/1e3; % delta msg 0.1


msg015_thr_tot = [0
    11866.553266289598
18294.206470169625
19792.59089567307
31495.467699062945
26657.31422557451
18745.610843399733
    ]'/1e3; % delta msg 0.15

msg015_thr_rel = [0,
    5508.976123753134
4003.2608775126128
5973.159125012837
18464.25660841005
15448.59473676153
4098.537628469716
    ]'/1e3; % delta msg 0.15

msg015_thr_UAV = [0
    6357.577142536465
14290.945592657012
13819.431770660234
13031.211090652892
11208.719488812982
14647.073214930018
    ]'/1e3; % delta msg 0.15


msg025_thr_tot = [0
    9886.475510706374
13081.289337152673
9616.375502162156
33512.82351037175
14787.282872732383
21727.191092071593
    ]'/1e3; % delta msg 0.25

msg025_thr_rel = [0
    1198.3140536549347
3987.258311587729
3706.8136871131837
20684.663949081223 
5358.931184890286
14039.854623809284
    ]'/1e3; % delta msg 0.25

msg025_thr_UAV = [0
    8688.16145705144
9094.031025564946
5909.561815048973
12828.15956129053 
9428.351687842096
7687.33646826231
    ]'/1e3; % delta msg 0.25

msg035_thr_tot = [0
    8096.408737431385
10202.51422832888
9368.960847846374
9916.548070004737
7328.333973791099
14270.687834100885
    ]'/1e3; % delta msg 0.35

msg035_thr_rel = [0
    898.1910635177848
3549.648046068348
431.35907417057996
12474.120971473309
726.7474635185306
3682.8737141712713
    ]'/1e3; % delta msg 0.35

msg035_thr_UAV = [0
    7198.2176739136
6652.866182260533
8937.601773675795
8498.784494434403
6601.586510272568
10587.814119929613
    ]'/1e3; % delta msg 0.35

msg05_thr_tot = [0
    6526.980035379321
9453.165666199591
8917.622060364434
8656.627305080365
7456.787022932885
4758.825904965702
    ]'/1e3; % delta msg 0.5

msg05_thr_rel = [0
    589.4674497081537
440.15718232395136
737.4652224384523
1935.8305276642438
568.2950483313356
869.5493242413359
    ]'/1e3; % delta msg 0.5

msg05_thr_UAV = [0
   5937.5125856711675
9013.008483875641
8180.156837925981
6720.79677741612
6888.491974601549
3889.2765807243654
    ]'/1e3; % delta msg 0.5

msg07_thr_tot = [0
    6504.087336061946
6456.213612608052
4830.415699299468
6388.590592025204
4285.7146422966825
3984.4117385338077
    ]'/1e3; % delta msg 0.7

msg07_thr_rel = [0
    668.1967704312136
280.45503239770403
220.6088996825637
601.1453352824213
756.5556457417626
681.9921889083278
    ]'/1e3; % delta msg 0.7

msg07_thr_UAV = [0
    5835.890565630732
6175.758580210348
4609.806799616904
5787.445256742783
3529.15899655492
3302.41954962548
    ]'/1e3; % delta msg 0.7

msg085_thr_tot = [0
    4700.519688110662
4127.468272015131
4730.233161321954
5605.222971302921
2852.2683845608003
3913.9830210375967
    ]'/1e3; % delta msg 0.85

msg085_thr_rel = [0
    232.50211278646944
260.301970724006
177.49686860974808
723.6748147586396
411.7954437329895
659.3535744687646
    ]'/1e3; % delta msg 0.85

msg085_thr_UAV = [0
    4468.017575324193
3867.1663012911254
4552.736292712207
4881.5481565442815
2440.472940827811
3254.629446568832
    ]'/1e3; % delta msg 0.85


msg1_thr_tot = [0
    2948.6941354261157
3291.3873042270125
4911.007410840827
4397.892203297319
3764.1828564465172
6170.658666042972
    ]'/1e3; % delta msg 1

msg1_thr_rel = [0
    226.01574138224836
304.69144703603905
348.8862690795656
851.881047128448
866.4050845990213
369.60663338957704
    ]'/1e3; % delta msg 1

msg1_thr_UAV = [0
    2722.6783940438677
2986.6958571909736
4562.121141761261
3546.011156168871
2897.777771847496
5801.052032653395
    ]'/1e3; % delta msg 1


msg2_thr_tot = [0
    1612.7084701015579
1656.930901963189
2143.3336217153187
2286.0478272908636
1409.9291852976166
3449.998961125309
    ]'/1e3; % delta msg 2

msg2_thr_rel = [0
    24.47191063370966
192.1918440367639
92.6649745424321
775.7062404164477
417.1901279894983
1305.8070498036527
    ]'/1e3; % delta msg 2

msg2_thr_UAV = [0
    1588.236559467848
1464.739057926425
2050.6686471728867
1510.341586874416
992.7390573081183
2144.1919113216563
    ]'/1e3; % delta msg 2

msg4_thr_tot = [0
    895.1571212027301
1069.8014660707609
1272.8031172188034
1938.6742626246053
1178.8931885449165
1615.1388465640714
    ]'/1e3; % delta msg 4

msg4_thr_rel = [0
    69.78407836625992
96.90543787717183
95.9944666549386
698.7567686753907
398.47437205023596
422.40829270150846
    ]'/1e3; % delta msg 4

msg4_thr_UAV = [0
    825.3730428364702
972.896028193589
1176.8086505638648
1239.9174939492145
780.4188164946804
1192.7305538625628
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
nome_file = 'bitloss with miss pers';
formato_file = 'png';
saveas(gcf, nome_file, formato_file);