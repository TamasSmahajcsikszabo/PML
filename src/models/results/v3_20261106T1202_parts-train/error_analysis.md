# oof

# Error analysis (8651 URLs, threshold 0.845)

TP 2836  FP 44  FN 1494  TN 4277  | recall 0.655  FPR 0.0102  precision 0.985  accuracy 0.822

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http 5315      2898    0.326   2417    0.013
        scheme       https 3336      1432    0.383   1904    0.007
      has path     no path 2498       851    0.617   1647    0.004
      has path        path 6153      3479    0.279   2674    0.014
        length       26-40 2454      1063    0.584   1391    0.008
        length       41-70 3057      1475    0.361   1582    0.011
        length      71-120 1516       886    0.141    630    0.013
        length        <=25  898       236    0.614    662    0.002
        length        >120  726       670    0.106     56    0.125
popular domain not popular 6390      3764    0.317   2626    0.014
popular domain     popular 2261       566    0.532   1695    0.004
           www      no www 4903      3427    0.303   1476    0.025
           www         www 3748       903    0.503   2845    0.002
           tld          au   98        55    0.200     43    0.000
           tld         com 5260      2531    0.345   2729    0.009
           tld         net  290       161    0.429    129    0.016
           tld         org  492        75    0.347    417    0.007
           tld       other 2142      1334    0.343    808    0.017
           tld          ru  226       120    0.358    106    0.009
           tld          uk  143        54    0.259     89    0.000

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          url_len -0.880        3.785         4.287
longest_digit_run -0.859        0.441         1.139
          ent_url -0.846        4.004         4.409
   url_digit_rate -0.819        0.030         0.114
         url_leet -0.758        0.014         0.055
 ratio_delims_url  0.733        0.026         0.019
         path_len -0.729        1.912         2.917
         ent_path -0.714        2.189         3.270
      max_seg_len -0.697        1.576         2.387
            n_seg -0.695        0.720         1.140

## Features that separate false positives vs correct clean (Cohen's d)

        feature     d  mean_errors  mean_correct
sc_delims_query 3.962        0.126         0.000
  qval_max_typo 3.646        0.121         0.000
 rep_char_query 3.492        0.159         0.001
        emb_hex 3.240        0.227         0.003
        n_pairs 2.995        0.543         0.026
   max_qkey_len 2.920        0.917         0.044
       n_eq_url 2.919        0.552         0.029
      query_len 2.881        1.713         0.089
      n_amp_url 2.824        0.343         0.007
   max_qval_len 2.764        1.299         0.065

## false negatives (phishing scored lowest)

    p                                                                                                  url
0.042                                                  http://www.calculator.net/ip-subnet-calculator.html
0.045                                               http://www.wikiwand.com/en/Select_or_special_committee
0.046                                                  http://www.infobarrel.com/Digital_Cameras_with_WiFi
0.048 https://www.quora.com/Why-is-the-longest-path-problem-NP-complete-given-that-the-shortest-path-probl
0.052                                                                              http://www.nbcnews.com/
0.053                                                                        https://www.directrelief.org/
0.055                                                      https://www.wisegeek.com/what-is-a-form-w-9.htm
0.056                                       https://www.consumeraffairs.com/internet/internet_services.htm
0.059 https://bytes.com/topic/computer-hardware/answers/903158-what-some-good-open-source-software-hardwar
0.060                                                              https://www.facebook.com/mimosanetworks

## false positives (clean scored highest)

    p                                                                                                  url
0.958 https://support-appleld.com.secureupdate.duilawyeryork.com/ap/ce9f83cca53de77/?cmd=_update&dispatch=
0.955 http://secureupdate.appleld.com.duilawyeryork.com/ap/9330524a3db85de?cmd=_update&dispatch=9330524a3d
0.951                                         https://urbanmeisters.ovh/wp-admin/css/colors/blue/sparka/DE
0.943                                  http://giaanhvu.com.vn/wp-content/languages/plugins/Cladoselachidae
0.940 https://login.microsoftonline.com/abe32f68-c72d-420d-b5bd-750c63a268e4/oauth2/authorize?client_id=00
0.939 https://login.microsoftonline.com/decee90c-ce03-461e-8c21-dd538e181c75/oauth2/authorize?client_id=00
0.936 https://login.microsoftonline.com/dc046083-4ce8-437a-bd49-e995b65e4d11/oauth2/authorize?client_id=00
0.935 https://login.microsoftonline.com/aa687de1-52b4-4b91-9b35-794eba4fd892/oauth2/authorize?client_id=00
0.933                             http://ww4.farmoyunlari.com/?subid1=4ae712f2-9a35-11e8-a4de-44a7c1746edf
0.931           https://www.miairsoft.org/index.php?PHPSESSID=bdf0358a8eef04e44dc5ad4d41be389d;wwwRedirect


# test

# Error analysis (2858 URLs, threshold 0.845)

TP 1005  FP 14  FN 424  TN 1415  | recall 0.703  FPR 0.0098  precision 0.986  accuracy 0.847

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http 1713       937    0.313    776    0.017
        scheme       https 1145       492    0.266    653    0.002
      has path     no path  871       296    0.537    575    0.003
      has path        path 1987      1133    0.234    854    0.014
        length       26-40  835       337    0.582    498    0.016
        length       41-70 1036       533    0.291    503    0.010
        length      71-120  461       271    0.074    190    0.005
        length        <=25  296        69    0.623    227    0.000
        length        >120  230       219    0.046     11      NaN
