// Nexus Modern IPTV Player & YouTube-Style Controller Engine

const channelData = [
  {
    "id": "aaryaa_tv",
    "name": "Aaryaa Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.ottlive.co.in/aryatvtamil/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1920x1080"
  },
  {
    "id": "fail_army",
    "name": "Fail Army",
    "cat": "English",
    "icon": "📺",
    "url": "https://failarmy-international-in.samsung.wurl.tv/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "hungama_tv",
    "name": "Hungama TV",
    "cat": "Tamil",
    "icon": "👶",
    "url": "http://103.185.24.134:3001/HUNGAMA/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1047x576"
  },
  {
    "id": "isaiaruvi_tv",
    "name": "Isaiaruvi Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://segment.yuppcdn.net/140622/isaiaruvi/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  },
  {
    "id": "kalaignar_murasu",
    "name": "Kalaignar Murasu",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://yuppmedtaorire.akamaized.net/v1/master/a0d007312bfd99c47f76b77ae26b1ccdaae76cb1/murasu_nim_https/050522/murasu/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  },
  {
    "id": "kalaignar_tv",
    "name": "Kalaignar Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://segment.yuppcdn.net/240122/kalaignartv/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  },
  {
    "id": "mk_six",
    "name": "MK Six",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt06.tangotv.in/qYyB8fXVMKSIX/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "mn_tv",
    "name": "MN Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mntv.livebox.co.in/mntvhls/live.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1280x720"
  },
  {
    "id": "madha_tv",
    "name": "Madha TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://mumt07.tangotv.in/zHjX9OFlMADHATV/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "madhimugam_tv",
    "name": "Madhimugam TV",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://mumt01.tangotv.in/O5aw8Zn3MATHIMUGAMTV/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "mei_alai_tv",
    "name": "Mei Alai TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://meialai.iptelevishion.com/meialai/2/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "768x576"
  },
  {
    "id": "movie_club_2_tv",
    "name": "Movie Club 2 Tv",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://d3gnyty2vddhsg.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-ytipwjqub3kf8/TMC2_IN.m3u8?ads.ads_cdn=cf&ads.cdn=cf",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "movie_club_tv",
    "name": "Movie Club Tv",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://sis-global.prod.samsungtv.plus/v1/tvpprd/sc-mp2ar4ca425xo.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "murasu_tv",
    "name": "Murasu Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://segment.yuppcdn.net/050522/murasu/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  },
  {
    "id": "nh_tamil_gold",
    "name": "NH Tamil Gold",
    "cat": "Tamil",
    "icon": "🎬",
    "url": "https://d3arbp6l7f096k.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-gv6wgpbb4mgwk/playlist.m3u8?ads.ads_cdn=cf&ads.app_domain=APP_DOMAIN&ads.cdn=cf",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "news_7_tv",
    "name": "News 7 Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://segment.yuppcdn.net/240122/news7/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  },
  {
    "id": "news_tamil_24x7",
    "name": "News Tamil 24x7",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://cdn.pishow.tv/ott/live/1433/master.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1047x576"
  },
  {
    "id": "nickelodeon",
    "name": "Nickelodeon",
    "cat": "Tamil",
    "icon": "👶",
    "url": "http://103.185.24.134:3001/NICK/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1047x576"
  },
  {
    "id": "polimer_tv",
    "name": "Polimer TV",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://cdn.pishow.tv/ott/live/1241/master.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1047x576"
  },
  {
    "id": "puthiya_thalaimurai",
    "name": "Puthiya Thalaimurai",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://mumt07.tangotv.in/zHjX9OFlPUTHIYAEXPRESS/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "puthuyugam_tv",
    "name": "Puthuyugam TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt04.tangotv.in/m18aqlK4PUTHUYUGAMTV/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "sirippoli_tv",
    "name": "Sirippoli Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://segment.yuppcdn.net/240122/siripoli/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  },
  {
    "id": "sonic",
    "name": "Sonic",
    "cat": "Tamil",
    "icon": "👶",
    "url": "http://103.185.24.134:3001/SONIC/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1047x576"
  },
  {
    "id": "sony_bbc_earth_hd",
    "name": "Sony BBC Earth HD",
    "cat": "Tamil",
    "icon": "✨",
    "url": "https://cloudplay-sonyliv.pages.dev/bbcearthhd.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "384x216"
  },
  {
    "id": "sony_pix_hd",
    "name": "Sony Pix HD",
    "cat": "English",
    "icon": "✨",
    "url": "https://cloudplay-sonyliv.pages.dev/pixhd.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "384x216"
  },
  {
    "id": "sony_sports_ten_4",
    "name": "Sony Sports Ten 4",
    "cat": "Tamil",
    "icon": "🏏",
    "url": "https://cloudplay-sonyliv.pages.dev/ten4.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "384x216"
  },
  {
    "id": "sony_yay",
    "name": "Sony Yay!",
    "cat": "Tamil",
    "icon": "👶",
    "url": "https://cloudplay-sonyliv.pages.dev/yay.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "384x216"
  },
  {
    "id": "south_station_tv",
    "name": "South Station Tv",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://cc-yw7ztecy8do3q.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-yw7ztecy8do3q/SS_IN.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "star_vijay",
    "name": "Star Vijay",
    "cat": "Tamil",
    "icon": "⭐",
    "url": "https://da86m1sqpm3o0.cloudfront.net/28072023/smil:starvijayuk.smil/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "super_hungama",
    "name": "Super Hungama",
    "cat": "Tamil",
    "icon": "👶",
    "url": "http://103.185.24.134:3001/SUPER-HUNGAMA/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1047x576"
  },
  {
    "id": "tamil_janam",
    "name": "Tamil Janam",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://mumt01.tangotv.in/O5aw8Zn3JANAMTVTAMIL/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "tamilan_tv",
    "name": "Tamilan TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt04.tangotv.in/m18aqlK4TAMILANTELEVISION/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "489x360"
  },
  {
    "id": "wow_kidz_tamil",
    "name": "WOW Kidz Tamil",
    "cat": "Tamil",
    "icon": "👶",
    "url": "https://yuppparoriglin.akamaized.net/181224/smil:wowkidztam.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b",
    "status": "Live",
    "live": true,
    "resolution": "1280x720"
  },
  {
    "id": "yet_max",
    "name": "YET Max",
    "cat": "Tamil",
    "icon": "🎵",
    "url": "https://live.yettelevision.com:5443/LiveApp/streams/yettv2.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1280x720"
  },
  {
    "id": "yet_tv",
    "name": "YET TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://live.yettelevision.com:5443/LiveApp/streams/yettv.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1280x720"
  },
  {
    "id": "zee_tamil_hd",
    "name": "Zee Tamil HD",
    "cat": "Tamil",
    "icon": "✨",
    "url": "https://da86m1sqpm3o0.cloudfront.net/28072023/smil:zeetamil1.smil/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "7s_music_tv",
    "name": "7s Music Tv",
    "cat": "Tamil",
    "icon": "🎵",
    "url": "https://cdn.pishow.tv/ott/live/1257/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "aaseervatham_tv",
    "name": "Aaseervatham TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://mumt04.tangotv.in/m18aqlK4AASEERVATHAMTV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "aastha_tamil",
    "name": "Aastha Tamil",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://aasthaott.akamaized.net/110923/smil:aasthatamil.smil/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "angel_tv",
    "name": "Angel TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://janya-digimix.akamaized.net/vglive-sk-394914/india/ngrp:angelindia_all/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "angel_tv_america",
    "name": "Angel TV America",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://janya-digimix.akamaized.net/vglive-sk-374850/america/ngrp:angelamerica_all/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "angel_tv_indo_china",
    "name": "Angel TV Indo-China",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://janya-digimix.akamaized.net/vglive-sk-703035/indochina/ngrp:angelindochina_all/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "angel_tv_indonesia",
    "name": "Angel TV Indonesia",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://janya-digimix.akamaized.net/vglive-sk-234616/indonesia/ngrp:angelindonesia_all/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "arputhar_yesu_tv",
    "name": "Arputhar Yesu TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://account33.livebox.co.in/jesushelpshls/live.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "chithiram_tv",
    "name": "Chithiram Tv",
    "cat": "Tamil",
    "icon": "👶",
    "url": "https://cdn.pishow.tv/ott/live/1243/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "colors_tamil_hd",
    "name": "Colors Tamil HD",
    "cat": "Tamil",
    "icon": "✨",
    "url": "https://da86m1sqpm3o0.cloudfront.net/28072023/smil:colorstamilhd11.smil/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "dd_tamil",
    "name": "DD Tamil",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://cdn-2.pishow.tv/live/26/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "dharsan_tv",
    "name": "Dharsan TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://cable91tataplay.akamaized.net/live/dharshantv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "etv_bal_bharat",
    "name": "ETV Bal Bharat",
    "cat": "Tamil",
    "icon": "👶",
    "url": "http://103.185.24.134:3001/ETV-BAL-BHARAT/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "go_usa",
    "name": "Go USA",
    "cat": "English",
    "icon": "📺",
    "url": "https://brandusa-gousa-1-in.samsung.wurl.tv/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "hebron_tv",
    "name": "Hebron TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://account20.livebox.co.in/charleshls/live.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "hosanna_tv",
    "name": "Hosanna TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://asia.mslivestream.net/mslive/bfba54c5c96a6359e2da0ca35f4998af.sdp/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "ibc_tamil",
    "name": "IBC Tamil",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://ibc.massstream.net/IBC/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "makkal_tv_576i",
    "name": "Makkal TV (576i)",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://5k8q87azdy4v-hls-live.wmncdn.net/MAKKAL/271ddf829afeece44d8732757fba1a66.sdp/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "moon_tv",
    "name": "Moon Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://player.mslivestream.net/mslive/e10bb900976df9177b9a080314f26f86.sdp/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "ntc_tv",
    "name": "NTC TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://galaxyott.live/hls/ntv.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "national_geographic",
    "name": "National Geographic",
    "cat": "Tamil",
    "icon": "📺",
    "url": "http://main.light-ott.net:80/play/live.php?mac=00:1A:79:17:28:41&stream=373017&extension=ts&play_token=zCaGy5dtla",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "news_j",
    "name": "News J",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://cdn.pishow.tv/ott/live/1279/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "news18_tamil_nadu",
    "name": "News18 Tamil Nadu",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://n18syndication.akamaized.net/bpk-tv/News18_Tamil_Nadu_NW18_MOB/output01/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "om_tv",
    "name": "OM TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://mumt01.tangotv.in/O5aw8Zn3OMTV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "oli_tv",
    "name": "Oli TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://live.olidigital.in/olitv/olitv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "peppers_tv",
    "name": "Peppers Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://cdn-2.pishow.tv/live/1383/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "polimer_news",
    "name": "Polimer news",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://live-cf-polimernews.dailyhunt.in/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "raj_digital_plus",
    "name": "Raj Digital Plus",
    "cat": "Tamil",
    "icon": "🎬",
    "url": "https://livestream.rajtv.tv/hlslive/Admin/px08241087/live/RajTV_Digital_plus/master_1.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "raj_musix_tamil",
    "name": "Raj Musix Tamil",
    "cat": "Tamil",
    "icon": "🎵",
    "url": "https://livestream.rajtv.tv/hlslive/Admin/px08241087/live/Raj_Musix/master_1.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "raj_tv",
    "name": "Raj TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://livestream.rajtv.tv/hlslive/Admin/px08241087/live/RAJTV/master_1.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "rakuten_action_movies",
    "name": "Rakuten Action Movies",
    "cat": "English",
    "icon": "📺",
    "url": "https://54045f0c40fd442c8b06df076aaf1e85.mediatailor.eu-west-1.amazonaws.com/v1/master/0547f18649bd788bec7b67b746e47670f558b6b2/production-LiveChannel-6065/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "rakuten_family_movies",
    "name": "Rakuten Family Movies",
    "cat": "English",
    "icon": "📺",
    "url": "https://e3207568b726401995c25670faaf32e4.mediatailor.eu-west-1.amazonaws.com/v1/master/0547f18649bd788bec7b67b746e47670f558b6b2/production-LiveChannel-6203/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "rakuten_top_movies",
    "name": "Rakuten Top Movies",
    "cat": "English",
    "icon": "📺",
    "url": "https://0145451975a64b35866170fd2e8fa486.mediatailor.eu-west-1.amazonaws.com/v1/master/0547f18649bd788bec7b67b746e47670f558b6b2/production-LiveChannel-5987/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "roja_hd_tv",
    "name": "Roja HD Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://live.rojatv.cloud/rojatv/rojatv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "roja_tv",
    "name": "Roja Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.rojatv.cloud/rojatv/rojatv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sai_tv",
    "name": "Sai TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt03.tangotv.in/Dsly5z3HSAITV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sairam_tv",
    "name": "Sairam TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "https://mumt04.tangotv.in/m18aqlK4SAIRAMTV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sanaa_tv",
    "name": "Sanaa Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://vglivessai.akamaized.net/us/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/b6d9e864-ec16-410a-804d-ccf8f720bfaa/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sirippoli_hd",
    "name": "Sirippoli HD",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://yuppmedtaorire.akamaized.net/v1/manifest/a0d007312bfd99c47f76b77ae26b1ccdaae76cb1/siripoli_nim_https/c4e6500f-ea05-4226-810e-2833ee0075ff/0.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "704x396"
  },
  {
    "id": "sivan_tv",
    "name": "Sivan TV",
    "cat": "Tamil",
    "icon": "🪷",
    "url": "http://sivantv.livebox.co.in/sivantvhls/sivan.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sony_max_2",
    "name": "Sony MAX 2",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://sl.vodep39240327.workers.dev/channel/SONY%20MAX%202.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sony_max_hd",
    "name": "Sony MAX HD",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://sl.vodep39240327.workers.dev/channel/SONY%20MAX%20HD.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sony_wah",
    "name": "Sony WAH",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://sl.vodep39240327.workers.dev/channel/SONY%20WAH.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "sooriyan_tv",
    "name": "Sooriyan TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://live20.bozztv.com/giatv/giatv-Infinittyott/Infinittyott/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "star_vijay_hd",
    "name": "Star Vijay HD",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://peaky.techcoder40.workers.dev/776.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "studio_one_tv",
    "name": "Studio One Tv",
    "cat": "Telugu",
    "icon": "📺",
    "url": "https://cdn-1.pishow.tv/live/276/master.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "subin_tv",
    "name": "Subin Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.galaxyott.live/live/subintv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "suriya_tv",
    "name": "Suriya Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.ottlive.co.in/suryatvtamil/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "suriyan_tv",
    "name": "Suriyan Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.sscloud7.com/live/suriyantv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "tvi_hd",
    "name": "TVI HD",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://live.cmr24.fm/TVI/HD/chunks.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "thalaa_tv",
    "name": "Thalaa Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://streams2.sofast.tv/ptnr-yupptv/title-THALAA-TV-TAM/sofastplayout/981f8f06-782a-4962-b5e0-7dcccd65279c_0_HLS/manifest.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "thanthi_tv",
    "name": "Thanthi Tv",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://streams.tangotv.in/THANTHITV/ORIGIN/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "tharun_movies",
    "name": "Tharun Movies",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://streaming.livebox.co.in/tharunmovieshls/live.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "toonami_movie",
    "name": "Toonami Movie",
    "cat": "English",
    "icon": "📺",
    "url": "http://api.toonamiaftermath.com:3000/movies/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "travel_xp_hd_tv",
    "name": "Travel XP HD Tv",
    "cat": "English",
    "icon": "📺",
    "url": "https://deltatesttatasky.akamaized.net/out/i/968284.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "travelxp_hd",
    "name": "Travelxp HD",
    "cat": "Tamil",
    "icon": "🌍",
    "url": "https://amg00416-amg00416c9-samsung-in-4882.playouts.now.amagi.tv/playlist/amg00416-travelxp-travelxphd-samsungin/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "ultimate_hd_tv",
    "name": "Ultimate HD Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.ottlive.co.in/utvtamil/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "ultimate_tv",
    "name": "Ultimate Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumbai-edge.smartplaytv.in/utv/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "vaanavil_tv",
    "name": "Vaanavil Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://6n3yope4d9ok-hls-live.5centscdn.com/vaanavil/TV.stream/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "vasanth_tv",
    "name": "Vasanth TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt04.tangotv.in/m18aqlK4VASANTHTV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "velicham_tv",
    "name": "Velicham Tv",
    "cat": "Tamil",
    "icon": "☀️",
    "url": "https://mumt05.tangotv.in/87NeALx2VALICHAMPLUS/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "vendhar_tv",
    "name": "Vendhar TV",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt04.tangotv.in/m18aqlK4VENDHARTV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "win_tv",
    "name": "Win Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://mumt06.tangotv.in/qYyB8fXVWINTV/index.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "zee_south_flix_tv",
    "name": "Zee South Flix Tv",
    "cat": "Hindi",
    "icon": "📺",
    "url": "https://amg00862-amg00862c9-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c9-amgplt0173/playlist.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  },
  {
    "id": "zee_tamil_news",
    "name": "Zee Tamil News",
    "cat": "Tamil",
    "icon": "📰",
    "url": "https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/ZMCL/ZeeTamilNews.m3u8",
    "status": "Dead",
    "live": false,
    "resolution": "0x0"
  }
];

let currentHls = null;
let activeChannel = channelData[0];
let currentFilter = 'all';
let currentLevelIndex = -1;

// --- 1. CHANNEL NAVIGATION & SEARCH ---
function renderChannels(items) {
  const grid = document.getElementById('channelsGrid');
  if (!grid) return;
  grid.innerHTML = '';
  items.forEach(ch => {
    const card = document.createElement('div');
    card.className = `channel-card ${ch.id === activeChannel.id ? 'active' : ''}`;
    card.id = `card-${ch.id}`;
    card.onclick = () => switchChannel(ch);

    const liveBadge = ch.live ? `<span class="live-dot" title="Verified Live"></span>` : ``;

    card.innerHTML = `
      <div class="channel-card-icon">${ch.icon}</div>
      <div class="channel-card-title">${ch.name}</div>
      <div class="channel-card-tag">${ch.cat}</div>
      ${liveBadge}
    `;
    grid.appendChild(card);
  });
}

function filterChannels() {
  const q = document.getElementById('channelSearch').value.toLowerCase().trim();
  const filtered = channelData.filter(ch => {
    const matchCat = (currentFilter === 'all' || ch.cat.toLowerCase() === currentFilter.toLowerCase());
    const matchQuery = ch.name.toLowerCase().includes(q) || ch.cat.toLowerCase().includes(q);
    return matchCat && matchQuery;
  });
  renderChannels(filtered);
}

function filterCategory(cat, el) {
  currentFilter = cat;
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  filterChannels();
}

function switchChannel(channel) {
  if (isRecording) {
    showToast('⚠️ Stop recording before changing channels!');
    return;
  }
  activeChannel = channel;
  document.querySelectorAll('.channel-card').forEach(c => c.classList.remove('active'));
  const activeEl = document.getElementById(`card-${channel.id}`);
  if (activeEl) activeEl.classList.add('active');

  document.getElementById('currentChannelName').innerText = channel.name;
  document.getElementById('currentChannelUrl').innerText = channel.url;
  document.getElementById('channelLogo').innerText = channel.icon;

  playStream(channel.url);
  showToast(`Switched to ${channel.name}`);
}

// --- 2. HLS PLAYBACK & DYNAMIC RESOLUTION ---
function playStream(url) {
  const video = document.getElementById('players');
  if (!video) return;

  if (currentHls) {
    currentHls.destroy();
    currentHls = null;
  }

  // Reset quality options
  resetQualityMenu();

  if (Hls.isSupported()) {
    const hls = new Hls({
      enableWorker: true,
      lowLatencyMode: true,
      backBufferLength: 60
    });
    currentHls = hls;
    hls.loadSource(url);
    hls.attachMedia(video);

    hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
      populateQualityMenu(data.levels);
      video.play().then(() => updatePlayIcon(true)).catch(() => updatePlayIcon(false));
    });

    hls.on(Hls.Events.LEVEL_SWITCHED, (event, data) => {
      const level = hls.levels[data.level];
      if (level && currentLevelIndex === -1) {
        document.getElementById('ytQualityText').innerText = `AUTO (${level.height}p)`;
      }
    });

    hls.on(Hls.Events.ERROR, (event, data) => {
      if (data.fatal) {
        switch(data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            hls.startLoad();
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            hls.recoverMediaError();
            break;
          default:
            hls.destroy();
            break;
        }
      }
    });
  } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = url;
    video.play();
    updatePlayIcon(true);
  }
}

// --- 3. DYNAMIC RESOLUTION MENU BUILDER ---
function resetQualityMenu() {
  const list = document.getElementById('ytQualityOptions');
  if (!list) return;
  list.innerHTML = `
    <div class="yt-quality-item active" onclick="setResolution(-1, 'Auto')">
      <span class="yt-check">✓</span>
      <span>Auto</span>
    </div>
  `;
  document.getElementById('ytQualityText').innerText = 'AUTO';
  currentLevelIndex = -1;
}

function populateQualityMenu(levels) {
  const list = document.getElementById('ytQualityOptions');
  if (!list || !levels || levels.length === 0) return;

  list.innerHTML = `
    <div class="yt-quality-item ${currentLevelIndex === -1 ? 'active' : ''}" onclick="setResolution(-1, 'Auto')">
      <span class="yt-check">✓</span>
      <span>Auto (Multi-bitrate)</span>
    </div>
  `;

  // Sort descending by height
  const sorted = levels.map((lvl, idx) => ({ ...lvl, origIdx: idx }))
                       .sort((a, b) => (b.height || 0) - (a.height || 0));

  sorted.forEach(lvl => {
    const height = lvl.height || Math.round((lvl.bitrate || 0) / 1000);
    const label = height > 700 ? `${height}p HD` : `${height}p`;
    const item = document.createElement('div');
    item.className = `yt-quality-item ${currentLevelIndex === lvl.origIdx ? 'active' : ''}`;
    item.onclick = (e) => {
      e.stopPropagation();
      setResolution(lvl.origIdx, label);
    };
    item.innerHTML = `
      <span class="yt-check">✓</span>
      <span>${label}</span>
    `;
    list.appendChild(item);
  });
}

function setResolution(levelIndex, label) {
  if (!currentHls) return;
  currentHls.currentLevel = levelIndex;
  currentLevelIndex = levelIndex;

  document.getElementById('ytQualityText').innerText = label.toUpperCase();

  // Update active checkmarks
  const items = document.querySelectorAll('.yt-quality-item');
  items.forEach(it => it.classList.remove('active'));
  if (event && event.currentTarget) {
    event.currentTarget.classList.add('active');
  }

  toggleQualityDropdown(false);
  showToast(`📺 Resolution switched to: ${label}`);
}

function toggleQualityDropdown(forceState) {
  const dropdown = document.getElementById('ytQualityDropdown');
  if (!dropdown) return;
  const isShow = forceState !== undefined ? forceState : !dropdown.classList.contains('show');
  if (isShow) dropdown.classList.add('show');
  else dropdown.classList.remove('show');
}

// --- 4. YOUTUBE PLAYER CONTROLS (PLAY, VOLUME, FULLSCREEN, PiP) ---
function togglePlayPause() {
  const video = document.getElementById('players');
  if (!video) return;
  if (video.paused) {
    video.play();
    updatePlayIcon(true);
    triggerCenterAnimation(true);
  } else {
    video.pause();
    updatePlayIcon(false);
    triggerCenterAnimation(false);
  }
}

function updatePlayIcon(isPlaying) {
  const icon = document.getElementById('ytPlayIcon');
  if (!icon) return;
  if (isPlaying) {
    icon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>'; // Pause icon
  } else {
    icon.innerHTML = '<path d="M8 5v14l11-7z"/>'; // Play icon
  }
}

function triggerCenterAnimation(isPlaying) {
  const wrap = document.getElementById('ytCenterAction');
  const btn = document.getElementById('ytCenterBtn');
  if (!wrap || !btn) return;
  const icon = btn.querySelector('svg');
  if (isPlaying) {
    icon.innerHTML = '<path d="M8 5v14l11-7z"/>';
  } else {
    icon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
  }
  wrap.classList.add('show-briefly');
  setTimeout(() => wrap.classList.remove('show-briefly'), 500);
}

function setVolume(val) {
  const video = document.getElementById('players');
  if (!video) return;
  video.volume = val;
  video.muted = (val === 0);
  updateVolumeIcon(video.muted ? 0 : val);
}

function toggleMute() {
  const video = document.getElementById('players');
  if (!video) return;
  video.muted = !video.muted;
  const slider = document.getElementById('ytVolRange');
  if (video.muted) {
    slider.value = 0;
    updateVolumeIcon(0);
  } else {
    slider.value = video.volume || 1;
    updateVolumeIcon(video.volume || 1);
  }
}

function updateVolumeIcon(vol) {
  const icon = document.getElementById('ytVolIcon');
  if (!icon) return;
  if (vol === 0) {
    icon.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
  } else if (vol < 0.5) {
    icon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>';
  } else {
    icon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>';
  }
}

function togglePiP() {
  const video = document.getElementById('players');
  if (document.pictureInPictureElement) document.exitPictureInPicture();
  else if (document.pictureInPictureEnabled) video.requestPictureInPicture();
}

function toggleFullscreen() {
  const vp = document.getElementById('videoViewport');
  const icon = document.getElementById('ytFsIcon');
  if (!document.fullscreenElement) {
    vp.requestFullscreen().catch(err => alert(err.message));
    if (icon) icon.innerHTML = '<path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"/>'; // exit fs icon
  } else {
    document.exitFullscreen();
    if (icon) icon.innerHTML = '<path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>'; // enter fs icon
  }
}

// Auto-hide controls timer
let idleTimeout = null;
function handleUserActivity() {
  const vp = document.getElementById('videoViewport');
  if (!vp) return;
  vp.classList.remove('yt-idle');
  clearTimeout(idleTimeout);
  idleTimeout = setTimeout(() => {
    const video = document.getElementById('players');
    if (video && !video.paused) {
      vp.classList.add('yt-idle');
      toggleQualityDropdown(false);
    }
  }, 3500);
}

// --- 5. STREAM RECORDER (SAVE MP4/WEBM LOCALLY) ---
let mediaRecorder = null;
let recordedChunks = [];
let isRecording = false;
let recordStartTime = null;
let recordInterval = null;

function getSupportedMimeType() {
  const types = [
    'video/mp4;codecs=avc1,mp4a.40.2',
    'video/mp4',
    'video/webm;codecs=vp9,opus',
    'video/webm;codecs=vp8,opus',
    'video/webm'
  ];
  for (const t of types) {
    if (MediaRecorder.isTypeSupported(t)) return t;
  }
  return '';
}

function toggleRecording() {
  if (!isRecording) startRecording();
  else stopRecording();
}

function startRecording() {
  const video = document.getElementById('players');
  const stream = video.captureStream ? video.captureStream() : (video.mozCaptureStream ? video.mozCaptureStream() : null);

  if (!stream) {
    showToast('❌ Browser does not support stream capture.');
    return;
  }

  const mimeType = getSupportedMimeType();
  recordedChunks = [];

  try {
    mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
  } catch (err) {
    showToast('❌ MediaRecorder error: ' + err.message);
    return;
  }

  mediaRecorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) recordedChunks.push(e.data);
  };

  mediaRecorder.onstop = saveRecordedFile;
  mediaRecorder.start(1000);
  isRecording = true;
  recordStartTime = Date.now();

  const btn = document.getElementById('btnRecord');
  btn.classList.add('recording');
  document.getElementById('recBtnLabel').innerText = 'Stop & Save Video';
  document.getElementById('recOverlay').style.display = 'flex';

  recordInterval = setInterval(updateRecTimer, 500);
  showToast('⏺️ Recording started...');
}

function updateRecTimer() {
  const diff = Math.floor((Date.now() - recordStartTime) / 1000);
  const mins = String(Math.floor(diff / 60)).padStart(2, '0');
  const secs = String(diff % 60).padStart(2, '0');
  document.getElementById('recTimer').innerText = `${mins}:${secs}`;
}

function stopRecording() {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') return;
  mediaRecorder.stop();
  isRecording = false;
  clearInterval(recordInterval);

  const btn = document.getElementById('btnRecord');
  btn.classList.remove('recording');
  document.getElementById('recBtnLabel').innerText = 'Record Stream (MP4)';
  document.getElementById('recOverlay').style.display = 'none';
  document.getElementById('recTimer').innerText = '00:00';
}

function saveRecordedFile() {
  const mimeType = mediaRecorder.mimeType || 'video/mp4';
  const isMp4 = mimeType.includes('mp4');
  const ext = isMp4 ? 'mp4' : 'webm';
  const blob = new Blob(recordedChunks, { type: mimeType });

  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const timeStr = new Date().toISOString().replace(/[:.]/g, '-');
  a.href = url;
  a.download = `${activeChannel.name.replace(/\s+/g, '_')}_Record_${timeStr}.${ext}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);

  showToast(`✅ Saved ${a.download} (${(blob.size / (1024 * 1024)).toFixed(2)} MB) to your PC!`);
}

function takeSnapshot() {
  const video = document.getElementById('players');
  if (!video.videoWidth || !video.videoHeight) {
    showToast('⚠️ No active video frame to capture.');
    return;
  }
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const a = document.createElement('a');
  const timeStr = new Date().toISOString().replace(/[:.]/g, '-');
  a.href = canvas.toDataURL('image/png');
  a.download = `${activeChannel.name.replace(/\s+/g, '_')}_Snapshot_${timeStr}.png`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  showToast(`📸 Snapshot saved: ${a.download}`);
}

function showToast(msg) {
  const tc = document.getElementById('toastContainer');
  if (!tc) return;
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = msg;
  tc.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateY(10px)';
    t.style.transition = 'all 0.3s';
    setTimeout(() => tc.removeChild(t), 300);
  }, 3500);
}

// Global Shortcuts & Events Setup
window.addEventListener('DOMContentLoaded', () => {
  const vp = document.getElementById('videoViewport');
  const video = document.getElementById('players');
  const playBtn = document.getElementById('ytPlayBtn');
  const muteBtn = document.getElementById('ytMuteBtn');
  const volRange = document.getElementById('ytVolRange');
  const qualityBtn = document.getElementById('ytQualityBtn');

  if (video) {
    video.addEventListener('playing', hideStandbyOverlay);
  }

  renderChannels(channelData);
  switchChannel(channelData[0]);

  if (playBtn) playBtn.onclick = (e) => { e.stopPropagation(); togglePlayPause(); };
  if (muteBtn) muteBtn.onclick = (e) => { e.stopPropagation(); toggleMute(); };
  if (volRange) volRange.oninput = (e) => { e.stopPropagation(); setVolume(parseFloat(e.target.value)); };
  if (qualityBtn) qualityBtn.onclick = (e) => { e.stopPropagation(); toggleQualityDropdown(); };

  // Click video viewport to play/pause
  if (vp) {
    vp.onclick = (e) => {
      // Don't toggle if clicking inside controls or quality menu
      if (e.target.closest('.yt-controls-wrapper')) return;
      togglePlayPause();
    };
    vp.ondblclick = (e) => {
      if (e.target.closest('.yt-controls-wrapper')) return;
      toggleFullscreen();
    };
    vp.onmousemove = handleUserActivity;
    vp.onmouseleave = () => {
      if (video && !video.paused) vp.classList.add('yt-idle');
    };
  }

  // Close quality dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.yt-quality-container')) {
      toggleQualityDropdown(false);
    }
  });

  // Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    if (e.code === 'Space') {
      e.preventDefault();
      togglePlayPause();
    } else if (e.code === 'KeyF') {
      e.preventDefault();
      toggleFullscreen();
    } else if (e.code === 'KeyM') {
      e.preventDefault();
      toggleMute();
    } else if (e.code === 'KeyR') {
      e.preventDefault();
      toggleRecording();
    } else if (e.code === 'KeyS') {
      e.preventDefault();
      takeSnapshot();
    }
  });
});

function startStreamPlayback() {
  const video = document.getElementById('players');
  hideStandbyOverlay();
  if (video) {
    video.play().then(() => {
      updatePlayIcon(true);
    }).catch(err => {
      console.log('Playback interaction error:', err);
      // Fallback: start muted if browser restricts sound
      video.muted = true;
      video.play().then(() => {
        updatePlayIcon(true);
        showToast('🔈 Playing muted due to browser policy. Click speaker to unmute!');
      }).catch(e => {
        console.log('Autoplay fallback error:', e);
      });
    });
  }
}

function hideStandbyOverlay() {
  const overlay = document.getElementById('standbyOverlay');
  if (overlay) overlay.classList.add('hidden');
}

function showStandbyOverlay(name, icon, cat) {
  const overlay = document.getElementById('standbyOverlay');
  if (overlay) {
    const titleEl = document.getElementById('standbyTitle');
    const logoEl = document.getElementById('standbyLogo');
    const statusEl = document.getElementById('standbyStatus');
    const subEl = document.getElementById('standbySubtitle');
    const playBtnText = document.getElementById('standbyPlayBtnText');
    
    if (titleEl) titleEl.innerText = name;
    if (logoEl) logoEl.innerText = icon || '📺';
    if (statusEl) statusEl.innerText = `Ready to Stream • ${name} (${cat || 'Live'})`;
    if (subEl) subEl.innerText = `${cat || 'Live'} Satellite Feed • Instant HLS Stream`;
    if (playBtnText) playBtnText.innerText = `▶ Watch ${name}`;
    overlay.classList.remove('hidden');
  }
}

function quickJumpCategory(catName) {
  const pills = document.querySelectorAll('.pill');
  for (const p of pills) {
    if (p.innerText.includes(catName)) {
      p.click();
      break;
    }
  }
  // Also switch to first channel in that category
  const match = channelData.find(c => c.cat.toLowerCase() === catName.toLowerCase());
  if (match) {
    switchChannel(match);
  }
}

