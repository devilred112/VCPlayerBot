#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from utils import LOGGER
try:
   import os
   import heroku3
   from dotenv import load_dotenv
   from ast import literal_eval as is_enabled

except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


class Config:
    #Telegram API Stuffs
    load_dotenv()  # load enviroment variables from .env file
    ADMIN = os.environ.get("ADMINS", '')
    SUDO = [int(admin) for admin in (ADMIN).split()] # Exclusive for heroku vars configuration.
    ADMINS = [int(admin) for admin in (ADMIN).split()] #group admins will be appended to this list.
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")

    #Stream Chat and Log Group
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")

    #Stream 
    STREAM_URL=os.environ.get("STARTUP_STREAM", "https://www.youtube.com/watch?v=zcrUCvBD16k")
   
    #Database
    DATABASE_URI=os.environ.get("DATABASE_URI", None)
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "VCPlayerBot")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", None)
    APP_NAME=os.environ.get("HEROKU_APP_NAME", None)


    #Optional Configuration
    SHUFFLE=is_enabled(os.environ.get("SHUFFLE", 'True'))
    ADMIN_ONLY=is_enabled(os.environ.get("ADMIN_ONLY", "False"))
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", False)
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    #others
    
    RECORDING_DUMP=os.environ.get("RECORDING_DUMP", False)
    RECORDING_TITLE=os.environ.get("RECORDING_TITLE", False)
    TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")    
    IS_VIDEO=is_enabled(os.environ.get("IS_VIDEO", 'True'))
    IS_LOOP=is_enabled(os.environ.get("IS_LOOP", 'True'))
    DELAY=int(os.environ.get("DELAY", '10'))
    PORTRAIT=is_enabled(os.environ.get("PORTRAIT", 'False'))
    IS_VIDEO_RECORD=is_enabled(os.environ.get("IS_VIDEO_RECORD", 'True'))
    DEBUG=is_enabled(os.environ.get("DEBUG", 'False'))
    PTN=is_enabled(os.environ.get("PTN", "False"))

    #Quality vars
    E_BITRATE=os.environ.get("BITRATE", False)
    E_FPS=os.environ.get("FPS", False)
    CUSTOM_QUALITY=os.environ.get("QUALITY", "100")

    #Search filters for cplay
    FILTERS =  [filter.lower() for filter in (os.environ.get("FILTERS", "video document")).split(" ")]


    #Dont touch these, these are not for configuring player
    GET_FILE={}
    DATA={}
    STREAM_END={}
    SCHEDULED_STREAM={}
    DUR={}
    msg = {}

    SCHEDULE_LIST=[]
    playlist=[]
    CONFIG_LIST = ["ADMINS", "IS_VIDEO", "IS_LOOP", "REPLY_PM", "ADMIN_ONLY", "SHUFFLE", "EDIT_TITLE", "CHAT", 
    "SUDO", "REPLY_MESSAGE", "STREAM_URL", "DELAY", "LOG_GROUP", "SCHEDULED_STREAM", "SCHEDULE_LIST", 
    "IS_VIDEO_RECORD", "IS_RECORDING", "WAS_RECORDING", "RECORDING_TITLE", "PORTRAIT", "RECORDING_DUMP", "HAS_SCHEDULE", 
    "CUSTOM_QUALITY"]

    STARTUP_ERROR=None

    ADMIN_CACHE=False
    CALL_STATUS=False
    YPLAY=False
    YSTREAM=False
    CPLAY=False
    STREAM_SETUP=False
    LISTEN=False
    STREAM_LINK=False
    IS_RECORDING=False
    WAS_RECORDING=False
    PAUSE=False
    MUTED=False
    HAS_SCHEDULE=None
    IS_ACTIVE=None
    VOLUME=100
    CURRENT_CALL=None
    BOT_USERNAME=None
    USER_ID=None

    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    if not API_KEY or \
       not APP_NAME:
       HEROKU_APP=None
    else:
       HEROKU_APP=heroku3.from_key(API_KEY).apps()[APP_NAME]


    if EDIT_TITLE in ["NO", 'False']:
        EDIT_TITLE=False
        LOGGER.info("Title Editing turned off")
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        REPLY_PM=True
        LOGGER.info("Reply Message Found, Enabled PM MSG")
    else:
        REPLY_MESSAGE=False
        REPLY_PM=False

    if E_BITRATE:
       try:
          BITRATE=int(E_BITRATE)
       except:
          LOGGER.error("Invalid bitrate specified.")
          E_BITRATE=False
          BITRATE=48000
       if not BITRATE >= 48000:
          BITRATE=48000
    else:
       BITRATE=48000
    
    if E_FPS:
       try:
          FPS=int(E_FPS)
       except:
          LOGGER.error("Invalid FPS specified")
          E_FPS=False
       if not FPS >= 30:
          FPS=30
    else:
       FPS=30
    try:
       CUSTOM_QUALITY=int(CUSTOM_QUALITY)
       if CUSTOM_QUALITY > 100:
          CUSTOM_QUALITY = 100
          LOGGER.warning("maximum quality allowed is 100, invalid quality specified. Quality set to 100")
       elif CUSTOM_QUALITY < 10:
          LOGGER.warning("Minimum Quality allowed is 10., Qulaity set to 10")
          CUSTOM_QUALITY = 10
       if  66.9  < CUSTOM_QUALITY < 100:
          if not E_BITRATE:
             BITRATE=48000
       elif 50 < CUSTOM_QUALITY < 66.9:
          if not E_BITRATE:
             BITRATE=36000
       else:
          if not E_BITRATE:
             BITRATE=24000
    except:
       if CUSTOM_QUALITY.lower() == 'high':
          CUSTOM_QUALITY=100
       elif CUSTOM_QUALITY.lower() == 'medium':
          CUSTOM_QUALITY=66.9
       elif CUSTOM_QUALITY.lower() == 'low':
          CUSTOM_QUALITY=50
       else:
          LOGGER.warning("Invalid QUALITY specified.Defaulting to High.")
          CUSTOM_QUALITY=100



    #help strings 
    PLAY_HELP="""
__Bu se??eneklerden herhangi birini kullanarak oynayabilirsiniz.__

1. Bir YouTube ba??lant??s??ndan bir video oynat??n.
Command: **/play**
__Bunu bir YouTube ba??lant??s??na yan??t olarak veya ba??lant??y?? birlikte ilet komutu olarak kullanabilirsiniz. veya bunu YouTube'da aramak i??in iletiye yan??t olarak.__

2. Bir telgraf dosyas??ndan oynat??n.
Command: **/play**
__Desteklenen bir medyaya yan??t verin (video ve belgeler veya ses dosyas??).__
Not: __Her iki durumda da /fplay ayr??ca y??neticiler taraf??ndan s??ran??n bitmesini beklemeden ??ark??y?? hemen ??almak i??in kullan??labilir.__

3. Bir YouTube oynatma listesinden oynat??n
Command: **/yplay**
__??nce @GetPlaylistBot veya @DumpPlaylist'ten bir ??alma listesi dosyas?? al??n ve ??alma listesi dosyas??na yan??t verin.__

4. Canl?? Ak????
Command: **/stream**
__Ak???? olarak oynatmak i??in bir canl?? yay??n URL'si veya herhangi bir do??rudan URL iletin.__

5. Eski bir ??alma listesini i??e aktar??n.
Command: **/import**
__??nceden d????a aktar??lan bir oynatma listesi dosyas??na yan??t verin. __

6. Kanal Oynatma
Command: **/cplay**
__Verilen kanaldaki t??m dosyalar?? oynatmak i??in `/cplay kanal kullan??c?? ad?? veya kanal kimli??i`ni kullan??n.
Varsay??lan olarak hem video dosyalar?? hem de belgeler oynat??lacakt??r. `FILTERS` de??i??kenini kullanarak dosya t??r??n?? ekleyebilir veya kald??rabilirsiniz.
??rne??in, kanaldan ses, video ve belge ak?????? yapmak i??in `/env FILTERS video belge sesi`ni kullan??n. Yaln??zca sese ihtiyac??n??z varsa, `/env FILTERS video audio` vb. ????elerini kullanabilirsiniz.
Bir kanaldaki dosyalar?? STARTUP_STREAM olarak ayarlamak, b??ylece dosyalar bot ba??lang??c??nda otomatik olarak oynatma listesine eklenecektir. `/env STARTUP_STREAM kanal kullan??c?? ad?? veya kanal kimli??i' kullan??n

Herkese a????k kanallar i??in '@' ile birlikte kanallar??n kullan??c?? ad??n?? ve ??zel kanallar i??in kanal kimli??ini kullanman??z gerekti??ini unutmay??n.
??zel kanallar i??in hem bot hem de KULLANICI hesab??n??n kanal??n ??yesi oldu??undan emin olun.__
"""
    SETTINGS_HELP="""
**Oyuncunuzu ihtiya??lar??n??za g??re kolayca ??zelle??tirebilirsiniz. A??a????daki konfig??rasyonlar mevcuttur:**

????Command: **/settings**

????Mevcut YAPILANDIRMALAR:

**Oyuncu Modu** - __Bu, oynat??c??n??z?? 7/24 m??zik ??alar olarak veya yaln??zca s??rada ??ark?? oldu??unda ??al????t??rman??za olanak tan??r.
Devre d?????? b??rak??l??rsa, oynatma listesi bo?? oldu??unda oyuncu aramadan ????kar.
Aksi takdirde, oynatma listesi kimli??i bo?? oldu??unda STARTUP_STREAM yay??nlan??r.__

**Video Etkin** - __Bu, ses ve video aras??nda ge??i?? yapman??z?? sa??lar.
devre d?????? b??rak??l??rsa, video dosyalar?? ses olarak oynat??lacakt??r.__

**Yaln??zca Y??netici** - __Bunu etkinle??tirmek, y??netici olmayan kullan??c??lar??n oynatma komutunu kullanmas??n?? k??s??tlar.__

**Ba??l?????? D??zenle** - __Bunu etkinle??tirmek, VideoChat ba??l??????n??z?? o anda ??almakta olan ??ark?? ad??na g??re d??zenler.__

**Kar????t??rma Modu** - __Bunu etkinle??tirmek, bir oynatma listesini i??e aktard??????n??zda veya /yplay'i kulland??????n??zda oynatma listesini kar????t??r??r __

**Otomatik Yan??t** - __Oynayan kullan??c?? hesab??n??n PM mesajlar??n?? yan??tlay??p yan??tlamamay?? se??in.
`REPLY_MESSAGE` konfig??rasyonunu kullanarak ??zel bir cevap mesaj?? olu??turabilirsiniz.__
"""
    SCHEDULER_HELP="""
__VCPlayer, bir ak???? planlaman??za olanak tan??r.
Bu, gelecekteki bir tarih i??in bir ak???? planlayabilece??iniz ve planlanan tarihte ak??????n otomatik olarak oynat??laca???? anlam??na gelir.
??u anda bir y??ll??k bir yay??n ak?????? planlayabilirsiniz!!. Bir veritaban?? kurdu??unuzdan emin olun, aksi takdirde oynat??c?? yeniden ba??lad??????nda programlar??n??z?? kaybedersiniz. __

Command: **/schedule**

__Bir dosyaya veya youtube videosuna veya hatta bir metin mesaj??na program komutuyla yan??t verin.
Cevaplanan medya veya youtube videosu planlanacak ve planlanan tarihte oynat??lacakt??r.
IST'de programlama zaman?? varsay??land??r ve 'TIME_ZONE' yap??land??rmas??n?? kullanarak saat dilimini de??i??tirebilirsiniz.__

Command: **/slist**
__Mevcut planlanm???? ak????lar??n??z?? g??r??nt??leyin.__

Command: **/cancel**
__Bir program?? zamanlama kimli??ine g??re iptal edin, /slist komutunu kullanarak zamanlama kimli??ini alabilirsiniz__

Command: **/cancelall**
__Planlanm???? t??m ak????lar?? iptal edin__"""
    RECORDER_HELP="""
__VCPlayer ile t??m g??r??nt??l?? sohbetlerinizi kolayca kaydedebilirsiniz.
Varsay??lan olarak telgraf, maksimum 4 saat kay??t yapman??z?? sa??lar.
4 saat sonra kay??t otomatik olarak yeniden ba??lat??larak bu limit a????lmaya ??al??????lm????t??r__

Command: **/record**

MEVCUT YAPILANDIRMALAR:
1. Video Kaydet: __Etkinle??tirilirse, ak??????n hem videosu hem de sesi kaydedilir, aksi takdirde yaln??zca ses kaydedilir.__

2. Video boyutu: __Kayd??n??z i??in dikey ve yatay boyutlar aras??nda se??im yap??n__

3. ??zel Kay??t Ba??l??????: __Kay??tlar??n??z i??in ??zel bir kay??t ba??l?????? ayarlay??n. Bunu yap??land??rmak i??in /rtitle komutunu kullan??n.
??zel ba??l?????? kapatmak i??in `/rtitle False `__ kullan??n

4. Kay??t Aptal: __T??m kay??tlar??n??z?? bir kanala iletmeyi ayarlayabilirsiniz, aksi takdirde kay??tlar ak???? hesab??n??n kay??tl?? mesajlar??na g??nderilece??inden bu yararl?? olacakt??r.
`RECORDING_DUMP` yap??land??rmas??n?? kullanarak kurulum.__

?????? vcplayer ile bir kayda ba??larsan??z, vcplayer ile ayn?? ??eyi durdurdu??unuzdan emin olun.
"""

    CONTROL_HELP="""
__VCPlayer, ak????lar??n??z?? kolayca kontrol etmenizi sa??lar__
1. Bir ??ark??y?? atlay??n.
Command: **/skip**
__??ark??y?? o konumda atlamak i??in 2'den b??y??k bir say?? iletebilirsiniz.__

2. Oynat??c??y?? duraklat??n.
Command: **/pause**

3. Oynat??c??y?? devam ettirin.
Command: **/resume**

4. Ses Seviyesini De??i??tirin.
Command: **/volume**
__Sesi 1-200 aras??nda ge??irin.__

5. VC'den ayr??l??n.
Command: **/leave**

6. ??alma listesini kar????t??r??n.
Command: **/shuffle**

7. Mevcut ??alma listesi s??ras??n?? temizleyin.
Command: **/clearplaylist**

8. Videoyu aray??n.
Command: **/seek**
__Atlanacak saniye say??s??n?? ge??ebilirsiniz. ??rnek: 10 saniye atlamak i??in /seek 10. / 10 saniye geri sarmak i??in -10 ara.__

9. Oynat??c??y?? sessize al??n.
Command: **/vcmute**

10. Oynat??c??n??n sesini a????n.
Command : **/vcunmute**

11. ??alma listesini g??sterir.
Command: **/playlist** 
__Kontrol d????meleriyle g??stermek i??in /player'?? kullan??n__
"""

    ADMIN_HELP="""
__VCPlayer, y??neticileri kontrol etmenizi sa??lar, yani y??netici ekleyebilir ve kolayca kald??rabilirsiniz.
Daha iyi bir deneyim i??in bir MongoDb veritaban?? kullan??lmas?? ??nerilir, aksi takdirde t??m y??neticileriniz yeniden ba??latt??ktan sonra s??f??rlan??r.__

Command: **/vcpromote**
__Bir y??neticiyi, kullan??c?? ad?? veya kullan??c?? kimli??i ile ya da o kullan??c?? mesaj??na yan??t vererek terfi ettirebilirsiniz.__

Command: **/vcdemote**
__Y??netici listesinden bir y??neticiyi kald??r??n__

Command: **/refresh**
__Sohbetin y??netici listesini yenileyin__"""

    MISC_HELP="""
Command: **/export**
__VCPlayer, mevcut ??alma listenizi ileride kullanmak ??zere d????a aktarman??za olanak tan??r.__
__Size bir json dosyas?? g??nderilecek ve ayn??s?? /import komutu ile birlikte kullan??labilir.__

Command : **/logs**
__Oyuncunuz bir ??eyler ters gittiyse, /logs kullanarak g??nl??kleri kolayca kontrol edebilirsiniz.__

Command : **/env**
__Yap??land??rma de??i??kenlerinizi /env komutuyla ayarlay??n.__
__??rnek: Bir __ `REPLY_MESSAGE` kurmak i??in __use__ `/env REPLY_MESSAGE=Hey, PM'ime spam g??ndermek yerine @subin_works'e g??z at??n`__
__Bir yap??land??rma de??i??kenini bunun i??in bir de??er atlayarak silebilirsiniz, ??rnek:__ `/env LOG_GROUP=` __bu, mevcut LOG_GROUP yap??land??rmas??n?? siler.__

Command: **/config**
__/env** kullan??m??yla ayn??

Command: **/update**
__En son de??i??ikliklerle botunuzu g??nceller__

??pucu: __Kullan??c?? hesab??n?? ve bot hesab??n?? ba??ka bir gruba ve yeni gruptaki herhangi bir komutu ekleyerek CHAT yap??land??rmas??n?? kolayca de??i??tirebilirsiniz__
"""
    ENV_HELP="""
**Bunlar, mevcut yap??land??r??labilir de??i??kenlerdir ve her birini /env komutunu kullanarak ayarlayabilirsiniz**

**Zorunlu De??i??kenler**
1. "API_ID" : __[my.telegram.org'dan](https://my.telegram.org/) al??n??z__
2. `API_HASH` : __[my.telegram.org'dan](https://my.telegram.org/) al??n??z__

3. `BOT_TOKEN` : __[@Botfather](https://telegram.dog/BotFather)__

4. `SESSION_STRING` : __Generate From here [GenerateStringName](https://repl.it/@subinps/getStringName)__

5. `CHAT` : __Bot'un M??zik ??ald?????? Kanal??n/Grubun Kimli??i.__

6. `STARTUP_STREAM` : __Bu, botun ba??lat??lmas?? ve yeniden ba??lat??lmas?? s??ras??nda yay??nlanacak.
Herhangi bir STREAM_URL'yi veya herhangi bir videonun do??rudan ba??lant??s??n?? veya bir Youtube Canl?? ba??lant??s??n?? kullanabilirsiniz.
Ayr??ca YouTube Oynatma Listesini de kullanabilirsiniz. Oynatma listeniz i??in [PlayList Dumb](https://telegram.dog/DumpPlaylist) adresinden bir Telegram Ba??lant??s?? bulabilir veya [PlayList Extract](https://telegram.dog/GetAPlaylistbot) adresinden bir Oynatma Listesi alabilirsiniz. .
Oynatma Listesi ba??lant??s?? "https://t.me/DumpPlaylist/xxx" bi??iminde olmal??d??r.
Bir kanaldaki dosyalar?? ba??lang???? ak?????? olarak da kullanabilirsiniz. Bunun i??in STARTUP_STREAM de??eri olarak kanal??n kanal kimli??ini veya kanal kullan??c?? ad??n?? kullan??n.
Kanal oynatma hakk??nda daha fazla bilgi i??in oynat??c?? b??l??m??ndeki yard??m?? okuyun.__

**??nerilen Opsiyonel De??i??kenler**

1. `DATABASE_URI`: __MongoDB veritaban?? URL'si, [mongodb](https://cloud.mongodb.com) adresinden al??n. Bu iste??e ba??l?? bir de??i??kendir, ancak t??m ??zellikleri deneyimlemek i??in bunu kullanman??z ??nerilir.__

2. `HEROKU_API_KEY`: __Heroku API anahtar??n??z. [Buradan](https://dashboard.heroku.com/account/applications/authorizations/new)__ bir tane edinin

3. `HEROKU_APP_NAME`: __Heroku uygulaman??z??n ad??.__

4. `FILTERS`: __Kanal oynatma dosyas?? aramas?? i??in filtreler. Oynat??c?? b??l??m??ndeki cplay ile ilgili yard??m?? okuyun.__

**Di??er Opsiyonel De??i??kenler**
1. `LOG_GROUP` : __CHAT bir Grup ise Oynatma Listesi g??nderilecek grup__

2. `ADMINS` : __Y??netici komutlar??n?? kullanabilen kullan??c??lar??n kimli??i.__

3. `REPLY_MESSAGE` : __Kullan??c?? hesab??na PM ile mesaj atanlara cevap. Bu ??zelli??e ihtiyac??n??z yoksa bo?? b??rak??n. (Mongodb eklendiyse d????meler arac??l??????yla yap??land??r??labilir. /ayarlar?? kullan??n)__

4. `ADMIN_ONLY` : __Pass `True` Sadece `CHAT` y??neticileri i??in /play komutu vermek istiyorsan??z. Varsay??lan olarak /play herkes i??in mevcuttur.(Mongodb eklendiyse d????meler arac??l??????yla yap??land??r??labilir. /ayarlar?? kullan??n)__

5. `DATABASE_NAME`: __mongodb veritaban??n??z i??in veritaban?? ad??.mongodb__

6. `SHUFFLE` : __??alma listelerini kar????t??rmak istemiyorsan??z 'Yanl????' yap??n. (D????meler arac??l??????yla yap??land??r??labilir)__

7. `EDIT_TITLE` : __Bot'un ??alan ??ark??ya g??re g??r??nt??l?? sohbet ba??l??????n?? d??zenlemesini istemiyorsan??z 'Yanl????' yap??n. (Mongodb eklendiyse d????meler arac??l??????yla yap??land??r??labilir. /ayarlar?? kullan??n)__

8. `RECORDING_DUMP` : __G??r??nt??l?? sohbet kay??tlar??n?? bo??altmak i??in y??netici olarak KULLANICI hesab?? olan bir Kanal Kimli??i.__

9. `RECORDING_TITLE`: __G??r??nt??l?? sohbet kay??tlar??n??z i??in ??zel bir ba??l??k.__

10. `TIME_ZONE` : __??lkenizin Saat Dilimi, varsay??lan olarak IST__

11. `IS_VIDEO_RECORD` : __Video kaydetmek istemiyorsan??z 'Yanl????' yap??n ve yaln??zca ses kaydedilecektir.(Mongodb eklendiyse d????meler arac??l??????yla yap??land??r??labilir. /kaydet kullan)__

12. `IS_LOOP` ; __7/24 G??r??nt??l?? Sohbet istemiyorsan??z 'Yanl????' yap??n. (Mongodb eklendiyse d????meler arac??l??????yla yap??land??r??labilir. /ayarlar?? kullan??n)__

13. `IS_VIDEO` : __??alar?? videosuz bir m??zik ??alar olarak kullanmak istiyorsan??z 'Yanl????' yap??n. (Mongodb eklendiyse d????meler arac??l??????yla yap??land??r??labilir. /ayarlar?? kullan??n)__

14. `PORTRAIT`: __Video kayd??n?? portre modunda istiyorsan??z 'Do??ru' yap??n. (Mongodb eklendiyse butonlarla yap??land??r??labilir. /record kullan??n)__

15. `DELAY` : __Komutlar??n silinmesi i??in zaman s??n??r??n?? se??in. varsay??lan olarak 10 saniye.__

16. `QUALITY` : __G??r??nt??l?? sohbetin kalitesini ??zelle??tirin, a??a????dakilerden birini kullan??n: `high`, `medium`, `low`.__

17. `BITRATE` : __Ses bit h??z?? (de??i??tirilmesi ??nerilmez).__

18. `FPS` : __ Oynat??lacak videonun Fps'si (De??i??tirilmesi ??nerilmez.)__

"""
