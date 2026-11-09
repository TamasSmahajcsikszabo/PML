# oof

# Error analysis (8651 URLs, threshold 0.846)

TP 2827  FP 44  FN 1503  TN 4277  | recall 0.653  FPR 0.0102  precision 0.985  accuracy 0.821

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http 5315      2898    0.327   2417    0.013
        scheme       https 3336      1432    0.387   1904    0.007
      has path     no path 2498       851    0.620   1647    0.004
      has path        path 6153      3479    0.280   2674    0.014
        length       26-40 2454      1063    0.584   1391    0.006
        length       41-70 3057      1475    0.361   1582    0.012
        length      71-120 1516       886    0.153    630    0.013
        length        <=25  898       236    0.614    662    0.002
        length        >120  726       670    0.101     56    0.125
popular domain not popular 6386      3760    0.319   2626    0.014
popular domain     popular 2265       570    0.535   1695    0.005
           www      no www 4903      3427    0.307   1476    0.025
           www         www 3748       903    0.499   2845    0.002
           tld          au   98        55    0.145     43    0.000
           tld         com 5260      2531    0.350   2729    0.009
           tld         net  290       161    0.447    129    0.016
           tld         org  492        75    0.333    417    0.007
           tld       other 2142      1334    0.343    808    0.016
           tld          ru  226       120    0.358    106    0.009
           tld          uk  143        54    0.241     89    0.000

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          url_len -0.880        3.787         4.288
longest_digit_run -0.867        0.439         1.142
          ent_url -0.844        4.005         4.409
   url_digit_rate -0.823        0.030         0.114
         url_leet -0.764        0.013         0.055
         path_len -0.725        1.917         2.917
 ratio_delims_url  0.721        0.026         0.019
         ent_path -0.711        2.193         3.271
      max_seg_len -0.689        1.583         2.386
            n_seg -0.689        0.723         1.140

## Features that separate false positives vs correct clean (Cohen's d)

        feature     d  mean_errors  mean_correct
sc_delims_query 3.962        0.126         0.000
  qval_max_typo 3.646        0.121         0.000
 rep_char_query 3.492        0.159         0.001
        emb_hex 3.240        0.227         0.003
        n_pairs 3.156        0.568         0.025
       n_eq_url 3.073        0.577         0.029
   max_qkey_len 3.055        0.954         0.044
      query_len 3.001        1.774         0.089
      n_amp_url 2.969        0.359         0.007
 sc_other_query 2.898        0.750         0.033

## false negatives (phishing scored lowest)

    p                                                                                                  url
0.041                                               http://www.wikiwand.com/en/Select_or_special_committee
0.042                                                  http://www.calculator.net/ip-subnet-calculator.html
0.044                                                  http://www.infobarrel.com/Digital_Cameras_with_WiFi
0.051                                                                        https://www.directrelief.org/
0.051 https://www.quora.com/Why-is-the-longest-path-problem-NP-complete-given-that-the-shortest-path-probl
0.052                                                      https://www.wisegeek.com/what-is-a-form-w-9.htm
0.054                                                                              http://www.nbcnews.com/
0.056                                       https://www.consumeraffairs.com/internet/internet_services.htm
0.056                                                              https://www.facebook.com/mimosanetworks
0.057 https://bytes.com/topic/computer-hardware/answers/903158-what-some-good-open-source-software-hardwar

## false positives (clean scored highest)

    p                                                                                                  url
0.966 https://support-appleld.com.secureupdate.duilawyeryork.com/ap/ce9f83cca53de77/?cmd=_update&dispatch=
0.959 http://secureupdate.appleld.com.duilawyeryork.com/ap/9330524a3db85de?cmd=_update&dispatch=9330524a3d
0.948                                         https://urbanmeisters.ovh/wp-admin/css/colors/blue/sparka/DE
0.947                                  http://giaanhvu.com.vn/wp-content/languages/plugins/Cladoselachidae
0.939 https://login.microsoftonline.com/abe32f68-c72d-420d-b5bd-750c63a268e4/oauth2/authorize?client_id=00
0.938 https://login.microsoftonline.com/decee90c-ce03-461e-8c21-dd538e181c75/oauth2/authorize?client_id=00
0.937                             http://ww4.farmoyunlari.com/?subid1=4ae712f2-9a35-11e8-a4de-44a7c1746edf
0.937 https://login.microsoftonline.com/aa687de1-52b4-4b91-9b35-794eba4fd892/oauth2/authorize?client_id=00
0.936 https://login.microsoftonline.com/dc046083-4ce8-437a-bd49-e995b65e4d11/oauth2/authorize?client_id=00
0.933 https://login.microsoftonline.com/9024fef9-acd7-4a9a-98d1-b7225b67cf24/oauth2/authorize?client_id=00


# test

# Error analysis (2858 URLs, threshold 0.846)

TP 1009  FP 15  FN 420  TN 1414  | recall 0.706  FPR 0.0105  precision 0.985  accuracy 0.848

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http 1713       937    0.308    776    0.018
        scheme       https 1145       492    0.266    653    0.002
      has path     no path  871       296    0.530    575    0.003
      has path        path 1987      1133    0.232    854    0.015
        length       26-40  835       337    0.567    498    0.016
        length       41-70 1036       533    0.285    503    0.012
        length      71-120  461       271    0.077    190    0.005
        length        <=25  296        69    0.681    227    0.000
        length        >120  230       219    0.041     11      NaN
