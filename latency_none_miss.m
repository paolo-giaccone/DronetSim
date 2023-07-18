close all
clear all
clc
% Dati dei valori

msg01_lat_rel = [
    0
    62.814508297370736
52.1718041171707
59.767083103912206
56.18295240524717
54.07961968628032
74.14607288865918
    ]'; % delta msg0.1

msg01_lat_UAV = [0
   38.44080760994648
23.36493184211801
29.061500173093336
32.82922928680726
32.91114468212233
31.998290748604088
    ]'; % delta msg 0.1

msg015_lat_rel = [
    0
    70.70955464225774
52.644752676218495
37.17472503383363
34.96795605411895
45.282322308897704
47.17039069112044
    ]'; % delta msg0.15

msg015_lat_UAV = [0
13.926596981089375
25.39079054686143
5.206090288085709
9.029137921753554
16.929316693973252
12.300465208869145
    ]'; % delta msg 0.15

msg025_lat_rel = [
    0
    59.41220387594727
33.91651353424719
19.32495815793816
18.123002152707155
30.32881290017401
36.62394169958616
    ]'; % delta msg0.25

msg025_lat_UAV = [0
15.079924429043883
3.3775811146316252
8.112145912666698
11.001770444842977
3.9376642510359776
6.382827745422082
    ]'; % delta msg 0.25

msg035_lat_rel = [
    0
    47.108494509245894
8.297994751821065
9.813514218036449
23.669413242285792
15.432083997258053
13.558797751653492
    ]'; % delta msg0.35

msg035_lat_UAV = [0
0.4682479710148514
0.27826561135263794
1.293079068181663
2.0009423539953843
4.6551291200939104
4.17166949029208
    ]'; % delta msg 0.35

msg05_lat_rel = [
    0
    2.07922871008634
28.075681308962324
1.3242501993279363
0.21075438186532988
26.054844381135766
5.003505552333971
    ]'; % delta msg0.5

msg05_lat_UAV = [0
1.5377330595879144
0.6430525446046411
0.7101637729582021
1.4416447885794743
4.3807744734721155
1.9096832300316506
    ]'; % delta msg 0.5

msg07_lat_rel = [
    0
    0.3573211780387459
0.12168244402592455
1.1994062376243535
0.7918670393178178
8.984787763892536
2.256989986909043
    ]'; % delta msg0.7

msg07_lat_UAV = [0
0.27635215014234993
0.830832528031385
0.5399784556870071
0.20813494084995976
5.0668943280579155
0.8092716762364984
    ]'; % delta msg 0.7

msg085_lat_rel = [
    0
    0.7542142786878703
0.12858654435679595
0.3260137495171845
2.7205145745444343
0.2674760518343444
0.1548486783431268
    ]'; % delta msg0.85

msg085_lat_UAV = [0
2.360476870178602
0.5303182750028131
0.3670504644633831
2.2129530135960995
0.23320998811748533
1.072972409343259
    ]'; % delta msg 0.85

msg1_lat_rel = [
    0
    4.284876676384459
0.21829508650341095
0.10323090839697048
0.3579282238969508
0.28909971116718686
2.0857076763496707
    ]'; % delta msg1

msg1_lat_UAV = [0
5.608281631384526
0.7008878438800115
0.17735794491550871
1.4448830041076153
0.22606010594236886
0.7028679130512505
    ]'; % delta msg 1

msg2_lat_rel = [
    0
0.29617786192575735
0.40077779967706484
0.3130378867056918
0.44186493258270054
5.02161384130459
0.232472204719663
    ]'; % delta msg2

msg2_lat_UAV = [0
0.21763258436629834
0.21150105725323204
0.15228821131267592
0.19788409917012323
0.8874504117865964
0.30915831268604044
    ]'; % delta msg 2

msg4_lat_rel = [
    0
     0.29507248672716563
0.3717899152699743
0.14699363621624748
0.20466122759976585
0.6783183388210616
0.11931284987877333
    ]'; % delta msg4

msg4_lat_UAV = [0
0.22576841900288463
0.44842319273221004
0.17659141011577764
0.18917868907964847
0.48452272239194194
0.20677704090814764
    ]'; % delta msg 4

lambda = [0 1/4 1/2 1 1/.85 1/0.7 1/0.5 1/0.35 1/.25 1/0.15 1/0.1];% 12.5]; % I valori di lambda corrispondenti

