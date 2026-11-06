# oof

# Error analysis (66187 URLs, threshold 0.828)

TP 21650  FP 373  FN 7281  TN 36883  | recall 0.748  FPR 0.0100  precision 0.983  accuracy 0.884

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by        value     n  phishing  FN rate  clean  FP rate
        scheme         http 21483     13862    0.198   7621    0.026
        scheme        https 27018      7098    0.343  19920    0.004
        scheme    no scheme 17640      7925    0.265   9715    0.010
        scheme other scheme    46        46    0.109      0      NaN
      has path      no path 13698      6289    0.372   7409    0.018
      has path         path 52489     22642    0.218  29847    0.008
        length        26-40 15342      6695    0.394   8647    0.018
        length        41-70 24184      9261    0.233  14923    0.007
        length       71-120 12925      5648    0.111   7277    0.006
        length         <=25  8796      3620    0.443   5176    0.008
        length         >120  4940      3707    0.070   1233    0.019
popular domain  not popular 51306     26915    0.232  24391    0.015
popular domain      popular 14881      2016    0.513  12865    0.001
           www       no www 43802     23858    0.236  19944    0.016
           www          www 22385      5073    0.326  17312    0.003
           tld           br   901       718    0.185    183    0.016
           tld          com 36736     13433    0.292  23303    0.009
           tld          net  2443      1256    0.293   1187    0.009
           tld          org  4767      1132    0.264   3635    0.006
           tld        other 18997     11468    0.204   7529    0.014
           tld           ru  1255       597    0.266    658    0.017
           tld           uk  1088       327    0.187    761    0.014

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          url_len -0.692        3.677         4.133
    sw_phrase_url -0.661        0.027         0.277
          ent_url -0.633        3.961         4.279
     ent_url_norm  0.600        0.797         0.752
     sc_other_url -0.537        1.143         1.439
   sw_phrase_path -0.525        0.017         0.176
         url_leet -0.520        0.015         0.046
longest_digit_run -0.515        0.510         0.964
     reg_log_rank -0.504        5.518         5.889
            n_seg -0.497        0.746         1.062

## Features that separate false positives vs correct clean (Cohen's d)

       feature      d  mean_errors  mean_correct
  sfx_platform  2.768        0.319         0.010
      url_leet  0.999        0.031         0.008
       emb_hex  0.877        0.097         0.009
  is_shortener  0.820        0.019         0.000
url_legibility -0.770        0.758         0.864
  reg_log_rank  0.695        5.850         4.837
           www -0.693        0.123         0.468
  seg_max_leet  0.685        0.055         0.016
   sw_kit_path  0.668        0.087         0.015
n_hyphens_path -0.662        0.050         0.583

## false negatives (phishing scored lowest)

    p                                                                                    url
0.002                                        https://www.wisegeek.com/what-is-a-form-w-9.htm
0.002            https://www.8premier.com/mathematical-physics-by-h-k-dass-pdf-free-download
0.002                                           https://www.powr.io/media-gallery/i/41370701
0.003                                            https://www.powr.io/form-builder/i/41100949
0.003                                  https://www.8premier.com/bloodsport-2-dual-audio-1996
0.003 https://www.8premier.com/postworld-cheat-code-with-serial-key-free-win-mac-2022-latest
0.004                                        https://www.google.com.br/search?q=suporte+itau
0.004                                 https://www.contactsupportgroup.com/att-email-support/
0.005                                 http://www.angelfire.com/ma/MartinsWorld/Hotmail2.html
0.005                                                   https://www.instagram.com/unicard.us

## false positives (clean scored highest)

    p                                                                                         url
0.991                                                http://schools-wikipedia.org/wp/i/Insect.htm
0.991                                                                 http://url.cn/51rszau?69swc
0.989                     kiwidepia.com/kiwi/bi9vL2IvQ2F0ZWdvcsOtYX5Ob2JsZXNfZGVfRXNwYcOxYV83MWNh
0.984                                                                        https://git.io/fhzd5
0.983                                              https://ezoteryka-magia-okultyzm.blogspot.com/
0.979                                        http://r68aza.bankruptcy-law-help.com/B01K3I71LE.pdf
0.977 https://rhetfig.appspot.com/view?id=ag1zfnJoZXRmaWctaHJkchgLEhBSaGV0b3JpY2FsRmlndXJlGM3fAgw
0.976 https://rhetfig.appspot.com/view?id=ag1zfnJoZXRmaWctaHJkchgLEhBSaGV0b3JpY2FsRmlndXJlGMGjCQw
0.976                                        http://www.starsportsmanship.com/go/school/login.php
0.976 https://rhetfig.appspot.com/view?id=ag1zfnJoZXRmaWctaHJkchgLEhBSaGV0b3JpY2FsRmlndXJlGNOGAww


# test

# Error analysis (2858 URLs, threshold 0.828)

TP 1052  FP 21  FN 377  TN 1408  | recall 0.736  FPR 0.0147  precision 0.980  accuracy 0.861

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http 1713       937    0.236    776    0.023
        scheme       https 1145       492    0.317    653    0.005
      has path     no path  871       296    0.365    575    0.019
      has path        path 1987      1133    0.237    854    0.012
        length       26-40  835       337    0.457    498    0.026
        length       41-70 1036       533    0.251    503    0.012
        length      71-120  461       271    0.118    190    0.005
        length        <=25  296        69    0.522    227    0.004
        length        >120  230       219    0.096     11      NaN
