from linebot.models import (
    ImageSendMessage,
    TextSendMessage,
)

replies_massa = [
    TextSendMessage(text='M****? KARTU KUNING MAS MBA!'),
    TextSendMessage(text='Ga ada m*ss* di HMIF, adanya anggota'),
    TextSendMessage(text='M****? Tolong ini ditendang dong'),
    TextSendMessage(text='Eh siapa bilang m****? Ntar dicubit Deborah lho'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/Meme-1.png',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/Meme-1.png'),
    ImageSendMessage(original_content_url='https://hmif-bot.herokuapp.com/images/Meme-2.png',
                     preview_image_url='https://hmif-bot.herokuapp.com/images/Meme-2.png'),
]

reply_help = \
    '''*Query*
help hmif bot deadline
help hmif bot seminar
help hmif bot sidang
help hmif bot ujian
'''

reply_help_deadline = \
    '''*Query*
Format 1:
Ada deadline apa saja untuk <Nama Jurusan> <Tahun Angkatan> <Jangka Waktu>

Format 2:
Ada deadline apa saja untuk <Nama Jurusan> <Nama Angkatan> <Jangka Waktu>

Jangka Waktu:
- hari ini
- minggu ini
- bulan ini
- besok
- minggu depan
- sejauh ini

*Contoh*
Ada deadline apa saja untuk STI 18 bulan ini
Ada deadline apa saja untuk Async bulan ini
'''

reply_help_seminar = \
    '''*Query*
Format 1:
Ada seminar apa saja <Jangka Waktu>

Format 2:
Ada sidang apa saja <Jangka Waktu>

Jangka Waktu:
- hari ini
- minggu ini
- bulan ini
- besok
- minggu depan
- sejauh ini

*Contoh*
Ada seminar apa saja bulan ini
Ada sidang apa saja besok
'''

reply_help_ujian = \
    '''*Query*
Format 1:
Ada ujian apa saja untuk <Nama Jurusan> <Tahun Angkatan> <Jangka Waktu>

Format 2:
Ada ujian apa saja untuk <Nama Jurusan> <Nama Angkatan> <Jangka Waktu>

Jangka Waktu:
- hari ini
- minggu ini
- bulan ini
- besok
- minggu depan
- sejauh ini

*Contoh*
Ada ujian apa saja untuk STI 18 besok
Ada ujian apa saja untuk Async minggu ini
'''
