close all
clear all
clc
% Dati dei valori

msg01_lat_rel = [
    0
    47.561535619502195
    70.2883325832359
    61.860177679804785
    59.767083103912206
    50.20535816005327
    58.1210943835999
    ]'; % delta msg0.1

msg01_lat_UAV = [0
    38.18007450405241
    27.67274171383584
    31.840483293642976
    29.061500173093336
    30.3320550452363
    30.801815940244833
    ]'; % delta msg 0.1

msg015_lat_rel = [
    0
    39.976222281619506
53.152335719728214
64.08003254193416
34.96795605411895
39.90966454382001 
56.83155695725546
    ]'; % delta msg0.15

msg015_lat_UAV = [0
27.79509677955849
18.423949506742737
13.321727256611892
9.029137921753554
30.3320550452363
11.064899192096368
    ]'; % delta msg 0.15

msg025_lat_rel = [
    0
    14.940957265164657
32.78714562643958
35.90530038970007
33.75684515366839
18.123002152707155
36.7435529915857
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
    11.05836646413736
28.89001838626321
11.679792145316393
13.558797751653492
11.228382976095999
24.531977908959497
    ]'; % delta msg0.35

msg035_lat_UAV = [0
5.015547339735891
0.790333058032647
1.1645303368344462
4.17166949029208
1.0247280764479603
2.0698458734386684
    ]'; % delta msg 0.35

msg05_lat_rel = [
    0
    0.8691037267697088
2.905218813956289
10.752049775005094
5.003505552333971
4.748496439360599
16.48312409687731
    ]'; % delta msg0.5

msg05_lat_UAV = [0
3.564951003867943
0.42716796057304585
0.6412782341548618
1.9096832300316506
0.64241422690188
3.2117888869437
    ]'; % delta msg 0.5

msg07_lat_rel = [
    0
    2.1248931951719965
1.5869333509413588
0.7647248853981748
2.2569899869090397
3.179617931579122
4.885464825990733
    ]'; % delta msg0.7

msg07_lat_UAV = [0
0.8908448175574701
1.6439354412517009
2.6834791303450927
0.8092716762364991
0.781671910863182
2.4974170051962448
    ]'; % delta msg 0.7

msg085_lat_rel = [
    0
    0.3249528055129598
0.7274042745955205
0.43692940809215347
0.1548486783431268
0.20362463061852312
1.0185551425042692
    ]'; % delta msg0.85

msg085_lat_UAV = [0
1.1655628990034692
0.20698336338523501
0.2785902291188754
1.072972409343259
0.38657496424570914
2.2160830468301085
    ]'; % delta msg 0.85

msg1_lat_rel = [
    0
    0.976200920307498
2.0857076763496707
0.9703956851372723
0.22389680823744085
8.444616336045398
0.5718559323749465
    ]'; % delta msg1

msg1_lat_UAV = [0
0.38670551455528224
0.7028679130512505
0.2593293654222786
0.49137970335184916
1.0826045605140784
0.20809574345715093
    ]'; % delta msg 1

msg2_lat_rel = [
    0
0.17235936291373122
0.7303130290737379
0.2707055030227694
0.15748945521238786
0.5200146452968597
0.232472204719663
    ]'; % delta msg2

msg2_lat_UAV = [0
0.3177996027920851
0.2529905866431153
0.5300882435220543
0.6965196448174542
0.1808369349228759
0.30915831268604044
    ]'; % delta msg 2

msg4_lat_rel = [
    0
    0.13666899218108466
0.11362181445112896
0.21430031560174329
0.11931284987877333
0.11340439183330198
0.170028754432775
    ]'; % delta msg4

msg4_lat_UAV = [0
0.33903923887056225
0.2299302247399755
0.2885761439642742
0.20677704090814764
0.1419490080949888
0.27066647664218485
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
legend( 'Latency Relay','Confidence interval lat_{Relay}', 'Latency UAVs', 'Confidence interval lat_{UAV}', 'Location','northwest');

% Imposta le dimensioni desiderate per l'immagine rettangolare
larghezza = 2600; % Larghezza desiderata dell'immagine in pixel
altezza = 1800; % Altezza desiderata dell'immagine in pixel
set(gcf, 'PaperPosition', [0 0 larghezza/100 altezza/100]);

% Salva l'immagine in formato rettangolare (ad esempio, PNG)
nome_file = 'latency with miss';
formato_file = 'png';
saveas(gcf, nome_file, formato_file);