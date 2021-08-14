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

reply_help = '''
Ada deadline apa saja untuk <Nama Jurusan> <Tahun Angkatan> <Jangka Waktu>
Ada deadline apa saja untuk <Nama Jurusan> <Nama Angkatan> <Jangka Waktu>

Jangka Waktu:
- hari ini
- minggu ini
- bulan ini
- besok
- minggu depan
'''