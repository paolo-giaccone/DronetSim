close all
clear all
clc
% Dati dei valori
msg01_thr_tot = [0
    35578.2981572671
51352.57959679605
37792.50684721668
 42012.213164562374 
34815.82426014332
33783.88522252206]' /1e3

msg01_thr_rel = [0
 4985.64841313509
6611.597665717706
7128.73098471867
6765.552923257109
6620.35730917026
5426.823191853091
    ]'/1e3; % delta msg 0.1

msg01_thr_UAV = [0
 30592.64974413201
44740.98193107834
30663.775862498012
35246.66024130526
28195.466950973067
28357.062030668967
    ]'/1e3; % delta msg 0.1

msg015_thr_tot = [0
    35771.88067292953
34492.79108570027
48311.8132313245
45511.73322713786
42258.88082122567
37789.16953643919
    ]'/1e3; % delta msg 0.15

msg015_thr_rel = [0,
    4600.939564482156
4814.450465357696
6599.923183369826
9666.716986785612
6663.933212784528
7360.231629548723
    ]'/1e3; % delta msg 0.15

msg015_thr_UAV = [0
    31170.941108447376
29678.340620342573
41711.89004795467
35845.01624035225
35594.94760844114
30428.93790689047
    ]'/1e3; % delta msg 0.15


msg025_thr_tot = [0
    30133.45690673828
29813.11288425919
37175.61059097585
42735.657881054016
32383.86357709776
26049.64762988181
    ]'/1e3; % delta msg 0.25

msg025_thr_rel = [0
    4835.605415777258
5353.763229215559
8142.424928833469
15120.800059606629
6905.946190119979
7372.883578137619
    ]'/1e3; % delta msg 0.25

msg025_thr_UAV = [0
    25297.851490961024
24459.349655043632
29033.18566214238
27614.857821447386
25477.917386977777
18676.76405174419
    ]'/1e3; % delta msg 0.25

msg035_thr_tot = [0
    24213.414018867184
29891.995475882333
28871.16319421028
24900.716201079584
26189.884900142217
38385.731895712845
    ]'/1e3; % delta msg 0.35

msg035_thr_rel = [0
    5919.776877467353
8645.050134492945
7788.064364004247
7766.199382234199
5591.370990695797
16817.656970838583
    ]'/1e3; % delta msg 0.35

msg035_thr_UAV = [0
    18293.63714139983
21246.945341389386
21083.098830206032
17134.516818845383
20598.51390944642
21568.07492487426
    ]'/1e3; % delta msg 0.35

msg05_thr_tot = [0
    20761.196322238528
19512.217311176308
21557.37777355138
21301.072203446507
19090.44920674383
38504.781872103515
    ]'/1e3; % delta msg 0.5

msg05_thr_rel = [0
    5075.496190535612
7206.986515542986
5646.871762576665
4829.943717188668
7276.425952381053
16869.603938642198
    ]'/1e3; % delta msg 0.5

msg05_thr_UAV = [0
    15685.700131702915
12305.230795633324
15910.506010974716
16471.128486257836
11814.023254362777
21635.177933461317
    ]'/1e3; % delta msg 0.5

msg07_thr_tot = [0
    15431.590581998275
15506.472863642677
15583.354530887495
16000.828427968847
14733.6415513555
37509.88591876521
    ]'/1e3; % delta msg 0.7

msg07_thr_rel = [0
    3807.5859912807427
4140.667557922668
4762.990554228914
4221.025333705158
5666.091178353493
22154.83734740847
    ]'/1e3; % delta msg 0.7

msg07_thr_UAV = [0
    11624.004590717532
11365.805305720009
10820.363976658582
11779.80309426369
9067.550373002006
15355.048571356747
    ]'/1e3; % delta msg 0.7

msg085_thr_rel = [0
   3744.2434670115463
3549.330128937293
3485.2305951644657
4264.779223853023
2904.2313801599666
18496.70074074159
    ]'/1e3; % delta msg 0.85

msg085_thr_tot = [0
     12500.53292936812
13085.819764845124
13306.475063576952
12127.12062596684
12920.209408689492
33720.71074162039
    ]'/1e3; % delta msg 0.85

