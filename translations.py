# translations.py - multilingual support for bot texts with inline keyboard language selection

translations = {
    "start": {
        "az": "🛡️ <b>SOSİAL MÜhİT</b> Telegram kanalına qoşulmaq üçün aşağıdakı məlumatları diqqətlə və düzgün şəkildə təqdim etməyiniz xahiş olunur.",
        "ru": "🛡️ <b>СОЦИАЛЬНАЯ СРЕДА</b> Для присоединения к Telegram-каналу, пожалуйста, внимательно и правильно предоставьте информацию ниже.",
        "en": "🛡️ <b>SOCIAL ENVIRONMENT</b> To join the Telegram channel, please carefully and correctly provide the information below.",
        "tr": "🛡️ <b>SOSYAL ORTAM</b> Telegram kanalına katılmak için lütfen aşağıdaki bilgileri dikkatli ve doğru bir şekilde doldurunuz."
    },
    "choose_language": {
        "az": "🌍 Zəhmət olmasa, davam etmək üçün dili seçin:",
        "ru": "🌍 Пожалуйста, выберите язык для продолжения:",
        "en": "🌍 Please choose a language to continue:",
        "tr": "🌍 Lütfen devam etmek için bir dil seçin:"
    },
    "language_selected": {
        "az": "✅ Diliniz <b>Azərbaycanca</b> olaraq təyin edildi.",
        "ru": "✅ Ваш язык установлен на <b>русский</b>.",
        "en": "✅ Your language has been set to <b>English</b>.",
        "tr": "✅ Diliniz <b>Türkçe</b> olarak ayarlandı."
    },
    "enter_name": {
        "az": "✍️ Ad və soyadınızı daxil edin:",
        "ru": "✍️ Введите ваше имя и фамилию:",
        "en": "✍️ Please enter your full name:",
        "tr": "✍️ Lütfen adınızı ve soyadınızı girin:"
    },
    "enter_phone": {
        "az": "📞 Telefon nömrənizi +994 formatında daxil edin:",
        "ru": "📞 Введите номер телефона в формате +994:",
        "en": "📞 Enter your phone number in +994 format:",
        "tr": "📞 Telefon numaranızı +994 formatında girin:"
    },
    "invalid_phone": {
        "az": "❗ Zəhmət olmasa, düzgün formatda nömrə daxil edin. Məsələn: +994501234567",
        "ru": "❗ Пожалуйста, введите номер в правильном формате. Например: +994501234567",
        "en": "❗ Please enter the number in correct format. Example: +994501234567",
        "tr": "❗ Lütfen doğru formatta numara girin. Örn: +994501234567"
    },
    "payment_info": {
        "az": "💰 Zəhmət olmasa, aşağıdakı kart nömrəsinə ödəniş edin:",
        "ru": "💰 Пожалуйста, оплатите на следующий номер карты:",
        "en": "💰 Please make the payment to the card number below:",
        "tr": "💰 Lütfen aşağıdaki kart numarasına ödeme yapınız:"
    },
    "send_screenshot": {
        "az": "📸 Ödəniş etdikdən sonra qəbzin şəklini bu çatda paylaşın.",
        "ru": "📸 После оплаты отправьте фото чека в этот чат.",
        "en": "📸 After payment, share the screenshot of the receipt in this chat.",
        "tr": "📸 Ödeme yaptıktan sonra fişin ekran görüntüsünü bu sohbette paylaşın."
    },
    "only_photo": {
        "az": "❗ Zəhmət olmasa, yalnız ödəniş qəbzinin şəklini göndərin.",
        "ru": "❗ Пожалуйста, отправьте только фото квитанции об оплате.",
        "en": "❗ Please send only a photo of the payment receipt.",
        "tr": "❗ Lütfen sadece ödeme makbuzunun fotoğrafını gönderin."
    },
    "registration_complete": {
        "az": "✅ Qeydiyyat tamamlandı. Məlumat adminə göndərildi.",
        "ru": "✅ Регистрация завершена. Информация отправлена администратору.",
        "en": "✅ Registration completed. Information sent to admin.",
        "tr": "✅ Kayıt tamamlandı. Bilgiler yöneticilere gönderildi."
    },
    "wait_for_link": {
        "az": "📨 Təsdiqdən sonra 24 saatlıq keçərli giriş linki göndəriləcək.",
        "ru": "📨 После подтверждения будет отправлена ссылка с доступом на 24 часа.",
        "en": "📨 After approval, a one-time 24h access link will be sent.",
        "tr": "📨 Onaydan sonra size 24 saat geçerli giriş bağlantısı gönderilecektir."
    },
    "approve_button": {
        "az": "✅ Təsdiqlə",
        "ru": "✅ Подтвердить",
        "en": "✅ Approve",
        "tr": "✅ Onayla"
    },
    "link_sent": {
        "az": "✅ Giriş linkiniz göndərildi.",
        "ru": "✅ Ваша ссылка для входа отправлена.",
        "en": "✅ Your access link has been sent.",
        "tr": "✅ Giriş bağlantınız gönderildi."
    },
    "error_user_not_found": {
        "az": "❗ Xəta: istifadəçi məlumatı tapılmadı.",
        "ru": "❗ Ошибка: данные пользователя не найдены.",
        "en": "❗ Error: user data not found.",
        "tr": "❗ Hata: kullanıcı bilgisi bulunamadı."
    },
    "error_callback_data": {
        "az": "❗ Xəta: callback məlumatı tapılmadı.",
        "ru": "❗ Ошибка: данные callback не найдены.",
        "en": "❗ Error: callback data not found.",
        "tr": "❗ Hata: geri çağırma verisi bulunamadı."
    },
    "error": {
        "az": "❗ Naməlum xəta baş verdi.",
        "ru": "❗ Произошла неизвестная ошибка.",
        "en": "❗ An unknown error occurred.",
        "tr": "❗ Bilinmeyen bir hata oluştu."
    }
}

def get_text(key, lang="az"):
    return translations.get(key, {}).get(lang, translations.get(key, {}).get("az", ""))
