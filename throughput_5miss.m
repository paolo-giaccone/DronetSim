close all
clear all
clc
% Dati dei valori
msg01_thr_tot = [0
    29009.89691331013
    38776.57828393183
    33630.38486677065
    42012.213164562374
    44078.2884150348
    43347.28345724566]' /1e3

msg01_thr_rel = [0
    4968.545880180188
    4415.815218644715
    5157.08495383539
    6765.552923257109
    8303.62230214904
    8094.691010001178
    ]'/1e3; % delta msg 0.1

msg01_thr_UAV = [0
    24041.351033129944
    34360.763065287116
    28473.29991293526
    35246.66024130526
    35774.66611288577
    35252.59244724449
    ]'/1e3; % delta msg 0.1


msg015_thr_tot = [0
    28813.460211171227
    35490.705221677905
    40802.2946619706
    45511.73322713786
    43769.287175193516
    36491.59279064229
    ]'/1e3; % delta msg 0.15

msg015_thr_rel = [0,
    4418.1060595778135
    4696.483918677829
    4218.432853866632
    9666.716986785612
    11701.348105974204
    4927.064410251307
    ]'/1e3; % delta msg 0.15

msg015_thr_UAV = [0
    24395.354151593412
    30794.221303000075
    28473.29991293526
    36583.86180810397
    35845.01624035225
    32067.939069219312
    ]'/1e3; % delta msg 0.15


msg025_thr_tot = [0
    29457.268720772827
    32475.40906608726
    31765.21385450766
    48437.38330063844
    42735.657881054016
    33746.03479635316
    ]'/1e3; % delta msg 0.25

msg025_thr_rel = [0
    10801.103325744523
    8589.575738332565
    5771.203026522033
    10815.513124593885
    15120.800059606629
    10865.810416398088
    ]'/1e3; % delta msg 0.25

msg025_thr_UAV = [0
    18656.165395028303
    23885.833327754695
    25994.010827985625
    37621.870176044555
    27614.857821447386
    9428.351687842096
    ]'/1e3; % delta msg 0.25

msg035_thr_tot = [0
    29786.759217697574
    27901.06049217962
    29448.74772870057
    38385.731895712845
    35291.8225346781
    36612.18131183926
    ]'/1e3; % delta msg 0.35

msg035_thr_rel = [0
    10640.73066964704
    9056.137748695503
    10099.18699794747
    16817.656970838583
    12474.120971473309
    15400.574908505498
    ]'/1e3; % delta msg 0.35

msg035_thr_UAV = [0
    19146.028548050534
    18844.922743484116
    19349.5607307531
    21568.07492487426
    22817.70156320479
    21211.606403333757
    ]'/1e3; % delta msg 0.35

msg05_thr_tot = [0
    26297.626194301778
    32865.02059932965
    30299.313249500363
    38504.781872103515
    36172.866158016266
    24760.494195405794
    ]'/1e3; % delta msg 0.5

msg05_thr_rel = [0
    12159.608236011007
    14020.592957822151
    11765.717404639441
    16869.603938642198
    23020.74607617565
    11613.08778223523
    ]'/1e3; % delta msg 0.5

msg05_thr_UAV = [0
    14138.017958290771
    18844.4276415075
    18533.595844860924
    21635.177933461317
    13152.120081840616
    13147.406413170564
    ]'/1e3; % delta msg 0.5

msg07_thr_tot = [0
    25251.118763936724
    26402.431139809167
    23717.668549895854
    37509.885918765205
    21422.08433921752
    24038.436378290127
    ]'/1e3; % delta msg 0.7

msg07_thr_rel = [0
    9027.870284646271
    15847.695886949761
    14868.800462628575
    22154.837347408466
    6504.140966333005
    13253.605709728332
    ]'/1e3; % delta msg 0.7

msg07_thr_UAV = [0
    16223.248479290454
    10554.735252859406
    8848.868087267278
    15355.048571356743
    14917.943372884512
    10784.830668561795
    ]'/1e3; % delta msg 0.7

msg085_thr_tot = [0
    21422.536261534326
    20634.446052138577
    23660.661013273475
    33720.71074162039
    18518.114839974376
    21064.505708060267
    ]'/1e3; % delta msg 0.85

