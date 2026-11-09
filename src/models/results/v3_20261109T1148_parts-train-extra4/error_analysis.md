# oof

# Error analysis (43255 URLs, threshold 0.895)

TP 15446  FP 217  FN 6186  TN 21406  | recall 0.714  FPR 0.0100  precision 0.986  accuracy 0.852

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by        value     n  phishing  FN rate  clean  FP rate
        scheme         http 15804     10678    0.221   5126    0.024
        scheme        https 16855      5454    0.397  11401    0.004
        scheme    no scheme 10563      5467    0.303   5096    0.011
        scheme other scheme    33        33    0.152      0      NaN
      has path      no path  9327      4665    0.467   4662    0.018
      has path         path 33928     16967    0.236  16961    0.008
        length        26-40 10263      5019    0.435   5244    0.018
        length        41-70 15488      6953    0.261   8535    0.008
        length       71-120  8402      4274    0.128   4128    0.004
        length         <=25  5613      2587    0.546   3026    0.009
        length         >120  3489      2799    0.083    690    0.009
popular domain  not popular 33989     19994    0.263  13995    0.015
popular domain      popular  9266      1638    0.568   7628    0.000
           www       no www 28923     17759    0.272  11164    0.017
           www          www 14332      3873    0.351  10459    0.002
           tld           br   622       517    0.182    105    0.019
           tld          com 23697     10168    0.329  13529    0.009
           tld          net  1612       915    0.329    697    0.010
           tld          org  2894       809    0.320   2085    0.006
           tld        other 12876      8516    0.234   4360    0.014
           tld           ru   865       458    0.301    407    0.015
           tld           uk   689       249    0.197    440    0.009

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          url_len -0.772        3.671         4.169
          ent_url -0.710        3.954         4.305
    sw_phrase_url -0.669        0.036         0.290
     ent_url_norm  0.660        0.798         0.749
            n_seg -0.595        0.718         1.093
         path_len -0.589        1.932         2.786
     sc_other_url -0.583        1.141         1.457
         ent_path -0.560        2.225         3.113
longest_digit_run -0.550        0.509         0.990
   sw_phrase_path -0.527        0.021         0.182

## Features that separate false positives vs correct clean (Cohen's d)

       feature      d  mean_errors  mean_correct
  sfx_platform  2.895        0.346         0.011
      url_leet  0.871        0.027         0.007
url_legibility -0.788        0.758         0.865
  reg_log_rank  0.776        5.951         4.820
           www -0.747        0.115         0.487
   reg_popular -0.728        0.009         0.356
         https -0.695        0.184         0.531
       emb_hex  0.680        0.078         0.010
n_hyphens_path -0.669        0.031         0.564
   sw_kit_path  0.628        0.080         0.014

## false negatives (phishing scored lowest)

    p                                                                                                  url
0.000 https://bytes.com/topic/computer-hardware/answers/903158-what-some-good-open-source-software-hardwar
0.001                                                  http://www.calculator.net/ip-subnet-calculator.html
0.001                                               http://www.wikiwand.com/en/Select_or_special_committee
0.001 https://www.quora.com/Why-is-the-longest-path-problem-NP-complete-given-that-the-shortest-path-probl
0.002                                       https://www.consumeraffairs.com/internet/internet_services.htm
0.002                                                          https://www.powr.io/form-builder/i/41100949
0.002                                                                        https://www.directrelief.org/
0.002               https://www.8premier.com/postworld-cheat-code-with-serial-key-free-win-mac-2022-latest
0.003                                                      https://www.wisegeek.com/what-is-a-form-w-9.htm
0.003 https://blog.roku.com/blog/2016/08/18/discovery-tlc-animal-planet-science-discovery-investigation-no

## false positives (clean scored highest)

    p                                                                                                  url
0.998 http://secureupdate.appleld.com.duilawyeryork.com/ap/9330524a3db85de?cmd=_update&dispatch=9330524a3d
0.993                              kiwidepia.com/kiwi/bi9vL2IvQ2F0ZWdvcsOtYX5Ob2JsZXNfZGVfRXNwYcOxYV83MWNh
0.993 https://support-appleld.com.secureupdate.duilawyeryork.com/ap/ce9f83cca53de77/?cmd=_update&dispatch=
0.991                                  http://giaanhvu.com.vn/wp-content/languages/plugins/Cladoselachidae
0.991                                                         http://schools-wikipedia.org/wp/i/Insect.htm
0.989                                                       https://ezoteryka-magia-okultyzm.blogspot.com/
0.987                                                                        http://keiba-review.com/supi/
0.987                                               http://voenspec.su/site/latest%20revalidate/Update.php
0.984                                                                http://ederslik.edu.az/site/index.php
0.984                                                                                 http://i-to.cc/zX4FA


# test

# Error analysis (2858 URLs, threshold 0.895)

TP 1002  FP 8  FN 427  TN 1421  | recall 0.701  FPR 0.0056  precision 0.992  accuracy 0.848

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http 1713       937    0.269    776    0.010
        scheme       https 1145       492    0.356    653    0.000
      has path     no path  871       296    0.480    575    0.007
      has path        path 1987      1133    0.252    854    0.005
        length       26-40  835       337    0.534    498    0.012
        length       41-70 1036       533    0.280    503    0.004
        length      71-120  461       271    0.111    190    0.000
        length        <=25  296        69    0.609    227    0.000
        length        >120  230       219    0.119     11      NaN