popular domain not popular 2108      1211    0.300    897    0.016
popular domain     popular  750       218    0.280    532    0.000
           www      no www 1583      1131    0.258    452    0.029
           www         www 1275       298    0.443    977    0.001
           tld         com 1791       873    0.277    918    0.008
           tld          de   42         9      NaN     33    0.000
           tld         net   91        59    0.373     32    0.062
           tld         org  156        24    0.417    132    0.000
           tld       other  660       410    0.322    250    0.020
           tld          ru   68        33    0.333     35    0.000
           tld          uk   50        21    0.238     29    0.000

## Features that separate false negatives vs caught phishing (Cohen's d)

           feature      d  mean_errors  mean_correct
           ent_url -1.119        3.910         4.416
           url_len -1.048        3.713         4.264
 longest_digit_run -1.037        0.313         1.120
    url_digit_rate -0.848        0.022         0.104
  ratio_delims_url  0.839        0.028         0.019
          url_leet -0.812        0.009         0.050
          path_len -0.764        1.802         2.864
ratio_nonalnum_url  0.752        0.196         0.163
          ent_path -0.749        2.063         3.211
       max_seg_len -0.739        1.484         2.339

## Features that separate false positives vs correct clean (Cohen's d)

            feature      d  mean_errors  mean_correct
              n_sub -1.775        0.149         0.600
        n_dots_host -1.680        0.838         1.078
      sc_other_host -1.680        0.838         1.078
       brand_in_reg  1.546        0.071         0.001
       max_qkey_len  1.529        0.486         0.045
qval_min_legibility -1.484        0.786         0.983
          has_query  1.445        0.286         0.030
            n_pairs  1.379        0.227         0.024
     sw_phrase_path  1.350        0.128         0.010
                www -1.340        0.071         0.690

## false negatives (phishing scored lowest)

    p                                     url
0.073       http://www.geocities.ws/steamcom/
0.075 http://feeds.feedburner.com/investorway
0.085        https://stateagencybe.tumblr.com
0.093 https://artekcamp.tumblr.com/icampi#_=_
0.098            https://seetflix.tumblr.com/
0.099            https://www.perfectliker.net
0.099           https://www.officialliker.co/
0.118                    http://www.dalla.eu/
0.122       http://www.automoves-halifax.com/
0.123           https://netflxius.tumblr.com/

## false positives (clean scored highest)

    p                                                                                               url
0.931                                                                        http://back.dog/auth/login
0.894                                                   http://termolak.bayhamconsulting.com/t/OOFJCi01
0.891 http://bectechnologies.net/wordpress/wp-content/uploads/2015/08/BEC_8920NE_QSG_v1.0_2014_0711.pdf
0.886                                                                http://isp1.us/state/new-york/nyc/
0.885                                                                      http://bagru.info/t/BySXSWap
0.884                                    https://freemeteo.ro/vremea/?language=romanian&country=romania
0.882                                                                     http://cyb-sys.com/jietg/Upue
0.880                                                            http://eudesign.com/mnems/portstar.htm
0.877                                    http://clioadams.azurewebsites.net/Account/Login?ReturnUrl=%2F
0.874                                                          http://isp1.us/state/washington/seattle/


# external_test

# Error analysis (2858 URLs, threshold 0.845)

TP 601  FP 0  FN 828  TN 1429  | recall 0.421  FPR 0.0000  precision 1.000  accuracy 0.710

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http  750       750    0.803      0      NaN
        scheme       https 2108       679    0.333   1429      0.0
      has path     no path 2458      1029    0.713   1429      0.0
      has path        path  400       400    0.235      0      NaN
        length       26-40 1456       571    0.723    885      0.0
        length       41-70  386       370    0.268     16      0.0
        length      71-120  142       142    0.141      0      NaN
        length        <=25  835       307    0.954    528      0.0
        length        >120   39        39    0.077      0      NaN
popular domain not popular 2602      1271    0.589   1331      0.0
popular domain     popular  256       158    0.506     98      0.0
           www      no www  833       833    0.355      0      NaN
           www         www 2025       596    0.893   1429      0.0
           tld         app   88        87    0.575      1      NaN
           tld          co   68        59    0.322      9      NaN
           tld         com 1367       628    0.646    739      0.0
           tld          io   77        70    0.300      7      NaN
           tld         net   98        58    0.603     40      0.0
           tld         org  189        27    1.000    162      0.0
           tld       other  971       500    0.540    471      0.0

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          ent_url -1.714        3.579         4.263
 ratio_delims_url  1.565        0.035         0.021
          url_len -1.450        3.431         4.020
longest_digit_run -1.308        0.301         1.209
              www  1.287        0.643         0.106
  ratio_other_url  1.165        0.109         0.075
            https -1.094        0.273         0.754
   url_digit_rate -1.034        0.027         0.113
         has_path -0.978        0.114         0.509
    ent_path_norm -0.971        0.094         0.422

## Features that separate false positives vs correct clean (Cohen's d)

(too few errors)

## false negatives (phishing scored lowest)

    p                              url
0.058          http://www.coinhive.com
0.060         http://www.bearsmyip.com
0.063      http://www.simplemining.net
0.064   http://www.medianewsonline.com
0.079        http://www.cshack.ucoz.ru
0.080           http://www.salas.co.uk
0.085           http://www.gila.com.br
0.088   https://www.bitmart-trust.net/
0.089            http://www.gab.com.tr
0.090 http://www.moneysavingreport.com

## false positives (clean scored highest)

(none)