msg085_thr_rel = [0
    14398.52506472204
    11342.989266634228
    12842.635581404154
    18496.70074074159
    8652.702277613591
    9830.61413650528
    ]'/1e3; % delta msg 0.85

msg085_thr_UAV = [0
    7024.011196812287
    9291.45678550435
    10818.02543186932
    15224.010000878792
    9865.412562360785
    11233.891571554985
    ]'/1e3; % delta msg 0.85


msg1_thr_tot = [0
    19206.489368985105
    22208.419291007074
    23679.17299623498
    25698.87376581857
    20267.55514067347
    28746.434193893754
    ]'/1e3; % delta msg 1

msg1_thr_rel = [0
    9610.498568084213
    10226.342781660493
    11065.088511181833
    9244.635806971546
    7515.556544051909
    16902.182856276944
    ]'/1e3; % delta msg 1

msg1_thr_UAV = [0
    9595.990800900892
    11982.076509346582
    12614.084485053147
    16454.237958847025
    12751.998596621563
    11844.25133761681
    ]'/1e3; % delta msg 1


msg2_thr_tot = [0
    14679.542509011379
    11529.630764663238
    16600.64061123127
    9537.045179792522
    10817.439338310704
    18694.23190799726
    ]'/1e3; % delta msg 2

msg2_thr_rel = [0
    11155.587377757187
    7106.518164074665
    11047.99606872374
    2969.864900567148
    5354.656797390983
    7559.702829894658
    ]'/1e3; % delta msg 2

msg2_thr_UAV = [0
    3523.955131254191
    4423.112600588573
    5552.644542507527
    6567.180279225373
    5462.782540919719
    11134.5290781026
    ]'/1e3; % delta msg 2

msg4_thr_tot = [0
    11437.703242206551
    11551.205162978933
    12643.651237944581
    23056.903023341674
    10153.443974482041
    16567.70793653817
    ]'/1e3; % delta msg 4

msg4_thr_rel = [0
    9715.372797422264
    7968.006250544416
    10063.657436992966
    13758.133947983755
    5670.802585793137
    7932.53847325918
    ]'/1e3; % delta msg 4

msg4_thr_UAV = [0
    1722.3304447842872
    3583.1989124345178
    2579.993800951616
    9298.769075357919
    4482.641388688905
    8635.169463278988
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
line(lambda, av, 'Color', Blu_p, 'Marker', '.', 'MarkerSize', 20,'LineStyle', '-', 'LineWidth', 2);
%errorbar(lambda, av_UAV, CI_UAV, 'g-', 'LineWidth', 0.75);
line(lambda, av_UAV, 'Color', Rosa_p, 'Marker', '.','MarkerSize', 20, 'LineStyle', '-', 'LineWidth', 2);
line(lambda, av_rel, 'Color', Verde_p, 'Marker', '.', 'MarkerSize', 20,'LineStyle', '-', 'LineWidth', 2);
errorbar(lambda, av_rel, CI_rel, 'Color', Verde_p, 'LineStyle', '-', 'LineWidth', 1);
%line(get(gca,'XLim'), [100 100], 'Color', [0.5 0.5 0.5], 'LineStyle', '-', 'LineWidth', 1.5);

ylim([-1; 110])
xlabel('Generation Rate [s^{-1}]', 'Interpreter', 'tex', 'FontSize', 12);
ylabel('Throughput [kbps]', 'Interpreter', 'tex', 'FontSize', 12);

xticks(lambda);
xtickangle(90)

ylim([-1; 55])
set(gca,'FontSize',16)


% Mostra la legenda
legend('Throughput TOT', ... %'Confidence interval Th_{TOT}',
    'Throughput UAVs', ... %'Confidence interval Th_{UAV}',
    'Throughput Relay','Confidence interval Th_{Relay}', 'Max Datarate');

% Imposta le dimensioni desiderate per l'immagine rettangolare
larghezza = 4600; % Larghezza desiderata dell'immagine in pixel
altezza = 2400; % Altezza desiderata dell'immagine in pixel
set(gcf, 'PaperPosition', [0 0 larghezza/100 altezza/100]);

% Salva l'immagine in formato rettangolare (ad esempio, PNG)
nome_file = 'throughput with miss pers';
formato_file = 'png';
saveas(gcf, nome_file, formato_file);