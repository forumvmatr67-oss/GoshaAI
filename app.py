from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_web(query):
    """Поиск в интернете через Google (упрощённый вариант)"""
    try:
        # Формируем URL для поиска
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            # Ищем блоки с результатами поиска (классы могут меняться)
            for g in soup.find_all('div', class_='g')[:5]:  # берём первые 5 результатов
                title_tag = g.find('h3')
                link_tag = g.find('a')
                desc_tag = g.find('div', {'data-sncf': '1'})

                if title_tag and link_tag:
                    title = title_tag.get_text()
                    link = link_tag['href']
                    description = desc_tag.get_text() if desc_tag else "Описание недоступно"

                    results.append({
                        'title': title,
                        'link': link,
                        'description': description
                    })
            return results
        else:
            return [{'error': f'HTTP {response.status_code}'}]
    except Exception as e:
        return [{'error': str(e)}]

@app.route('/search', methods=['POST'])
def handle_search():
    query = request.json.get('query', '')
    if not query:
        return jsonify({'error': 'Пустой запрос'}), 400

    results = search_web(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
