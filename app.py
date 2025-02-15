import pandas as pd
import requests
import streamlit as st
from datetime import datetime
import base64
import os
import json
import time
import hashlib
import hmac
from bs4 import BeautifulSoup

def get_version_number():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    
    response = requests.get("https://www.fotmob.com/", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    version_element = soup.find('span', class_=lambda cls: cls and 'VersionNumber' in cls)
    if version_element:
        return version_element.text.strip()
    else:
        return None
    
version_number = get_version_number()

def get_xmas_pass():
    url = 'https://raw.githubusercontent.com/bariscanyeksin/streamlit_radar/refs/heads/main/xmas_pass.txt'
    response = requests.get(url)
    if response.status_code == 200:
        file_content = response.text
        return file_content
    else:
        print(f"Failed to fetch the file: {response.status_code}")
        return None
    
xmas_pass = get_xmas_pass()

def create_xmas_header(url, password):
        try:
            timestamp = int(datetime.now().timestamp() * 1000)
            request_data = {
                "url": url,
                "code": timestamp,
                "foo": version_number
            }
            
            json_string = f"{json.dumps(request_data, separators=(',', ':'))}{password.strip()}"
            signature = hashlib.md5(json_string.encode('utf-8')).hexdigest().upper()
            body = {
                "body": request_data,
                "signature": signature
            }
            encoded = base64.b64encode(json.dumps(body, separators=(',', ':')).encode('utf-8')).decode('utf-8')
            return encoded
        except Exception as e:
            return f"Error generating signature: {e}"

def headers_playerData(player_id):
    api_url = "/api/playerData?id=" + str(player_id)
    xmas_value = create_xmas_header(api_url, xmas_pass)
    
    headers = {
        'accept': '*/*',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://www.fotmob.com/en-GB/players/{player_id}/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-mas': f'{xmas_value}',
    }
    
    return headers

def headers_season_stats(player_id, season_id):
    api_url = f"/api/playerStats?playerId={player_id}&seasonId={season_id}"
    xmas_value = create_xmas_header(api_url, xmas_pass)
    
    headers = {
        'accept': '*/*',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://www.fotmob.com/en-GB/players/{player_id}/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-mas': f'{xmas_value}',
    }
    
    return headers

def headers_matchDetails(match_id):
    api_url = "/api/matchDetails?matchId=" + str(match_id)
    xmas_value = create_xmas_header(api_url, xmas_pass)
    
    headers = {
        'accept': '*/*',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://www.fotmob.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-mas': f'{xmas_value}',
    }
    
    return headers

def fetch_players(search_term):
    if not search_term.strip():
        return {}

    headers = {
        'accept': '*/*',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'if-none-match': '"ye9k3y5smr9ux"',
        'priority': 'u=1, i',
        'referer': 'https://www.fotmob.com',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-mas': 'eyJib2R5Ijp7InVybCI6Ii9hcGkvcGxheWVyRGF0YT9pZD0xMDkyMDE1IiwiY29kZSI6MTczMzIyNDA3NjgxOSwiZm9vIjoiNGJkMDI2ODk4In0sInNpZ25hdHVyZSI6IkFFMDUwMEY0NTY1MTU2OUUwQjJBNDlENjdGM0ZBQkI4In0='
    }

    params = {
        'hits': '50',
        'lang': 'tr,en',
        'term': search_term,
    }

    response = requests.get('https://www.fotmob.com/api/search/suggest', params=params, headers=headers)
    
    try:
        data = response.json()
    except ValueError:
        st.error("API yanıtı JSON formatında değil veya boş.")
        return {}

    if not isinstance(data, list) or len(data) == 0 or 'suggestions' not in data[0]:
        st.error("Beklenen JSON yapısı bulunamadı.")
        return {}

    suggestions = data[0]['suggestions']
    player_options = {f"{player['name']} ({player['teamName']})": player['id'] for player in suggestions if player['type'] == 'player'}
    return player_options

def get_player_data(player_id):
    url = f"https://www.fotmob.com/api/playerData?id={player_id}"
    headers = headers_playerData(player_id)
    response = requests.get(url, headers=headers)
    return response.json()

def get_match_details(match_id):
    url = f"https://www.fotmob.com/api/matchDetails?matchId={match_id}"
    headers = headers_matchDetails(match_id)
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    st.title("Futbolcu Maç İstatistikleri")
    
    search_term = st.text_input("Oyuncu Ara", "")
    
    if search_term:
        player_options = fetch_players(search_term)
        
        if player_options:
            selected_player = st.selectbox(
                "Oyuncu Seç",
                options=list(player_options.keys()),
                key="player_select"
            )
        else:
            st.warning("Oyuncu bulunamadı.")
    
    # Ana container'da maç verileri
    if 'player_select' in st.session_state and st.session_state.player_select:
        player_id = player_options[st.session_state.player_select]
        player_data = get_player_data(player_id)
        
        if 'recentMatches' in player_data:
            matches = player_data['recentMatches']
            
            # Mevcut ligleri bul
            leagues = list(set(match['leagueName'] for match in matches))
            selected_league = st.selectbox("Lig Seçin", leagues)
            
            # Seçilen lige göre maçları filtrele
            filtered_matches = [match for match in matches if match['leagueName'] == selected_league][:5]
            
            # Maç detaylarını topla
            match_stats = []
            for match in filtered_matches:
                try:
                    match_details = get_match_details(match['id'])
                    
                    # Daha kapsamlı hata kontrolü
                    if not match_details:
                        continue
                        
                    content = match_details.get('content')
                    if not content:
                        continue
                        
                    player_stats = content.get('playerStats')
                    if not player_stats:
                        continue
                        
                    player_match_stats = player_stats.get(str(player_id))
                    if not player_match_stats or 'stats' not in player_match_stats:
                        continue

                    # Maç bilgilerini ekle
                    stats_row = {
                        'Tarih': datetime.fromisoformat(match['matchDate']['utcTime'].replace('Z', '+00:00')).strftime('%d/%m/%Y'),
                        'Maç': f"{match['teamName']} vs {match['opponentTeamName']}",
                        'Skor': f"{match['homeScore']} - {match['awayScore']}",
                    }
                    
                    # İstenen istatistikleri topla
                    wanted_stats = {
                        'Goals': ('top_stats', 'Goals'),
                        'Headers scored': ('attack', 'Headed goals'),
                        'Assists': ('top_stats', 'Assists'),
                        'Accurate shots': ('attack', 'Shot accuracy'),
                        'Yellow cards': ('top_stats', 'Yellow cards'),
                        'Red cards': ('top_stats', 'Red cards'),
                        'Was fouled': ('duels', 'Was fouled'),
                        'Fouls committed': ('duels', 'Fouls committed'),
                        'Accurate passes': ('top_stats', 'Accurate passes'),
                        'Offsides': ('attack', 'Offsides'),
                        'Minutes': ('top_stats', 'Minutes played')
                    }
                    
                    # Her stat kategorisini kontrol et
                    for stat_category in player_match_stats['stats']:
                        category_title = stat_category['key']
                        
                        if 'stats' in stat_category:
                            # İstenen istatistikleri bul
                            for stat_name, (cat_key, stat_key) in wanted_stats.items():
                                if category_title == cat_key and stat_key in stat_category['stats']:
                                    stat_data = stat_category['stats'][stat_key]
                                    if 'stat' in stat_data:
                                        if stat_data['stat'].get('type') == 'fractionWithPercentage':
                                            value = stat_data['stat'].get('value', 0)
                                            total = stat_data['stat'].get('total', 0)
                                            stat_value = f"{value}/{total}"
                                        else:
                                            value = stat_data['stat'].get('value', '')
                                            stat_value = str(value) if value != '' else '-'
                                        
                                        stats_row[stat_name] = stat_value
                    
                    match_stats.append(stats_row)
                except Exception as e:
                    st.error(f"Maç verisi alınırken hata oluştu: {str(e)}")
                    continue
            
            if match_stats:
                # DataFrame oluştur ve NaN değerleri '-' ile değiştir
                df = pd.DataFrame(match_stats).astype(str)
                df = df.replace({'nan': '-', 'NaN': '-', '<NA>': '-'})
                
                # Maç sütun başlıklarını oluştur
                match_columns = []
                for _, row in df.iterrows():
                    match_parts = row['Maç'].split(' vs ')
                    match_columns.append(f"{match_parts[0]} {row['Skor']} {match_parts[1]}")
                
                # DataFrame'i yeniden düzenle
                df = df.drop(['Maç', 'Skor'], axis=1)  # Tarih'i tutuyoruz
                df = df.transpose()
                df.columns = match_columns
                
                # İndex ismini temizle
                df.index.name = None
                
                # İstatistik başlıklarını Türkçeleştir
                turkish_names = {
                    'Goals': 'Gol',
                    'Headers scored': 'Kafa Golü',
                    'Assists': 'Asist',
                    'Accurate shots': 'İsabetli Şut',
                    'Yellow cards': 'Sarı Kart',
                    'Red cards': 'Kırmızı Kart',
                    'Was fouled': 'Maruz Kalınan Faul',
                    'Fouls committed': 'Yapılan Faul',
                    'Accurate passes': 'İsabetli Pas',
                    'Offsides': 'Ofsayt',
                    'Minutes': 'Dakika',
                    'Tarih': 'Tarih'
                }
                
                df.index = df.index.map(lambda x: turkish_names.get(x, x))
                
                # İstenen sıralamayı belirle
                row_order = [
                    'Tarih',
                    'Dakika',
                    'Gol',
                    'Asist',
                    'İsabetli Şut',
                    'İsabetli Pas',
                    'Maruz Kalınan Faul',
                    'Yapılan Faul',
                    'Ofsayt'
                ]
                
                # DataFrame'i yeniden sırala
                df = df.reindex(row_order)
                
                # NaN değerleri tekrar kontrol et ve değiştir
                df = df.fillna('-')
                
                # İlk DataFrame gösterimi
                st.dataframe(
                    df,
                    use_container_width=True
                )
                
                # İstatistik analizleri için sekmeler
                tabs = st.tabs(["İsabetli Pas Analizi", "Gol Analizi", "Şut Analizi", "Faul Analizi"])
                
                with tabs[0]:  # İsabetli Pas Analizi
                    # İsabetli pas analizi
                    accurate_passes = []
                    minutes_played = []
                    
                    for col in df.columns:
                        passes = df.loc['İsabetli Pas', col]
                        minutes = df.loc['Dakika', col]
                        
                        # Sadece geçerli verileri al (- veya None olmayan)
                        if passes != '-' and passes is not None:
                            try:
                                successful, total = map(int, passes.split('/'))
                                minutes_value = int(minutes) if minutes != '-' and minutes is not None else 0
                                
                                # En az 15 dakika oynadığı maçları değerlendir
                                if minutes_value >= 15:
                                    # Başarı oranını hesapla
                                    success_rate = successful / total if total > 0 else 0
                                    accurate_passes.append((successful, total, success_rate))
                            except (ValueError, AttributeError):
                                continue
                    
                    if len(accurate_passes) >= 2:  # En az 2 maç verisi varsa analiz yap
                        # Başarı oranlarının ortalamasını al
                        avg_success_rate = sum(x[2] for x in accurate_passes) / len(accurate_passes)
                        # Ortalama pas sayısını hesapla
                        avg_total_passes = sum(x[1] for x in accurate_passes) / len(accurate_passes)
                        # Beklenen isabetli pas sayısı
                        expected_successful = int(avg_success_rate * avg_total_passes)
                        
                        # Güven aralığı için alt sınır (0.8 çarpanı)
                        lower_bound = int(expected_successful * 0.8)
                        
                        if lower_bound > 0:
                            st.write(f"👉 Oyuncunun gelecek maçta en az {lower_bound} isabetli pas yapması öngörülebilir.")
                            # Maç başına ortalama başarılı pas ve toplam pas sayısı
                            avg_successful_per_match = sum(x[0] for x in accurate_passes) / len(accurate_passes)
                            avg_total_per_match = sum(x[1] for x in accurate_passes) / len(accurate_passes)
                            st.caption(f"(Son {len(accurate_passes)} maçta ortalama {avg_total_per_match:.0f} pas denemesinde {avg_successful_per_match:.1f} isabetli pas)")
                
                with tabs[1]:  # Gol Analizi
                    # Gol analizi
                    goals_data = []
                    
                    for col in df.columns:
                        goals = df.loc['Gol', col]
                        minutes = df.loc['Dakika', col]
                        
                        # Sadece geçerli verileri al (- veya None olmayan)
                        if goals != '-' and goals is not None and minutes != '-' and minutes is not None:
                            try:
                                goals_value = int(goals)
                                minutes_value = int(minutes)
                                
                                # En az 15 dakika oynadığı maçları değerlendir
                                if minutes_value >= 15:
                                    goals_data.append((goals_value, minutes_value))
                            except (ValueError, AttributeError):
                                continue
                    
                    if len(goals_data) >= 2:  # En az 2 maç verisi varsa analiz yap
                        total_goals = sum(x[0] for x in goals_data)
                        total_minutes = sum(x[1] for x in goals_data)
                        goals_per_90 = (total_goals * 90) / total_minutes
                        
                        if total_goals > 0:
                            st.write(f"👉 Oyuncunun 90 dakika başına {goals_per_90:.2f} gol ortalaması var.")
                            st.caption(f"(Son {len(goals_data)} maçta toplam {total_goals} gol, {total_minutes} dakika oynadı)")
                        else:
                            st.write("👉 Son maçlarda gol atamadı.")
                
                with tabs[2]:  # Şut Analizi
                    # Şut analizi
                    shots_data = []
                    
                    for col in df.columns:
                        shots = df.loc['İsabetli Şut', col]
                        minutes = df.loc['Dakika', col]
                        
                        # Sadece geçerli verileri al (- veya None olmayan)
                        if shots != '-' and shots is not None:
                            try:
                                successful, total = map(int, shots.split('/'))
                                minutes_value = int(minutes) if minutes != '-' and minutes is not None else 0
                                
                                # En az 15 dakika oynadığı maçları değerlendir
                                if minutes_value >= 15:
                                    # Şut isabeti oranını hesapla
                                    accuracy_rate = successful / total if total > 0 else 0
                                    shots_data.append((successful, total, accuracy_rate, minutes_value))
                            except (ValueError, AttributeError):
                                continue
                    
                    if len(shots_data) >= 2:  # En az 2 maç verisi varsa analiz yap
                        total_successful = sum(x[0] for x in shots_data)
                        total_attempts = sum(x[1] for x in shots_data)
                        total_minutes = sum(x[3] for x in shots_data)
                        
                        if total_attempts > 0:
                            accuracy_percentage = (total_successful / total_attempts) * 100
                            shots_per_90 = (total_attempts * 90) / total_minutes
                            
                            st.write(f"👉 Oyuncunun şut isabeti: %{accuracy_percentage:.1f}")
                            st.caption(f"(Son {len(shots_data)} maçta {total_attempts} şut denemesinde {total_successful} isabet, 90 dk başına {shots_per_90:.1f} şut)")
                        else:
                            st.write("👉 Son maçlarda şut denemesi yok.")
                
                with tabs[3]:  # Faul Analizi
                    # Faul verileri
                    foul_data = []
                    
                    for col in df.columns:
                        fouls_committed = df.loc['Yapılan Faul', col]
                        fouls_suffered = df.loc['Maruz Kalınan Faul', col]
                        minutes = df.loc['Dakika', col]
                        
                        try:
                            minutes_value = int(minutes) if minutes != '-' and minutes is not None else 0
                            
                            # Sadece geçerli verileri al
                            if fouls_committed != '-' and fouls_suffered != '-':
                                fouls_committed_value = int(fouls_committed)
                                fouls_suffered_value = int(fouls_suffered)
                                foul_data.append((fouls_committed_value, fouls_suffered_value, minutes_value))
                            
                        except (ValueError, AttributeError):
                            continue
                    
                    if foul_data:  # En az 1 maç verisi varsa analiz yap
                        total_committed = sum(x[0] for x in foul_data)
                        total_suffered = sum(x[1] for x in foul_data)
                        total_minutes = sum(x[2] for x in foul_data)
                        
                        # 90 dakika başına ortalamalar (eğer toplam dakika 0'dan büyükse)
                        if total_minutes > 0:
                            fouls_committed_per_90 = (total_committed * 90) / total_minutes
                            fouls_suffered_per_90 = (total_suffered * 90) / total_minutes
                        else:
                            fouls_committed_per_90 = 0
                            fouls_suffered_per_90 = 0
                        
                        # Maç başına ortalamalar
                        avg_committed = total_committed / len(foul_data)
                        avg_suffered = total_suffered / len(foul_data)
                        
                        st.write(f"👉 Oyuncunun 90 dakika başına yaptığı faul: {fouls_committed_per_90:.1f}")
                        st.caption(f"(Son {len(foul_data)} maçta toplam {total_committed} faul yaptı, maç başına {avg_committed:.1f} faul)")
                        
                        st.write(f"👉 Oyuncuya 90 dakika başına yapılan faul: {fouls_suffered_per_90:.1f}")
                        st.caption(f"(Son {len(foul_data)} maçta toplam {total_suffered} faul yapıldı, maç başına {avg_suffered:.1f} faul)")
                
                st.markdown("---")  # Ayırıcı çizgi
                st.subheader("Son 5 Maç")
                
                # Son 5 maç için veri toplama
                last_5_matches = player_data['recentMatches'][:6]
                match_stats_last5 = []
                
                for match in last_5_matches:
                    try:
                        match_details = get_match_details(match['id'])
                        
                        # Daha kapsamlı hata kontrolü
                        if not match_details:
                            continue
                            
                        content = match_details.get('content')
                        if not content:
                            continue
                            
                        player_stats = content.get('playerStats')
                        if not player_stats:
                            continue
                            
                        player_match_stats = player_stats.get(str(player_id))
                        if not player_match_stats or 'stats' not in player_match_stats:
                            continue

                        stats_row = {
                            'Tarih': datetime.fromisoformat(match['matchDate']['utcTime'].replace('Z', '+00:00')).strftime('%d/%m/%Y'),
                            'Maç': f"{match['teamName']} vs {match['opponentTeamName']}",
                            'Skor': f"{match['homeScore']} - {match['awayScore']}",
                        }
                        
                        # Aynı istatistikleri topla
                        for stat_category in player_match_stats['stats']:
                            category_title = stat_category['key']
                            
                            if 'stats' in stat_category:
                                for stat_name, (cat_key, stat_key) in wanted_stats.items():
                                    if category_title == cat_key and stat_key in stat_category['stats']:
                                        stat_data = stat_category['stats'][stat_key]
                                        if 'stat' in stat_data:
                                            if stat_data['stat'].get('type') == 'fractionWithPercentage':
                                                value = stat_data['stat'].get('value', 0)
                                                total = stat_data['stat'].get('total', 0)
                                                stat_value = f"{value}/{total}"
                                            else:
                                                value = stat_data['stat'].get('value', '')
                                                stat_value = str(value) if value != '' else '-'
                                            
                                            stats_row[stat_name] = stat_value
                        
                        match_stats_last5.append(stats_row)
                    except Exception as e:
                        st.error(f"Maç verisi alınırken hata oluştu: {str(e)}")
                        continue
                
                if match_stats_last5:
                    # Son 5 maç için DataFrame oluştur
                    df_last5 = pd.DataFrame(match_stats_last5).astype(str)
                    df_last5 = df_last5.replace({'nan': '-', 'NaN': '-', '<NA>': '-'})
                    
                    # Maç sütun başlıklarını oluştur
                    match_columns_last5 = []
                    for _, row in df_last5.iterrows():
                        match_parts = row['Maç'].split(' vs ')
                        match_columns_last5.append(f"{match_parts[0]} {row['Skor']} {match_parts[1]}")
                    
                    # DataFrame'i yeniden düzenle
                    df_last5 = df_last5.drop(['Maç', 'Skor'], axis=1)
                    df_last5 = df_last5.transpose()
                    df_last5.columns = match_columns_last5
                    
                    # İndex'i Türkçeleştir ve sırala
                    df_last5.index = df_last5.index.map(lambda x: turkish_names.get(x, x))
                    df_last5 = df_last5.reindex(row_order)
                    df_last5 = df_last5.fillna('-')
                    
                    # Son 5 maç tablosunu göster
                    st.dataframe(
                        df_last5,
                        use_container_width=True
                    )
            else:
                st.warning("Seçilen maçlar için istatistik bulunamadı.")

if __name__ == "__main__":
    main()