msg085_thr_UAV = [0
     8756.289462356573
9536.489635907832
9821.244468412488
7862.341402113818
10015.978028529526
15224.010000878792
    ]'/1e3; % delta msg 0.85


msg1_thr_tot = [0
    10208.132512337394
11407.188890950065
9944.771173955955
10754.393636019217
11093.750590069663
22208.419291007074
    ]'/1e3; % delta msg 1

msg1_thr_rel = [0
    3396.704286982522
2567.8887325095616
2388.237730330886
2986.8614897834645
2426.004835771932
10226.342781660493
    ]'/1e3; % delta msg 1

msg1_thr_UAV = [0
    6811.428225354872
8839.300158440505
7556.533443625069
7767.5321462357515
8667.74575429773
11982.076509346582
    ]'/1e3; % delta msg 1


msg2_thr_tot = [0
    5673.781291457275
5515.665118724455
5482.781062724959
5548.403810517914
5501.733179272954
18694.23190799726
    ]'/1e3; % delta msg 2

msg2_thr_rel = [0
     1422.4409434921056
1569.9077278561235
1768.9378090886269
1582.852680390543
1777.6197671318105
7559.702829894658
    ]'/1e3; % delta msg 2

msg2_thr_UAV = [0
    4251.34034796517
3945.757390868332
3713.843253636332
3965.551130127371
3724.1134121411433
11134.5290781026
    ]'/1e3; % delta msg 2

msg4_thr_tot = [0
    2747.1026651578413
2611.6393802446323
2839.4570816856735
2846.9458916191493
2723.8068913837797
23056.903023341674
    ]'/1e3; % delta msg 4

msg4_thr_rel = [0
    725.7970109649979
680.2018964624283
703.016705111887
680.9697665832547
696.3778136547528
13758.133947983755
    ]'/1e3; % delta msg 4

msg4_thr_UAV = [0
     2021.3056541928436
1931.437483782204
2136.4403765737866
2165.9761250358947
2027.429077729027
9298.769075357919
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
%errorbar(lambda, av, CI_tot, 'r-', 'LineWidth', 0.75);
line(lambda, av, 'Color', Blu_p, 'Marker', '.', 'MarkerSize', 25,'LineStyle', '-', 'LineWidth', 2.5);
%errorbar(lambda, av_UAV, CI_UAV, 'g-', 'LineWidth', 0.75);
line(lambda, av_UAV, 'Color', Rosa_p, 'Marker', '.','MarkerSize', 25, 'LineStyle', '-', 'LineWidth', 2.5);
line(lambda, av_rel, 'Color', Verde_p, 'Marker', '.', 'MarkerSize', 25,'LineStyle', '-', 'LineWidth', 2.5);
errorbar(lambda, av_rel, CI_rel, 'Color', Verde_p, 'LineStyle', '-', 'LineWidth', 1);
%line(get(gca,'XLim'), [100 100], 'Color', [0.5 0.5 0.5], 'LineStyle', '-', 'LineWidth', 1.5);

ylim([-1; 55])
xlabel('Generation Rate [s^{-1}]', 'Interpreter', 'tex', 'FontSize', 16);
ylabel('Throughput [kbps]', 'Interpreter', 'tex', 'FontSize', 16);

xticks(lambda);
xtickangle(90)

set(gca,'FontSize',16)

% Mostra la legenda
legend('Throughput TOT', ... %'Confidence interval Th_{TOT}',
    'Throughput UAVs', ... %'Confidence interval Th_{UAV}',
    'Throughput Relay','Confidence interval Th_{Relay}', 'Max Datarate', 'FontSize', 16);

% Imposta le dimensioni desiderate per l'immagine rettangolare
larghezza = 4600; % Larghezza desiderata dell'immagine in pixel
altezza = 2400; % Altezza desiderata dell'immagine in pixel
set(gcf, 'PaperPosition', [0 0 larghezza/100 altezza/100]);

% Salva l'immagine in formato rettangolare (ad esempio, PNG)
nome_file = 'throughput without miss pers';
formato_file = 'png';
saveas(gcf, nome_file, formato_file);