popular domain not popular 2106      1209    0.289    897    0.008
popular domain     popular  752       220    0.355    532    0.002
           www      no www 1583      1131    0.275    452    0.018
           www         www 1275       298    0.389    977    0.000
           tld         com 1791       873    0.284    918    0.005
           tld          de   42         9      NaN     33    0.000
           tld         net   91        59    0.390     32    0.062
           tld         org  156        24    0.542    132    0.000
           tld       other  660       410    0.300    250    0.004
           tld          ru   68        33    0.364     35    0.000
           tld          uk   50        21    0.333     29    0.000

## Features that separate false negatives vs caught phishing (Cohen's d)

           feature      d  mean_errors  mean_correct
           ent_url -0.841        3.986         4.385
           url_len -0.801        3.793         4.231
 longest_digit_run -0.744        0.455         1.062
  ratio_delims_url  0.732        0.027         0.019
          url_leet -0.700        0.013         0.049
ratio_nonalnum_url  0.618        0.192         0.165
    url_digit_rate -0.617        0.036         0.098
     sw_phrase_url -0.613        0.057         0.293
          ent_path -0.609        2.204         3.154
          path_len -0.608        1.944         2.806

## Features that separate false positives vs correct clean (Cohen's d)

           feature      d  mean_errors  mean_correct
    sw_phrase_path  2.467        0.224         0.010
      sfx_platform  2.173        0.375         0.025
     sw_phrase_url  2.088        0.224         0.014
             n_sub -1.658        0.173         0.598
         rep_digit  1.620        0.125         0.005
host_digit_in_word  1.600        0.375         0.044
               www -1.487        0.000         0.688
     rep_char_host  1.180        0.125         0.009
          url_leet  1.101        0.018         0.004
    url_legibility -1.082        0.746         0.884

## false negatives (phishing scored lowest)

    p                                                                                                  url
0.024                                                                    http://www.geocities.ws/steamcom/
0.030                                                                        https://www.officialliker.co/
0.031                                                              http://feeds.feedburner.com/investorway
0.034 http://www.officialtobinbell.com/situasi-poker-online-indonesia-sokongan-implementasi-android-dan-io
0.042                                                              https://artekcamp.tumblr.com/icampi#_=_
0.043                                                       https://www.autolikesfree.net/access-token.php
0.047                               http://nationwide-com.com/nationwide-log-in/nationwide-log-in-internet
0.052         https://www.carddesignstudio.com/allaboutme/designer/wellsfargobank/DeviceNotSupported.shtml
0.064                                                        https://www.lasertec-mi.com/suneast/logon.asp
0.069                         https://bankcampuscareers.tal.net/vx/lang-en-GB/candidate/application/292496

## false positives (clean scored highest)

    p                                                            url
0.962                       http://in-the-name-of-god1.mihanblog.com
0.942                                  http://cyb-sys.com/jietg/Upue
0.942                                 http://yasmin888.blogspot.com/
0.937                                  http://p30banksoal.blogfa.com
0.932                                     http://back.dog/auth/login
0.917                                 http://moriwajin.blogspot.com/
0.914                   http://tjscott.net/firewall/stateful.ins.htm
0.901 http://clioadams.azurewebsites.net/Account/Login?ReturnUrl=%2F


# external_test

# Error analysis (2858 URLs, threshold 0.895)

TP 728  FP 1  FN 701  TN 1428  | recall 0.509  FPR 0.0007  precision 0.999  accuracy 0.754

## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)

            by       value    n  phishing  FN rate  clean  FP rate
        scheme        http  750       750    0.689      0      NaN
        scheme       https 2108       679    0.271   1429    0.001
      has path     no path 2458      1029    0.573   1429    0.001
      has path        path  400       400    0.278      0      NaN
        length       26-40 1456       571    0.583    885    0.000
        length       41-70  386       370    0.227     16    0.000
        length      71-120  142       142    0.176      0      NaN
        length        <=25  835       307    0.837    528    0.002
        length        >120   39        39    0.051      0      NaN
popular domain not popular 2601      1270    0.506   1331    0.001
popular domain     popular  257       159    0.365     98    0.000
           www      no www  833       833    0.280      0      NaN
           www         www 2025       596    0.785   1429    0.001
           tld         app   88        87    0.299      1      NaN
           tld          co   68        59    0.169      9      NaN
           tld         com 1367       628    0.616    739    0.000
           tld          io   77        70    0.286      7      NaN
           tld         net   98        58    0.569     40    0.000
           tld         org  189        27    0.630    162    0.000
           tld       other  971       500    0.416    471    0.002

## Features that separate false negatives vs caught phishing (Cohen's d)

          feature      d  mean_errors  mean_correct
          ent_url -1.290        3.578         4.145
 ratio_delims_url  1.159        0.035         0.024
              www  1.150        0.668         0.176
longest_digit_run -1.082        0.282         1.069
          url_len -1.056        3.441         3.907
            https -0.920        0.262         0.680
   url_digit_rate -0.896        0.024         0.101
   url_legibility  0.883        0.840         0.670
     sfx_platform -0.856        0.094         0.445
  host_digit_rate -0.778        0.022         0.114

## Features that separate false positives vs correct clean (Cohen's d)

(too few errors)

## false negatives (phishing scored lowest)

    p                                              url
0.020                   http://www.medianewsonline.com
0.025                          http://www.coinhive.com
0.042                         http://www.bearsmyip.com
0.058 https://alqowi.org/landmark-onlineservices/logon
0.059     https://mechanizedarts.com/signedmanagement/
0.066                   https://www.bitmart-trust.net/
0.078                      http://www.simplemining.net
0.090            http://www.rawlogic.flywheelsites.com
0.093                     https://beacons.ai/hex.stake
0.094                    http://www.marinov.zzz.com.ua

## false positives (clean scored highest)

    p                   url
0.946 https://www.bcnad.xyz
