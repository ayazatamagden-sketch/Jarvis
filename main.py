from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import datetime
import webbrowser
import subprocess
import random
import speech_recognition as sr
import threading
import time
from gtts import gTTS
import pygame
import tempfile
import os

# Pygame ses sistemini başlatalım
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Pygame ses başlatma hatası: {e}")

def konus(metin):
    print(f"JARVIS: {metin}")
    def ses_cal():
        temp_file = None
        try:
            tts = gTTS(text=metin, lang='tr', slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
            tts.save(temp_file)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.music.unload()
        except Exception as ex:
            print(f"Ses çalma hatası: {ex}")
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            
    threading.Thread(target=ses_cal).start()

class JarvisMobilApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.size = (400, 200)
        Window.title = "JARVIS Arka Plan Çekirdeği"
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.durum_etiketi = Label(
            text="JARVIS v10.1 - Güçlendirilmiş Başlatıcı\n'Jarvis' bekleniyor...",
            font_size=20,
            halign='center',
            valign='middle'
        )
        self.durum_etiketi.bind(size=self.durum_etiketi.setter('text_size'))
        layout.add_widget(self.durum_etiketi)
        
        threading.Thread(target=self.arkaplanda_dinle, daemon=True).start()
        return layout

    def evrensel_uygulama_ac(self, uygulama_adi):
        uygulama_adi = uygulama_adi.lower().strip()
        print(f"Açılmak istenen uygulama: {uygulama_adi}")
        
        # 1. Web tabanlı ve özel servisler
        if "youtube" in uygulama_adi:
            konus("Hemen YouTube'u açıyorum efendim.")
            webbrowser.open("https://www.youtube.com")
            return
        elif "whatsapp" in uygulama_adi:
            konus("Hemen WhatsApp'ı açıyorum efendim.")
            webbrowser.open("https://web.whatsapp.com")
            return
        elif "google" in uygulama_adi:
            konus("Hemen Google'ı açıyorum efendim.")
            webbrowser.open("https://www.google.com")
            return
            
        # 2. Windows Sistem Araçları
        elif "hesap" in uygulama_adi:
            konus("Hesap makinesini açıyorum efendim.")
            subprocess.Popen('calc.exe')
            return
        elif "not" in uygulama_adi or "defter" in uygulama_adi:
            konus("Not defterini açıyorum efendim.")
            subprocess.Popen('notepad.exe')
            return
        elif "kamera" in uygulama_adi:
            konus("Kamerayı açıyorum efendim.")
            subprocess.Popen('start microsoft.windows.camera:', shell=True)
            return

        # 3. Popüler Oyun ve Programlar için Doğrudan Protokoller (Örn: Steam, Discord, Valorant)
        bulundu = False
        try:
            if "steam" in uygulama_adi:
                konus("Steam açılıyor efendim.")
                subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')
                bulundu = True
            elif "discord" in uygulama_adi:
                konus("Discord açılıyor efendim.")
                subprocess.Popen(os.path.expanduser(r'~\\AppData\\Local\\Discord\\app-1.0.9000\\Discord.exe')) # Güncel yola göre değişebilir
                bulundu = True
            elif "valorant" in uygulama_adi or "riot" in uygulama_adi:
                konus("Valorant açılıyor efendim.")
                subprocess.Popen(r'C:\Riot Games\Riot Client\RiotClientServices.exe --launch-product=valorant --launch-patchline=live', shell=True)
                bulundu = True
            elif "spotify" in uygulama_adi:
                konus("Spotify açılıyor efendim.")
                subprocess.Popen(os.path.expanduser(r'~\\AppData\\Roaming\\Spotify\\Spotify.exe'))
                bulundu = True
        except Exception as e:
            print(f"Özel başlatma hatası: {e}")

        # 4. Eğer yukarıdakilerden biri değilse Windows kabuğu üzerinden çalıştırmayı dene
        if not bulundu:
            try:
                konus(f"{uygulama_adi.capitalize()} açılıyor efendim.")
                # Windows'un kendi arama ve başlatma komutu
                subprocess.Popen(f'start {uygulama_adi}', shell=True)
                bulundu = True
            except Exception as e:
                print(f"Genel açma hatası: {e}")
                
        if not bulundu:
            konus(f"Maalesef {uygulama_adi} uygulamasını bulamadım efendim.")

    def arkaplanda_dinle(self):
        konus("Arka plan sistemleri aktif efendim. Dinlemedeyim.")
        r = sr.Recognizer()
        
        while True:
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    self.durum_etiketi.text = "Gizli Modda Dinleniyor...\n('Jarvis' deyin)"
                    audio = r.listen(source, timeout=None, phrase_time_limit=4)
                
                duyulan = r.recognize_google(audio, language="tr-TR").lower()
                print(f"Duyulan: {duyulan}")
                
                if "jarvis" in duyulan:
                    self.durum_etiketi.text = "Dinliyorum efendim..."
                    konus("Dinliyorum efendim.")
                    
                    with sr.Microphone() as source:
                        komut_audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    
                    komut = r.recognize_google(komut_audio, language="tr-TR").lower()
                    print(f"Komut Alındı: {komut}")
                    self.durum_etiketi.text = f"Komut:\n'{komut}'"
                    
                    if "saat" in komut:
                        su_an = datetime.datetime.now().strftime("%H:%M")
                        konus(f"Saat şu an {su_an} efendim.")
                    elif "motivasyon" in komut or "söz" in komut:
                        sozler = [
                            "Bazen yürümeyi öğrenmeden önce koşman gerekir efendim.",
                            "Ben dahi, milyarder, hayırseverim.",
                            "Kendi kaderimizi kendimiz çizeriz efendim."
                        ]
                        konus(random.choice(sozler))
                    elif "aç" in komut:
                        uygulama = komut.replace("aç", "").replace("uygulamasını", "").strip()
                        if uygulama:
                            self.evrensel_uygulama_ac(uygulama)
                        else:
                            konus("Hangi uygulamayı açmamı istediğinizi duyamadım efendim.")
                    else:
                        konus("Hemen ilgileniyorum efendim.")
                        
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Hata: {e}")
                time.sleep(0.5)

if __name__ == '__main__':
    JarvisMobilApp().run()