popular domain not popular 2106      1209    0.299    897    0.017
popular domain     popular  752       220    0.268    532    0.000
           www      no www 1583      1131    0.257    452    0.031
           www         www 1275       298    0.433    977    0.001
           tld         com 1791       873    0.273    918    0.009
           tld          de   42         9      NaN     33    0.000
           tld         net   91        59    0.373     32    0.062
           tld         org  156        24    0.417    132    0.000
           tld       other  660       410    0.322    250    0.020
           tld          ru   68        33    0.333     35    0.000
           tld          uk   50        21    0.238     29    0.000

## Features that separate false negatives vs caught phishing (Cohen's d)

           feature      d  mean_errors  mean_correct
           ent_url -1.145        3.901         4.417
           url_len -1.065        3.706         4.264
 longest_digit_run -1.040        0.309         1.118
  ratio_delims_url  0.866        0.028         0.019
    url_digit_rate -0.838        0.022         0.104
          url_leet -0.805        0.009         0.050
ratio_nonalnum_url  0.780        0.197         0.163
          path_len -0.772        1.792         2.864
          ent_path -0.764        2.046         3.214
       max_seg_len -0.750        1.474         2.340

## Features that separate false positives vs correct clean (Cohen's d)

            feature      d  mean_errors  mean_correct
       brand_in_reg  3.031        0.133         0.001
qval_min_legibility -1.900        0.733         0.983
              n_sub -1.819        0.139         0.600
        n_dots_host -1.754        0.828         1.078
      sc_other_host -1.754        0.828         1.078
          has_query  1.727        0.333         0.030
            n_pairs  1.600        0.258         0.024
       max_qkey_len  1.581        0.500         0.044
           n_eq_url  1.542        0.258         0.026
          query_len  1.535        0.925         0.090

## false negatives (phishing scored lowest)

    p                                                                                                  url
0.072                                                                    http://www.geocities.ws/steamcom/
0.074                                                              http://feeds.feedburner.com/investorway
0.088                                                                     https://stateagencybe.tumblr.com
0.093                                                                         https://seetflix.tumblr.com/
0.096                                                                        https://www.officialliker.co/
0.102                                                              https://artekcamp.tumblr.com/icampi#_=_
0.103                                                                                 http://www.dalla.eu/
0.104                                                                         https://www.perfectliker.net
0.115                                                                    http://www.automoves-halifax.com/
0.120 http://www.officialtobinbell.com/situasi-poker-online-indonesia-sokongan-implementasi-android-dan-io

## false positives (clean scored highest)

    p                                                                                               url
0.933                                                                        http://back.dog/auth/login
0.896                                                                http://isp1.us/state/new-york/nyc/
0.896                                                   http://termolak.bayhamconsulting.com/t/OOFJCi01
0.895 http://bectechnologies.net/wordpress/wp-content/uploads/2015/08/BEC_8920NE_QSG_v1.0_2014_0711.pdf
0.887                                                            http://eudesign.com/mnems/portstar.htm
0.886                                                                      http://bagru.info/t/BySXSWap
0.886                                    https://freemeteo.ro/vremea/?language=romanian&country=romania
0.882                                                                     http://cyb-sys.com/jietg/Upue
0.873                                                          http://isp1.us/state/washington/seattle/
0.872                                                                    http://yasmin888.blogspot.com/


# external_test

# Error analysis (2858 URLs, threshold 0.846)

TP 598  FP 0  FN 831  TN 1429  | recall 0.418  FPR 0.0000  precision 1.000  accuracy 0.709

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http  750       750    0.807      0      NaN
        scheme       https 2108       679    0.333   1429      0.0
      has path     no path 2458      1029    0.715   1429      0.0
      has path        path  400       400    0.238      0      NaN
        length       26-40 1456       571    0.727    885      0.0
        length       41-70  386       370    0.273     16      0.0
        length      71-120  142       142    0.155      0      NaN
        length        <=25  835       307    0.948    528      0.0
        length        >120   39        39    0.051      0      NaN
popular domain not popular 2601      1270    0.591   1331      0.0
popular domain     popular  257       159    0.503     98      0.0
           www      no www  833       833    0.358      0      NaN
           www         www 2025       596    0.894   1429      0.0
           tld         app   88        87    0.563      1      NaN
           tld          co   68        59    0.322      9      NaN
           tld         com 1367       628    0.650    739      0.0
           tld          io   77        70    0.329      7      NaN
           tld         net   98        58    0.621     40      0.0
           tld         org  189        27    1.000    162      0.0
           tld       other  971       500    0.538    471      0.0

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          ent_url -1.672        3.585         4.259
 ratio_delims_url  1.529        0.035         0.021
          url_len -1.434        3.434         4.019
longest_digit_run -1.299        0.305         1.209
              www  1.287        0.641         0.105
  ratio_other_url  1.157        0.109         0.075
            https -1.107        0.272         0.758
   url_digit_rate -1.029        0.027         0.113
         has_path -0.978        0.114         0.510
    ent_path_norm -0.970        0.095         0.423

## Features that separate false positives vs correct clean (Cohen's d)

(too few errors)

## false negatives (phishing scored lowest)

    p                            url
0.055        http://www.coinhive.com
0.057       http://www.bearsmyip.com
0.063 http://www.medianewsonline.com
0.069    http://www.simplemining.net
0.078      http://www.cshack.ucoz.ru
0.079         http://www.salas.co.uk
0.079               http://www.na.tl
0.081         http://www.ys-pack.com
0.084 https://www.bitmart-trust.net/
0.086      http://www.artgrowth.fund

## false positives (clean scored highest)

(none)