% Numero di esperimenti
n_esperimenti = size(msg01_lat_UAV', 1);
conf = 0.5;
alpha = 1-conf;
pLo = alpha/2;
pUp = 1-alpha/2;
ts = tinv(conf, n_esperimenti-1);

% Calcola le medie dei punti per ogni valore di lambda
av4_rel = mean(msg4_lat_rel, 2);
av2_rel = mean(msg2_lat_rel, 2);
av1_rel = mean(msg1_lat_rel, 2);
av085_rel = mean(msg085_lat_rel, 2);
av07_rel = mean(msg07_lat_rel, 2);
av05_rel = mean(msg05_lat_rel, 2);
av035_rel = mean(msg035_lat_rel, 2);
av025_rel = mean(msg025_lat_rel, 2);
av015_rel = mean(msg015_lat_rel, 2);
av01_rel = mean(msg01_lat_rel, 2);

av_rel=[0,av4_rel, av2_rel, av1_rel, av085_rel, av07_rel, av05_rel, av035_rel, av025_rel, av015_rel, av01_rel]

% Calcola la deviazione standard dei punti per ogni valore di lambda
dv4_rel = std(msg4_lat_rel,0, 2);
dv2_rel = std(msg2_lat_rel,0, 2);
dv1_rel = std(msg1_lat_rel, 0,2);
dv085_rel = std(msg085_lat_rel, 0,2);
dv07_rel = std(msg07_lat_rel, 0,2);
dv05_rel = std(msg05_lat_rel,0, 2);
dv035_rel = std(msg035_lat_rel,0, 2);
dv025_rel = std(msg025_lat_rel, 0, 2);
dv015_rel = std(msg015_lat_rel,0, 2);
dv01_rel = std(msg01_lat_rel,0, 2);

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


av4_UAV = mean(msg4_lat_UAV, 2);
av2_UAV = mean(msg2_lat_UAV, 2);
av1_UAV = mean(msg1_lat_UAV, 2);
av085_UAV = mean(msg085_lat_UAV, 2);
av07_UAV = mean(msg07_lat_UAV, 2);
av05_UAV = mean(msg05_lat_UAV, 2);
av035_UAV = mean(msg035_lat_UAV, 2);
av025_UAV = mean(msg025_lat_UAV, 2);
av015_UAV = mean(msg015_lat_UAV, 2);
av01_UAV = mean(msg01_lat_UAV, 2);

av_UAV=[0, av4_UAV, av2_UAV, av1_UAV, av085_UAV, av07_UAV, av05_UAV, av035_UAV, av025_UAV, av015_UAV, av01_UAV]

% Calcola la deviazione standard dei punti per ogni valore di lambda
dv4_UAV = std(msg4_lat_UAV,0, 2);
dv2_UAV = std(msg2_lat_UAV,0, 2);
dv1_UAV = std(msg1_lat_UAV, 0,2);
dv085_UAV = std(msg085_lat_UAV,0, 2);
dv07_UAV = std(msg07_lat_UAV,0, 2);
dv05_UAV = std(msg05_lat_UAV,0, 2);
dv035_UAV = std(msg035_lat_UAV,0, 2);
dv025_UAV = std(msg025_lat_UAV, 0, 2);
dv015_UAV = std(msg015_lat_UAV,0, 2);
dv01_UAV = std(msg01_lat_UAV,0, 2);

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
%errorbar(lambda, av, CI_tot, 'r-', 'LineWidth', 0.75);
%line(lambda, av, 'Color', Blu_p, 'Marker', '.', 'MarkerSize', 20,'LineStyle', '-', 'LineWidth', 2);
line(lambda, av_rel, 'Color', Verde_p, 'Marker', '.', 'MarkerSize', 20,'LineStyle', '-', 'LineWidth', 2);
errorbar(lambda, av_rel, CI_rel, 'Color', Verde_p, 'LineStyle', '-', 'LineWidth', 1);

line(lambda, av_UAV, 'Color', Rosa_p, 'Marker', '.','MarkerSize', 20, 'LineStyle', '-', 'LineWidth', 2);
errorbar(lambda, av_UAV, CI_UAV,'Color', Rosa_p, 'LineStyle', '-', 'LineWidth', 1);

xlabel('Generation Rate [s^{-1}]', 'Interpreter', 'tex', 'FontSize', 12);
ylabel('Latency [s]', 'Interpreter', 'tex', 'FontSize', 12);

xticks(lambda);
xtickangle(90)
%ylim([-1; 100])
set(gca,'FontSize',14)

% Mostra la legenda
legend( 'Latency Relay','Confidence interval lat_{Relay}', 'Latency UAVs', 'Confidence interval lat_{UAV}');

% Imposta le dimensioni desiderate per l'immagine rettangolare
larghezza = 2600; % Larghezza desiderata dell'immagine in pixel
altezza = 1800; % Altezza desiderata dell'immagine in pixel
set(gcf, 'PaperPosition', [0 0 larghezza/100 altezza/100]);


% Salva l'immagine in formato rettangolare (ad esempio, PNG)
nome_file = 'latency without miss';
formato_file = 'png';
saveas(gcf, nome_file, formato_file);