popular domain not popular 2108      1211    0.252    897    0.022
popular domain     popular  750       218    0.330    532    0.002
           www      no www 1583      1131    0.234    452    0.042
           www         www 1275       298    0.376    977    0.002
           tld         com 1791       873    0.246    918    0.016
           tld          de   42         9      NaN     33    0.000
           tld         net   91        59    0.390     32    0.094
           tld         org  156        24    0.542    132    0.008
           tld       other  660       410    0.268    250    0.008
           tld          ru   68        33    0.303     35    0.000
           tld          uk   50        21    0.238     29    0.000

## Features that separate false negatives vs caught phishing (Cohen's d)

           feature      d  mean_errors  mean_correct
           ent_url -0.746        4.000         4.360
           url_len -0.729        3.802         4.207
 longest_digit_run -0.698        0.457         1.032
          url_leet -0.678        0.012         0.047
  ratio_delims_url  0.670        0.027         0.020
     sw_phrase_url -0.615        0.048         0.285
ratio_nonalnum_url  0.595        0.192         0.166
    url_digit_rate -0.590        0.036         0.095
      seg_max_leet -0.545        0.025         0.100
           emb_hex -0.530        0.011         0.192

## Features that separate false positives vs correct clean (Cohen's d)

           feature      d  mean_errors  mean_correct
      sfx_platform  2.619        0.429         0.021
             n_sub -1.591        0.198         0.601
               www -1.299        0.095         0.692
    sw_phrase_path  1.248        0.118         0.009
     sw_phrase_url  1.039        0.118         0.013
       sw_kit_path  0.954        0.099         0.010
host_digit_in_word  0.944        0.238         0.043
    url_legibility -0.923        0.768         0.885
          url_leet  0.797        0.014         0.004
        sw_kit_url  0.784        0.099         0.015

## false negatives (phishing scored lowest)

    p                                                                                                  url
0.009                                                       https://www.autolikesfree.net/access-token.php
0.020 http://www.officialtobinbell.com/situasi-poker-online-indonesia-sokongan-implementasi-android-dan-io
0.021                                                                    http://www.geocities.ws/steamcom/
0.022                                                              http://feeds.feedburner.com/investorway
0.032         https://www.carddesignstudio.com/allaboutme/designer/wellsfargobank/DeviceNotSupported.shtml
0.036                                                                        https://www.officialliker.co/
0.041                               http://nationwide-com.com/nationwide-log-in/nationwide-log-in-internet
0.042                                                                         https://www.perfectliker.net
0.043                                                                     https://nineled.com/Suncorp-user
0.052                         https://bankcampuscareers.tal.net/vx/lang-en-GB/candidate/application/292496

## false positives (clean scored highest)

    p                                                                                               url
0.931                                                                     http://p30banksoal.blogfa.com
0.927                                                http://www.kamicemc.com/images/docs/astkatalog.pdf
0.920                                                                    http://moriwajin.blogspot.com/
0.907                                                                     http://cyb-sys.com/jietg/Upue
0.903                                                                        http://back.dog/auth/login
0.898                                                                    http://yasmin888.blogspot.com/
0.889 http://bectechnologies.net/wordpress/wp-content/uploads/2015/08/BEC_8920NE_QSG_v1.0_2014_0711.pdf
0.882                                                          http://in-the-name-of-god1.mihanblog.com
0.875                                                      http://tjscott.net/firewall/stateful.ins.htm
0.874                                                                         https://ww3.dbsmanga.com/


# external_test

# Error analysis (2858 URLs, threshold 0.828)

TP 772  FP 1  FN 657  TN 1428  | recall 0.540  FPR 0.0007  precision 0.999  accuracy 0.770

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http  750       750    0.672      0      NaN
        scheme       https 2108       679    0.225   1429    0.001
      has path     no path 2458      1029    0.540   1429    0.001
      has path        path  400       400    0.252      0      NaN
        length       26-40 1456       571    0.548    885    0.000
        length       41-70  386       370    0.197     16    0.000
        length      71-120  142       142    0.127      0      NaN
        length        <=25  835       307    0.818    528    0.002
        length        >120   39        39    0.051      0      NaN
popular domain not popular 2602      1271    0.474   1331    0.001
popular domain     popular  256       158    0.342     98    0.000
           www      no www  833       833    0.239      0      NaN
           www         www 2025       596    0.768   1429    0.001
           tld         app   88        87    0.241      1      NaN
           tld          co   68        59    0.119      9      NaN
           tld         com 1367       628    0.583    739    0.000
           tld          io   77        70    0.186      7      NaN
           tld         net   98        58    0.552     40    0.000
           tld         org  189        27    0.630    162    0.000
           tld       other  971       500    0.402    471    0.002

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          ent_url -1.301        3.558         4.129
              www  1.233        0.697         0.179
 ratio_delims_url  1.195        0.036         0.024
          url_len -1.068        3.424         3.895
longest_digit_run -1.023        0.276         1.029
            https -1.004        0.233         0.681
     sfx_platform -0.945        0.067         0.448
   url_legibility  0.902        0.847         0.674
   url_digit_rate -0.841        0.024         0.096
  ratio_other_url  0.793        0.108         0.083

## Features that separate false positives vs correct clean (Cohen's d)

(too few errors)

## false negatives (phishing scored lowest)

    p                                              url
0.031                          http://www.coinhive.com
0.031                   http://www.medianewsonline.com
0.038                         http://www.bearsmyip.com
0.047 https://alqowi.org/landmark-onlineservices/logon
0.058                      http://www.simplemining.net
0.062                   https://www.bitmart-trust.net/
0.067         https://bio.site/instagramappealform.com
0.067     https://mechanizedarts.com/signedmanagement/
0.067              https://top6six.com/findomesticweb/
0.088                     https://beacons.ai/hex.stake

## false positives (clean scored highest)

   p                   url
0.93 https://www.bcnad.xyz
